## Response Code
- We use status codes in decorators.

- We can get help from ` from fastapi import status `  

- In main.py
```
from fastapi import status
...
...
@app.post("/customers", status_code=status.HTTP_201_CREATED)
...
...
```

- http://127.0.0.1:8002/docs#  

Add one more customer and see the status code is 201.

- We can assign custom response codes different from decorator.  
` response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR ` 


## Exception
- When we try to get non-existing customers API return null instead of exception.

- In main.py
```
from fastapi import Response, HTTPException
...
...
# Get customer by id
@app.get("/customers/{id}", status_code=status.HTTP_200_OK)
async def get_by_id(id: int, session: Session = Depends(get_db)):
    statement = select(Customer).where(Customer.CustomerID == id)
    results = session.exec(statement)
    try:
        one_customer = results.one()
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Customer {id} has not found.")
    return one_customer
```

## Browser
- http://127.0.0.1:8002/docs#/default/get_by_id_customers__id__get
- Try some existing and non-existing customer ids
- Example response of non-existing customer
```commandline
{
  "detail": "Customer 4 has not found."
}
```