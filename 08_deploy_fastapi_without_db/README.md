In this project we will deploy iris and advertising classification models on 2 different endpoints.

Endpoints will be:  
- http://127.0.0.1:8000/prediction/iris
- http://127.0.0.1:8000/prediction/advertising

## Copy project to vm and rename it
```commandline
 mv 08_deploy_fastapi_without_db/ 08
 cd 08
```

## Train models
### Activate ds-dev
```commandline
conda activate ds-dev

pip install -r requirements.txt
```

### Train models
```commandline
python train_advertising_model.py

python train_iris_model.py
```
## Create a Docker Image then Run
```commandline
docker image build -t ml-prediction-with-fastapi:1.0 .

docker run --rm \
--name ml-prediction \
-p 8000:8000 -d ml-prediction-with-fastapi:1.0
```

## List containers
```commandline
docker ps
 
 
CONTAINER ID   IMAGE                            COMMAND                  CREATED          STATUS          PORTS                                       NAMES
e769fdd84ba0   ml-prediction-with-fastapi:1.0   "/bin/sh -c 'uvicorn…"   19 minutes ago   Up 19 minutes   0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   ml-prediction
```

## Make Predictions
```commandline
curl -X 'POST' \
  'http://127.0.0.1:8000/prediction/iris' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "SepalLengthCm": 5.1,
  "SepalWidthCm": 3.5,
  "PetalLengthCm": 1.4,
  "PetalWidthCm": 0.2
}'
```

- Expected output: `"Iris-setosa"`

## Stop container
```commandline
docker container stop ml-prediction
```
