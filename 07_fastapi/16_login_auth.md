- https://github.com/ianrufus/youtube/blob/main/fastapi-jwt-auth

## package/ auth.py
```commandline
from datetime import datetime, timedelta

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

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(self.security)):
        return self.decode_token(auth.credentials)


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


# Create Database and Tables on startup
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```
