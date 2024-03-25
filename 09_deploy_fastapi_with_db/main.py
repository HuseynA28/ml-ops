from fastapi import FastAPI, Depends, Request
import joblib
from models import Iris, Advertising, CreateUpdateIris, CreateUpdateAdvertising
from database import engine, get_db, create_db_and_tables
from sqlalchemy.orm import Session

# Read models saved during train phase
estimator_iris_loaded = joblib.load("saved_models/01.knn_with_iris_dataset.pkl")
encoder_iris_loaded = joblib.load("saved_models/02.iris_label_encoder.pkl")
estimator_advertising_loaded = joblib.load("saved_models/03.randomforest_with_advertising.pkl")

app = FastAPI()

# Creates all the tables defined in models module
create_db_and_tables()


def insert_iris(request, prediction, client_ip, db):
    new_iris = Iris(
        sepal_length=request["sepal_length"],
        sepal_width=request['sepal_width'],
        petal_length=request['petal_length'],
        petal_width=request['petal_width'],
        prediction=prediction,
        client_ip=client_ip
    )

    with db as session:
        session.add(new_iris)
        session.commit()
        session.refresh(new_iris)

    return new_iris


def insert_advertising(request, prediction, client_ip, db):
    new_advertising = Advertising(
        tv=request["tv"],
        radio=request['radio'],
        newspaper=request['newspaper'],
        prediction=prediction,
        client_ip=client_ip
    )

    with db as session:
        session.add(new_advertising)
        session.commit()
        session.refresh(new_advertising)

    return new_advertising


# prediction function
def make_iris_prediction(model, encoder, request):
    # parse input from request
    sepal_length = request["sepal_length"]
    sepal_width = request['sepal_width']
    petal_length = request['petal_length']
    petal_width = request['petal_width']

    # Make an input vector
    flower = [[sepal_length, sepal_width, petal_length, petal_width]]

    # Predict
    prediction_raw = model.predict(flower)

    # Convert Species index to Species name
    prediction_real = encoder.inverse_transform(prediction_raw)

    return prediction_real[0]


def make_advertising_prediction(model, request):
    # parse input from request
    tv = request["tv"]
    radio = request['radio']
    newspaper = request['newspaper']

    # Make an input vector
    advertising = [[tv, radio, newspaper]]

    # Predict
    prediction = model.predict(advertising)

    return prediction[0]


# Iris Prediction endpoint
@app.post("/prediction/iris")
def predict_iris(request: CreateUpdateIris, fastapi_req: Request,  db: Session = Depends(get_db)):
    prediction = make_iris_prediction(estimator_iris_loaded, encoder_iris_loaded, request.dict())
    db_insert_record = insert_iris(request=request.dict(), prediction=prediction,
                                          client_ip=fastapi_req.client.host,
                                          db=db)
    return {"prediction": prediction, "db_record": db_insert_record}


# Advertising Prediction endpoint
@app.post("/prediction/advertising")
async def predict_advertising(request: CreateUpdateAdvertising, fastapi_req: Request,  db: Session = Depends(get_db)):
    prediction = make_advertising_prediction(estimator_advertising_loaded, request.dict())
    db_insert_record = insert_advertising(request=request.dict(), prediction=prediction,
                                          client_ip=fastapi_req.client.host,
                                          db=db)
    return {"prediction": prediction, "db_record": db_insert_record}

@app.get("/")
async def root():
    return {"data":"Wellcome to MLOps API"}
