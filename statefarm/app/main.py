import pandas as pd
import joblib
import numpy as np
import asyncio  # Import asyncio

from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from .models import PredictionRequest, BatchPredictionRequest

MODEL_PATH = "files/models/logistic_regression_model.pkl"
PREPROCESSOR_PATH = "files/models/preprocessor.pkl"
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

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
