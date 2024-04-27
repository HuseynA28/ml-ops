#!/bin/bash
sudo yum -y update
sudo yum -y install git
python3 -m pip install virtualenv
python3 -m virtualenv fastapi
source /fastapi/bin/activate
git clone https://github.com/erkansirin78/fastapi-advertising-prediction.git
cd /fastapi-advertising-prediction/src/fastapi_advertising_prediction/
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload