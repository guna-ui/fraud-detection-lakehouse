from decimal import Decimal
from pydantic import BaseModel, Field,IPvAnyAddress,AwareDatetime,field_validator
from typing import Literal
from uuid import UUID



class Merchant(BaseModel):
    merchant_id:str=Field(min_length=1)
    category:str
    city:str
    country:str=Field(min_length=2,max_length=2)
    @field_validator('country')
    @classmethod
    def county_validator(cls,country:str):
        if not country.isupper():
            raise ValueError("Must be uppercase")
        return country

class Device(BaseModel):
    ip_address:IPvAnyAddress
    device_id:UUID

class Location(BaseModel):
    latitude:float=Field(ge=-90.0,le=90.0)
    longitude:float=Field(ge=-180.0,le=180.0)

class Transaction(BaseModel):
    transaction_id:UUID
    user_id:str=Field(min_length=1)
    event_timestamp:AwareDatetime
    merchant:Merchant
    device:Device
    amount:Decimal=Field(gt=0)
    currency:Literal['INR', 'USD', 'EUR', 'GBP']
    location:Location
    channel:str
    action:str