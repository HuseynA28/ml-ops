- https://github.com/ianrufus/youtube/blob/main/fastapi-jwt-auth

## package/ auth.py
```commandline
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from mall.database import get_session
from mall.models import CreateUpdateCustomer, Customer, ShowCustomer

router = APIRouter()

# Create new customer
@router.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(request: CreateUpdateCustomer, session: Session = Depends(get_session)):
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


# Get customer by id
@router.get("/customers/{id}", response_model=ShowCustomer)
async def get_by_id(id: int, session: Session = Depends(get_session)):
    with session:
        customer_here = session.get(Customer, id)
        if not customer_here:
            raise HTTPException(status_code=404, detail=f"Customer with id: {id} has not found.")
        return customer_here


# Delete a customer by id
@router.delete("/customer/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, session: Session = Depends(get_session)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        session.delete(one_customer)
        session.commit()
        return {"ok": True}


# Update customer
@router.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer(id: int, request: CreateUpdateCustomer, session: Session = Depends(get_session)):
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
...
...
class Login(SQLModel):
    username: str
    password: str
    
```

## Add routers/user.py
```commandline
from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from sqlmodel import Session, select
from mall.database import get_session
from mall.models import ShowUser, User, CreateUpdateUser, Login
from mall.auth import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()


# Create user
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ShowUser)
async def create_user(request: CreateUpdateUser, session: Session = Depends(get_session)):
    hashed_password = auth_handler.get_password_hash(request.password)
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
def login(request: Login, session: Session = Depends(get_session)):
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
from sqlmodel import SQLModel
from mall.database import engine
from mall.routers import user, customer
from fastapi import FastAPI


app = FastAPI()

app.include_router(user.router)
app.include_router(customer.router)


# Create Database and Tables on startup
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```