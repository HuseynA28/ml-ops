## mall.database.py 
- Add get_db function
```commandline
import os
from dotenv import load_dotenv
from sqlmodel import Session
from sqlmodel import create_engine, SQLModel

load_dotenv()  # take environment variables from .env.
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
```
## mall.models.py
```commandline
from sqlmodel import SQLModel, Field
from typing import Optional


class Customer(SQLModel, table=True):
    CustomerID: Optional[int] = Field(default=None, primary_key=True)
    Gender: str
    Age: Optional[int]
    AnnualIncome: float
    SpendingScore: int


class CreateUpdateCustomer(SQLModel):
    Gender: str
    Age: Optional[int]
    AnnualIncome: float
    SpendingScore: int
```
## mall.main.py
- Modify @app.post("/customers") endpoint to store a customer to postgres.
```commandline
from fastapi import FastAPI, Depends
from fastapi import status
from sqlmodel import Session, select
from mall.schemas import Customer, CreateUpdateCustomer
from mall.database import engine, get_db

app = FastAPI()


# Create Database and Tables on startup
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Create new customer
@app.post("/customers")
async def create_customer(request: CreateUpdateCustomer, session: Session = Depends(get_db)):
    new_customer = Customer(
        Gender=request.Gender,
        Age=request.Age,
        AnnualIncome=request.AnnualIncome,
        SpendingScore=request.SpendingScore
    )
    with session:
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return new_customer
```

## http://127.0.0.1:8002/docs#

- Enter a record from this dataset  
https://github.com/erkansirin78/datasets/blob/master/Mall_Customers.csv

- An example
```
CustomerID,Gender,Age,AnnualIncome,SpendingScore
1,Male,19,15000,39
```
- Request body
```
"Gender": "Male",
"Age": 19,
"AnnualIncome": 15000,
"SpendingScore": 39
```
## DBeaver/psql
```
traindb=# select * from customers;
 CustomerID | Gender | Age | AnnualIncome | SpendingScore
------------+--------+-----+--------------+---------------
          1 | Male   |  19 |        15000 |            39
(1 row)
```

- Status Code 201 Created - The most fitting for Create operations. This code should signal backend-side resource creation and come along with a Location header that defines the most specific URL for that newly created resource. It’s also a good idea to include appropriate representation of the resource or at least one or more URLs to that resource in the response body.

