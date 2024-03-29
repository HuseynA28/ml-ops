- You can declare the model used for the response with the parameter response_model in any of the path operations.

- Notice that response_model is a parameter of the "decorator" method (get, post, etc). Not of your path operation function, like all the parameters and body.

- It receives the same type you would declare for a Pydantic model attribute, so, it can be a Pydantic model, but it can also be, e.g. a list of Pydantic models, like List[Item].

FastAPI will use this response_model to:

- Convert the output data to its type declaration.

- Validate the data.

- Add a JSON Schema for the response, in the OpenAPI path operation.

- Will be used by the automatic documentation systems.

But most importantly:

- Will limit the output data to that of the model. We'll see how that's important below.

## What if we don't want to see AnnualIncome and SpendingScore?
- For this we need to create a model (Pydantic) excluding CustomerID.

- And use this model as response model in decorator.


## mall.models.py
```
class ShowCustomer(SQLModel):
    CustomerID: int
    Gender: str
    Age: Optional[int]
```

## mall/main.py
- Just add  response_model=ShowCustomer
```
from mall.schemas import Customer, CreateUpdateCustomer, ShowCustomer
...
...
get("/customer/{id}", status_code=status.HTTP_200_OK, response_model=ShowCustomer)
...
...
```
- http://127.0.0.1:8001/docs

- See there is no AnnualIncome and SpendingScore in the result.
```commandline
{
  "CustomerID": 2,
  "Gender": "Female",
  "Age": 33
}
```

## Add same model to other endpoints
```
from typing import List
...
...
@app.get("/customers", response_model=List[ShowCustomer])
...
...
```

- http://127.0.0.1:8002/docs#/default/get_all_customers_get
```
[
  {
    "CustomerID": 2,
    "Gender": "Female",
    "Age": 33
  },
  {
    "CustomerID": 3,
    "Gender": "Male",
    "Age": 133
  }
]
```
