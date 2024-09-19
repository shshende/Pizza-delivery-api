from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]


    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "username":"johndoe",
                "email":"johndoe@gmail.com",
                "password":"password",
                "is_staff":False,
                "is_active":True
            }
        }



class Settings(BaseModel):
    authjwt_secret_key:str='b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02d5c45b2fa7b86341fa405'


class LoginModel(BaseModel):
    username:str
    password:str



class OrderModel(BaseModel):
    id:Optional[int]
    quantity:int
    order_status:Optional[str]="PENDING"
    pizza_size:Optional[str]="SMALL"
    user_id:Optional[int]


    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":2,
                "pizza_size":"LARGE"
            }
        }


class OrderStatusModel(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }


class RestaurantModel(BaseModel):
    id: Optional[int]
    name: str
    location: str
    description: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Pizza Palace",
                "location": "1234 Elm Street",
                "description": "Best pizzas in town."
            }
        }

class MenuModel(BaseModel):
    id: Optional[int]
    name: str
    price: int
    description: Optional[str]
    restaurant_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Margherita Pizza",
                "price": 15,
                "description": "Classic Margherita pizza with fresh tomatoes, mozzarella, and basil.",
                "restaurant_id": 1
            }
        }
