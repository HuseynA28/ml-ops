from sqlmodel import SQLModel, Field
from typing import Optional


class Customer(SQLModel, table=True):
    customerID: Optional[int] = Field(default=None, primary_key=True)
    customerFName: Optional[str] = Field(default=None)
    customerLName: Optional[str] = Field(default=None)
    customerEmail: Optional[str] = Field(default=None)
    customerPassword: Optional[str] = Field(default=None)
    customerStreet: Optional[str] = Field(default=None)
    customerCity: Optional[str] = Field(default=None)
    customerState: Optional[str] = Field(default=None)
    customerZipcode: Optional[str] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "customerId": 1,
                "customerFName": "Richard",
                "customerLName": "Hernandez",
                "customerEmail": "XXXXXXXXX",
                "customerPassword": "XXXXXXXXX",
                "customerStreet": "6303 Heather Plaza",
                "customerCity": "Brownsville",
                "customerState": "TX",
                "customerZipcode": "78521"
            }
        }


class CreateUpdateCustomer(SQLModel):
    customerFName: str
    customerLName: str
    customerEmail: str
    customerPassword: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str


class ShowCustomer(SQLModel):
    customerFName: str
    customerLName: str
    customerStreet: str
    customerCity: str
    customerState: str
    customerZipcode: str

    class Config():
        orm_mode = True
