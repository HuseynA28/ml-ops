- https://fastapi.tiangolo.com/tutorial/sql-databases/

## DB
FastAPI works with any database and any style of library to talk to the database supported by SQLAlchemy, like:

- PostgreSQL
- MySQL
- SQLite
- Oracle
- Microsoft SQL Server, etc.

## ORM
A common pattern is to use an "ORM": an "object-relational mapping" library.

An ORM has tools to convert ("map") between objects in code and database tables ("relations").

For example a class Pet could represent a SQL table pets.

And each instance object of that class represents a row in the database.

## Example FastAPI file structure with DB
```
.
└── mall
    ├── __init__.py
    ├── database.py
    ├── main.py
    ├── models.py
```

## SQLAlchemy ORM
- https://docs.sqlalchemy.org/en/14/orm/

## SQLModel
- https://sqlmodel.tiangolo.com/

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
- Open psql  
` docker exec -it postgresql psql -U postgres `
- Create and grant
```
create database traindb;
create user train with encrypted password 'Ankara06';
grant all privileges on database traindb to train;
```

- Port forwarding for 5433 -> 5433

## Add followings to requirements.txt
```
sqlmodel==0.0.8
psycopg2-binary==2.9.5
python-dotenv==0.21.0
```

## In root directory add .env 
```
SQLALCHEMY_DATABASE_URL="postgresql://train:Ankara06@localhost:5433/traindb"
```

## .gitignore
```
.env
```
### Attention
Since you added .env to .gitignore **don't forget to create .env in VM.**

## mall.database.py
```
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel

load_dotenv()  # take environment variables from .env.
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```
