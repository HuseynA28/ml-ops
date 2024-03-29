## Create PostgreSQL DB, User and Privileges
- Open vm/docker
- Start postgresql
```
docker run --rm -d \
--name postgresql \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=Ankara06 \
-e PGDATA=/var/lib/postgresql/data/pgdata \
-p 5433:5432 \
-v postgresql13_v:/var/lib/postgresql/data \
postgres:13
```

### Create database, user and give privileges
#### Open psql  
` docker exec -it postgresql psql -U postgres `

#### Create and grant
```
create database traindb;
create user train with encrypted password 'Ankara06';
grant all privileges on database traindb to train;
```

- Port forwarding for 5433 -> 5433

## Activate ds-dev and install requirements.txt