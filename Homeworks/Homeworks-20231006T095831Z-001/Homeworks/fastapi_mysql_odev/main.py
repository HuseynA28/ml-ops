from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from passlib.context import CryptContext
from sqlmodel import Session, select, SQLModel

from database import engine, get_session
from schemas import Customer, ShowCustomer, CreateUpdateCustomer

app = FastAPI()


# Create Database and Tables on startup
@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# Get customer by id
@app.get("/customers/{id}", response_model=ShowCustomer)
async def get_by_id(id: int, session: Session = Depends(get_session)):
    with session:
        customer_here = session.get(Customer, id)
        if not customer_here:
            raise HTTPException(status_code=404, detail=f"Customer with id: {id} has not found.")
        return customer_here


# Get all customers
@app.get("/customers", response_model=List[ShowCustomer])
async def get_all(session: Session = Depends(get_session)):
    customers = session.exec(
        select(Customer)).all()
    return customers


# Create new customers
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/customers", status_code=status.HTTP_201_CREATED)
async def create_customer(request: CreateUpdateCustomer, session: Session = Depends(get_session)):
    new_customer = Customer(
        customerFName=request.customerFName,
        customerLName=request.customerLName,
        customerEmail=request.customerEmail,
        customerPassword=get_password_hash(request.customerPassword),
        customerStreet=request.customerStreet,
        customerCity=request.customerCity,
        customerState=request.customerState,
        customerZipcode=request.customerZipcode
    )

    with session:
        session.add(new_customer)
        session.commit()
        session.refresh(new_customer)
        return new_customer


# Delete a customer
@app.delete("/customer/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, session: Session = Depends(get_session)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        session.delete(one_customer)
        session.commit()
        return {"ok": True}


# Update a customer
@app.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
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
