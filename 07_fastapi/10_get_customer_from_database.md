## Get all customers
- mall.main.py
```
# Get all customers
@app.get("/customers")
async def get_all(session: Session = Depends(get_db)):
    customers = session.exec(
        select(Customer)).all()
    return customers
```
- Enter a few more customers via @app.post("/customers")

- http://127.0.0.1:8002/docs

## Get particular customer
```
# Get customer by id
@app.get("/customers/{id}")
async def get_by_id(id: int, session: Session = Depends(get_db)):
    with session:
        customer_here = session.get(Customer, id)
        if not customer_here:
            return f"Customer with id: {id} has not found."
        return customer_here
```

- http://127.0.0.1:8002/docs


## For more querying db
- https://sqlmodel.tiangolo.com/tutorial/select/


