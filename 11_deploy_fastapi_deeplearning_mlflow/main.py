from fastapi import FastAPI
from schemas import Comment
import os
import mlflow.keras
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib

# Tell where is the tracking server and artifact server
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000/'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000/'

# Learn, decide and get model from mlflow model registry
model_name = "DL_Sentiment_Classification"
model_version = 1
model = mlflow.keras.load_model(
    model_uri=f"models:/{model_name}/{model_version}"
)

tokenizer_loaded = joblib.load("saved_models/keras-sentence-classification-tokenizer.pkl")

app = FastAPI()

# Note that model is coming from mlflow
def make_prediction(model, request):
    # parse input from request
    comment = [request["comment"]]

    # converting text to intergers
    token = tokenizer_loaded.texts_to_sequences(comment)
    #
    maxlen = 100
    #
    token = pad_sequences(token, padding='post', maxlen=maxlen)

    # # Predict
    prediction = model.predict(token)
    if prediction[0] > 0.5:
        return "positive"
    return "negtive"

# Advertising Prediction endpoint
@app.post("/prediction/comment")
async def predict_advertising(request: Comment):
    prediction = make_prediction(model, request.dict())
    print(prediction)
    return str(prediction)
