## Define a table  according to data 
- https://raw.githubusercontent.com/erkansirin78/datasets/master/Mall_Customers.csv 

### In mall package create models.py
```
from sqlmodel import SQLModel, Field
from typing import Optional


class Customer(SQLModel, table=True):
    CustomerID: Optional[int] = Field(default=None, primary_key=True)
    Gender: str
    Age: Optional[int]
    AnnualIncome: float
    SpendingScore: int
```

## How to execute create table command?
- main.py
```
from fastapi import FastAPI
from mall.schemas import Customer
from mall.database import create_db_and_tables 

app = FastAPI()

# Creates all tables
create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/customers/{id}")
async def get_customer(id: int):
    return {"data": f"Customer id : {id}"}


@app.post("/customers")
async def create_customer(customer: Customer):
    return {"data": f"Customer {customer.CustomerID} is created."}
```

## Run uvicorn if it is not.

## DBeaver/psql
- See the table is created.
```
 docker exec -it postgresql psql -U train -d traindb

traindb=> \dt
         List of relations
 Schema |   Name    | Type  | Owner
--------+-----------+-------+-------
 public | customers | table | train
(1 row)

```
