## Create routers package

## routers/customer.py
- Move customer paths to routers/customer.py
```commandline
from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from mall.models import Customer, CustomerCreateUpdate, ShowCustomer

router = APIRouter()

# Create new customer
@router.post("/customers")
async def create_customer(request: CustomerCreateUpdate, session: Session = Depends(get_db)):
    new_customer = Customer(
        Gender = request.Gender,
        Age = request.Age,
        AnnualIncome = request.AnnualIncome,
        SpendingScore = request.SpendingScore
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


# Get customer by id
@router.get("/customers/{id}", status_code=status.HTTP_200_OK, response_model=ShowCustomer)
async def get_by_id(id: int, session: Session = Depends(get_db)):
    with session:
        customer_here = session.get(Customer, id)
        if not customer_here:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer id: {id} is not found.")
        return customer_here


# Delete customer by id
@router.delete("/customers/{id}", status_code=status.HTTP_200_OK)
async def get_by_id(id: int, session: Session = Depends(get_db)):
    with session:
        customer_here = session.get(Customer, id)
        if not customer_here:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer id: {id} is not found.")
        session.delete(customer_here)
        session.commit()
        return {"ok": True}


# Update customer
@router.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_customer(id: int, request: CustomerCreateUpdate, session: Session = Depends(get_db)):
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

## main.py
```
from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlmodel import Session, select
from mall.models import Customer, CustomerCreateUpdate, ShowCustomer
from mall.database import create_db_and_tables, get_db

app = FastAPI()

# Create all tables
create_db_and_tables()

app.include_router(mall.customer.router)

# Creates all the tables defined in models module
models.Base.metadata.create_all(bind=engine)
```

## Move get_db() from main to database