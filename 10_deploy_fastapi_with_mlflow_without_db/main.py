from fastapi import FastAPI, Depends, Request
from schemas import Advertising
import os
from sqlalchemy.orm import Session
from mlflow.sklearn import load_model

# Tell where is the tracking server and artifact server
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000/'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000/'

# Learn, decide and get model from mlflow model registry
model_name = "AdvertisingRFModel"
model_version = 6
model = load_model(
    model_uri=f"models:/{model_name}/{model_version}"
)

app = FastAPI()


# Note that model is coming from mlflow
def make_advertising_prediction(model, request):
    # parse input from request
    TV = request["TV"]
    Radio = request['Radio']
    Newspaper = request['Newspaper']

    # Make an input vector
    advertising = [[TV, Radio, Newspaper]]

    # Predict
    prediction = model.predict(advertising)

    return prediction[0]


# Advertising Prediction endpoint
@app.post("/prediction/advertising")
async def predict_advertising(request: Advertising):
    prediction = make_advertising_prediction(model, request.dict())

    return {"prediction": prediction}
