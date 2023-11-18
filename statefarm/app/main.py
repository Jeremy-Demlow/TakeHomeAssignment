import pandas as pd
import joblib
import numpy as np
import asyncio
import os
import logging

from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from .models import PredictionRequest, BatchPredictionRequest


current_dir = os.getcwd()

MODEL_PATH = os.path.join(current_dir, "files/models/logistic_regression_model.pkl")
PREPROCESSOR_PATH = os.path.join(current_dir, "files/models/preprocessor.pkl")

if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
    raise FileNotFoundError(
        "Model and/or preprocessor files not found. Make sure they exist."
    )

try:
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
except Exception as e:
    logging.error(f"Error loading model or preprocessor: {str(e)}")
    raise

if model is None:
    logging.error("Failed to load the model.")
else:
    logging.info(f"Model loaded successfully: {type(model)}")
    if hasattr(model, "final_result"):
        if model.final_result is None:
            logging.error("Model final_result is None.")
        else:
            logging.info(f"Model final_result is set: {type(model.final_result)}")
    else:
        logging.error("Model does not have 'final_result' attribute.")

# Logging model's other attributes
model_attributes = dir(model)
logging.info(f"Model attributes: {model_attributes}")


app = FastAPI()


@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Perform a single prediction asynchronously.

    Args:
        request (PredictionRequest): Prediction request containing data for a single prediction.

    Returns:
        dict: Prediction response.
    """
    data_dict = {key: value for key, value in request.data.dict().items()}
    input_df = pd.DataFrame([data_dict])
    response = pd.DataFrame(
        model.final_result.predict(preprocessor.transform(input_df)[model.variables])
    ).rename(columns={0: "phat"})
    response["business_outcome"] = np.where(response["phat"] >= 0.75, 1, 0)
    response = response.to_dict(orient="records")[0]
    return response


@app.post("/batch_predict")
async def batch_predict(request: BatchPredictionRequest):
    """
    Batch process prediction requests asynchronously.

    Args:
        request (BatchPredictionRequest): Batch prediction request containing a list of data items.

    Returns:
        List[dict]: List of prediction responses, ordered based on the input order.
    """

    async def process_single_request(item):
        single_request = PredictionRequest(data=item)
        single_response = await predict(single_request)
        return single_response

    loop = asyncio.get_event_loop()
    responses = []

    with ThreadPoolExecutor() as executor:
        response_futures = await asyncio.gather(
            *[
                loop.run_in_executor(executor, process_single_request, item)
                for item in request.data
            ]
        )

    responses = await asyncio.gather(*response_futures)
    return responses
