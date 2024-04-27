In this project we will deploy deep learning model using mlflow model registry.

## 1. Start mlflow
```commandline
cd ~/02_mlops_docker/

docker-compose up -d mysql mlflow minio
```
## 2. Copy/push your project to VM.
```commandline
mv 11_deploy_fastapi_deeplearning_mlflow/ 11
cd 11
```
## 3. Activate/create conda/virtual env
```commandline
conda activate fastapi
```
## 4. Install requirements
```commandline
pip install -r requirements.txt
```

### 4.1. Get data
- Data source: https://archive.ics.uci.edu/ml/machine-learning-databases/00331/
```commandline
cd ~/datasets
wget -O sentiment_labeled_sentences.zip https://archive.ics.uci.edu/ml/machine-learning-databases/00331/sentiment%20labelled%20sentences.zip
unzip sentiment_labeled_sentences.zip
mv sentiment\ labelled\ sentences sentiment_labeled_sentences
ll sentiment_labeled_sentences
```
## 5. Train and log your experiment to mlflow
```commandline
cd ~/11; python train.py
```
## 6. Register model on mlflow UI
- Learn model name and version from Mlflow web UI
- Update model name version in the main.py

## 7. Start uvicorn
```commandline
uvicorn \
main:app --host 0.0.0.0 \
--port 8002 \
--reload
```

## 8. Open docs
` http://localhost:8002/docs# `

## 9. Close docker-compose
```commandline
cd ~/02_mlops_docker/; docker-compose down
```