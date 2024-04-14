- https://github.com/ianrufus/youtube/blob/main/fastapi-jwt-auth

## package/ auth.py
```commandline
om datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
```
###  customer.py
```
from typing import List, Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from mall.models import Customer, CreateUpdateCustomer, ShowCustomer
from database import get_db



router=APIRouter()
@router.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(request:CreateUpdateCustomer, session: Session = Depends(get_db)):
    new_customer=Customer(
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

# Get all customers
@router.get("/customers", response_model=List[ShowCustomer])
async def get_all(session: Session = Depends(get_db)):
    customers = session.exec(select(Customer)).all()
    return customers

@router.get("/customer/{id}", status_code=status.HTTP_200_OK, response_model=ShowCustomer)
async def get_by_id(id: Optional[int],session: Session=Depends(get_db)):
    with session:
        customer_here =session.get(Customer ,id)
        if not customer_here:
            return f'Customer is not found'
    return customer_here


# Delete a customer by id
@router.delete("/customer/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, session: Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        session.delete(one_customer)
        session.commit()
        return {"ok": True}


@router.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer(id: int, request: CreateUpdateCustomer, session: Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(one_customer, key, value)
        session.add(one_customer)
        session.commit()
        session.refresh(one_customer)
        return one_customer
```


## models.py
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
    Gender :str
    Age:Optional[int]
    AnnualIncome:float
    SpendingScore:int
class ShowCustomer(SQLModel):
    CustomerID: int
    Gender: str
    Age: Optional[int]

class Login(SQLModel):

    username: str
    password: str

class ShowUser(SQLModel):
    name: str
    email: str
    
```

## Add routers/user.py
```commandline
from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from sqlmodel import Session, select
from mall.database import get_db
from mall.models import ShowUser, ShowUser, CreateUpdateCustomer, Login

from mall.rounters import auth

router = APIRouter()
auth_handler = auth.AuthHandler()


# Create user
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(request: CreateUpdateCustomer, session: Session = Depends(get_db)):
    hashed_password = auth_handler.get_password_hash(request.password)
    from sqlalchemy.testing.pickleable import User
    new_user = User(
        name=request.name,
        username=request.username,
        email=request.email,
        password=hashed_password
    )
    with session:
        statement = select(User).where(User.username == new_user.username)
        results = session.exec(statement)
        one_user = results.first()
        if not one_user:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        else:
            raise HTTPException(status_code=400, detail=f'Username: {one_user.username} is taken')



@router.post('/login')
def login(request: Login, session: Session = Depends(get_db)):
    with session:
        statement = select(User).where(User.username == request.username)
        results = session.exec(statement)
        one_user = results.first()
        if (one_user is None) or (not auth_handler.verify_password(request.password, one_user.password)):
            raise HTTPException(status_code=401, detail='Invalid username and/or password')
        token = auth_handler.encode_token(one_user.username)
        return {'token': token}


@router.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}
```

## main.py
```commandline
from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlmodel import Session, select

from mall import models
from mall.models import Customer, CreateUpdateCustomer, ShowCustomer
from mall.database import create_db_and_tables, get_db, engine
from mall.rounters import customer

from sqlmodel import SQLModel
from database import engine
from mall.rounters import user, customer
from fastapi import FastAPI


app = FastAPI()

app.include_router(user.router)
app.include_router(customer.router)


# Create Database and Tables on startup
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

## database.py
```commandline
import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel, Session

load_dotenv()  # take environment variables from .env.
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    db=Session(engine)
    try:
        yield db
    finally:
        db.close()
```
