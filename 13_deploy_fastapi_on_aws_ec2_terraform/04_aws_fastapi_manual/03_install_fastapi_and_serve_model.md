### 1. Connect to Instance
![Connect to Instance](images/14_connect_to_instance.png 'Connect to Instance')

----------------------------------------------------------------------------

### 2. Connect
![Connect](images/15_connect.png 'Connect')


----------------------------------------------------------------------------

### 3. EC2 Shell
![EC2 Shell](images/16_ec2_shell.png 'EC2 Shell')


### 4. On EC2 terminal: yum update
` sudo yum -y update `

#### 5. On EC2 terminal: Python3 and pip versions
```commandline
python3 -V
Python 3.7.10


pip3 -V
pip 20.2.2 from /usr/lib/python3.7/site-packages/pip (python 3.7)
```

### 6. On EC2 terminal: Install git
` sudo yum -y install git `

### 7. On EC2 terminal: Create virtual environment
```commandline
python3 -m pip install virtualenv

python3 -m virtualenv fastapi

source fastapi/bin/activate


```
### 8. On Windows/MacOS: copy files to EC2 instance
- Learn public ip from web console
- Open gitbash/cmd or MacOS terminal
```commandline
scp -r -i erkan-admin-demo-keypair.pem \
/d/egitim/verilen/vbo/bootcamp-vbo-mlops/13_deploy_fastapi_on_aws_ec2 \
ec2-user@3.68.87.115:
```

### or get existing repo
```
git clone https://github.com/erkansirin78/fastapi-advertising-prediction.git

cd fastapi-advertising-prediction/

cd src/

cd fastapi_advertising_prediction/

pip install -r requirements.txt 
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 9. On EC2 terminal: Install requirements
```commandline
python3 -m pip install -r 13_deploy_fastapi_on_aws_ec2/requirements.txt
```

### 10. On EC2 terminal: Run uvicorn
```commandline
(fastapi) [ec2-user@ip-172-31-12-244 ~]$ cd 13_deploy_fastapi_on_aws_ec2/

(fastapi) [ec2-user@ip-172-31-12-244 13_deploy_fastapi_on_aws_ec2]$ ll
total 28
drwxr-xr-x 3 ec2-user ec2-user   99 Apr 18 19:54 aws
-rw-r--r-- 1 ec2-user ec2-user  221 Apr 18 19:54 Dockerfile
-rw-r--r-- 1 ec2-user ec2-user 2045 Apr 18 19:54 main.py
-rw-r--r-- 1 ec2-user ec2-user  806 Apr 18 19:54 README.md
-rw-r--r-- 1 ec2-user ec2-user   61 Apr 18 19:54 requirements.txt
drwxr-xr-x 2 ec2-user ec2-user  119 Apr 18 19:54 saved_models
-rw-r--r-- 1 ec2-user ec2-user  702 Apr 18 19:54 schemas.py
-rw-r--r-- 1 ec2-user ec2-user 1207 Apr 18 19:54 train_advertising_model.py
-rw-r--r-- 1 ec2-user ec2-user 1710 Apr 18 19:54 train_iris_model.py
```
```commandline
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 11. Copy public ip
![Copy public ip](images/17_copy_public_ip.png 'Copy public ip')

----------------------------------------------------------------------------

### 12. Open browser and reach fastapi docs
![reach fastapi docs](images/18_reach_fastapi_docs_on_browser.png 'reach fastapi docs')

----------------------------------------------------------------------------


## 13. Don't forget to terminate your machine!!!
![terminate your machine](images/22_terminate_instance.png 'terminate your machine')


## 14. Repeat same with user data
```commandline
sudo yum -y update
sudo yum -y install git
python3 -m pip install virtualenv
python3 -m virtualenv fastapi
source fastapi/bin/activate
git clone https://github.com/erkansirin78/fastapi-advertising-prediction.git
cd fastapi-advertising-prediction/fastapi_advertising_prediction/
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
