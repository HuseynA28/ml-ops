## 1. Start docker-compose
```
cd mlflow

docker-compose up -d

# Close unnecessary containers
docker-compose stop prod test jenkins mlflow minio 
```

## 2.Create database, user
https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
```
# Connect mysql container 
docker exec -it mlflow_db mysql -u root -p

# Create database 
mysql> create database mlops;

# Show databases
mysql> show databases;

# Create user 
mysql> CREATE USER 'mlops_user'@'%' IDENTIFIED BY 'Ankara06';

# See users
mysql> select user, host from mysql.user;

# Grand mlops_user on mlops database 
mysql> GRANT ALL PRIVILEGES ON mlops.* TO 'mlops_user'@'%' WITH GRANT OPTION;

mysql> FLUSH PRIVILEGES;

mysql> exit
```

## 3. Test connection 
```
docker exec -it mlflow_db mysql -u mlops_user -D mlops -p
Enter password: Ankara06

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mlops              |
+--------------------+
2 rows in set (0.00 sec)

mysql> exit
```

## 4. Develop the App

## 5. Copy/Push App to VM 

## 6. Activate conda environment

## 7. Install requirements

## 8. Run uvicorn 
```commandline
uvicorn main:app \
--host 0.0.0.0 \
--port 8002 \
--reload
```
## 9. Check customers table in mysql 
```
(base) [train@localhost ~]$ docker exec -it mlflow_db mysql -u mlops_user -D mlops -p
Enter password: Ankara06

mysql> use mlops;
Database changed

mysql> show tables;
+-----------------+
| Tables_in_mlops |
+-----------------+
| customers       |
+-----------------+
1 row in set (0.00 sec)

mysql> select * from customers;
Empty set (0.00 sec)

mysql> describe customers;
+------------------+--------------+------+-----+---------+----------------+
| Field            | Type         | Null | Key | Default | Extra          |
+------------------+--------------+------+-----+---------+----------------+
| customerId       | int          | NO   | PRI | NULL    | auto_increment |
| customerFName    | varchar(50)  | YES  |     | NULL    |                |
| customerLName    | varchar(50)  | YES  |     | NULL    |                |
| customerEmail    | varchar(50)  | YES  |     | NULL    |                |
| customerPassword | varchar(255) | YES  |     | NULL    |                |
| customerStreet   | varchar(100) | YES  |     | NULL    |                |
| customerCity     | varchar(20)  | YES  |     | NULL    |                |
| customerState    | varchar(5)   | YES  |     | NULL    |                |
| customerZipcode  | varchar(10)  | YES  |     | NULL    |                |
+------------------+--------------+------+-----+---------+----------------+
9 rows in set (0.01 sec)

mysql> exit
```
## 10. Check port forwarding

## 11. Open browser
http://localhost:8002/docs






