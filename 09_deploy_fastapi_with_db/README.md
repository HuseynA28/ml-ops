In this project we will deploy iris and advertising classification models on 2 different endpoints.

Endpoints will be:  
- http://127.0.0.1:8000/prediction/iris
- http://127.0.0.1:8000/prediction/advertising

Per each request a record will be saved in database as well as returned prediction response.
## Keywords
- fastapi
- mysql
- create mysql database, user, grant privileges
- scikit-learn
- RandomForestRegressor
- KNeighborsClassifier
## Create database, table and user
```commandline
cd 02_mlops_docker/

# Run only mysql container
docker-compose up -d mysql

# Connect mysql container 
docker exec -it mlflow_db mysql -u root -p

# Create database 
mysql> create database mlops;


# Create user 
mysql> CREATE USER 'mlops_user'@'%' IDENTIFIED BY 'Ankara06';


# Grand mlops_user on mlops database 
mysql> GRANT ALL PRIVILEGES ON mlops.* TO 'mlops_user'@'%' WITH GRANT OPTION;


mysql> FLUSH PRIVILEGES;


mysql> exit

```

## Copy project to vm and rename it
```commandline
 mv 09_deploy_fastapi_with_db/ 09
 cd 09
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

## Activate fastapi and install requirements
```commandline
conda activate fastapi

pip install -r requirements.txt
```

## Run uvicorn
```commandline
 uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

## Prediction
### Iris
#### Request
```commandline
curl -X 'POST' \
  'http://localhost:8002/prediction/iris' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}'
```

#### Response
```commandline
{
  "prediction": "Iris-setosa",
  "db_record": {
    "sepal_length": 5.1,
    "petal_length": 1.4,
    "prediction": "Iris-setosa",
    "client_ip": "10.0.2.2",
    "sepal_width": 3.5,
    "id": 1,
    "petal_width": 0.2,
    "prediction_time": "2022-12-07T04:07:05"
  }
}
```

### Advertising
#### Request
```commandline
curl -X 'POST' \
  'http://localhost:8002/prediction/advertising' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tv": 230.1,
  "radio": 37.8,
  "newspaper": 69.2
}'
```
#### Response
```commandline
{
  "prediction": 22.066499999999973,
  "db_record": {
    "tv": 230.1,
    "newspaper": 69.2,
    "id": 2,
    "prediction_time": "2022-12-07T04:20:06",
    "client_ip": "10.0.2.2",
    "prediction": 22.0665,
    "radio": 37.8
  }
}
```
