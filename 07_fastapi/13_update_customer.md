## UpdateCustomer to schemas.py
```commandline
class UpdateCustomer(SQLModel):
    Gender: str
    Age: Optional[int]
    AnnualIncome: float
    SpendingScore: int
```

## New endpoint main.py
```
from mall.schemas import Customer, UpdateCustomer
...
...
# Update customer
@app.put("/customer/{id}", status_code=status.HTTP_202_ACCEPTED)
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

- Note: 202 Accepted - If the update is done asynchronous, this code can be used. 