import pandas as pd
import joblib
import numpy as np
import asyncio
import os
import logging
import logging.handlers
import time
import json

from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from fastapi import HTTPException
from .models import PredictionRequest, BatchPredictionRequest
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram, Counter


logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)


app = FastAPI()
Instrumentator().instrument(app).expose(app)
# TODO: Was working through getting this for elastic search
phat_histogram = Histogram(
    "prediction_phats",
    "Probability Histogram",
    buckets=(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1),
)
api_calls_counter = Counter("api_calls", "API Calls Counter")

current_dir = os.getcwd()
MODEL_PATH = os.path.join(current_dir, "files/models/logistic_regression_model.pkl")
PREPROCESSOR_PATH = os.path.join(current_dir, "files/models/preprocessor.pkl")


async def load_model_async(model_path):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, joblib.load, model_path)


@app.on_event("startup")
async def startup_event():
    global model, preprocessor
    model = await load_model_async(MODEL_PATH)
    preprocessor = await load_model_async(PREPROCESSOR_PATH)

    if model is None or preprocessor is None:
        logger.error("Failed to load the model or preprocessor. Stopping application.")
        raise Exception("Critical resource loading failed")


@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    Perform a single prediction asynchronously.

    Args:
        request (PredictionRequest): Prediction request containing data for a single prediction.

    Returns:
        dict: Prediction response.
    """
    try:
        api_calls_counter.inc()
        data_dict = {key: value for key, value in request.data.dict().items()}
        input_df = pd.DataFrame([data_dict])
        response = pd.DataFrame(
            model.final_result.predict(
                preprocessor.transform(input_df)[model.variables]
            )
        ).rename(columns={0: "phat"})
        response["business_outcome"] = np.where(response["phat"] >= 0.75, 1, 0)
        response = response.to_dict(orient="records")[0]
        phat_value = response["phat"]
        phat_histogram.observe(phat_value)
        prediction_log = {
            "timestamp": time.time(),
            "phat": phat_value,
            "business_outcome": response["business_outcome"],
        }
        logger.info(json.dumps(prediction_log))
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during prediction")
    return response


@app.post("/batch_predict_simple")
async def batch_predict_simple(request: BatchPredictionRequest):
    """
    Batch process prediction requests asynchronously.

    Args:
        request (BatchPredictionRequest): Batch prediction request containing a list of data items.

    Returns:
        List[dict]: List of prediction responses, ordered based on the input order.
    """
    try:

        async def process_single_request(item):
            single_request = PredictionRequest(data=item)
            single_response = await predict(single_request)
            return single_response

        loop = asyncio.get_event_loop()
        responses = []

        num_cpus = os.cpu_count()
        max_workers = num_cpus if num_cpus is not None else 4

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            response_futures = await asyncio.gather(
                *[
                    loop.run_in_executor(executor, process_single_request, item)
                    for item in request.data
                ]
            )

        responses = await asyncio.gather(*response_futures)
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during batch prediction")

    return responses


@app.post("/batch_predict")
async def batch_predict(request: BatchPredictionRequest):
    try:
        api_calls_counter.inc()
        data_dict = [item.dict() for item in request.data]
        input_df = pd.DataFrame(data_dict)
        batch_predictions = model.final_result.predict(
            preprocessor.transform(input_df)[model.variables]
        )
        business_outcomes = np.where(batch_predictions >= 0.75, 1, 0)

        results_df = pd.DataFrame(
            {
                "timestamp": time.time(),
                "phat": batch_predictions,
                "business_outcome": business_outcomes,
            }
        )

        logger.info(results_df.to_json(orient="records"))

        responses = results_df.to_dict(orient="records")
        return responses
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during batch prediction")
