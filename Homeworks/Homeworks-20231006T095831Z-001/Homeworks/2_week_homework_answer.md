## 1. Start docker-compose
```
docker-compose up -d mysql
```

## 2.Create database, user
https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
```
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

## 9. Check mysql table 
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
```

## 10. Open browser




