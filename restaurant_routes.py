from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Restaurant, Menu
from schemas import RestaurantModel, MenuModel
from fastapi.encoders import jsonable_encoder

restaurant_router = APIRouter(
    prefix="/restaurants",
    tags=['restaurants']
)

@restaurant_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: RestaurantModel, db: Session = Depends(get_db)):
    new_restaurant = Restaurant(
        name=restaurant.name,
        location=restaurant.location,
        description=restaurant.description
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return jsonable_encoder(new_restaurant)

@restaurant_router.get('/list', status_code=status.HTTP_200_OK)
async def list_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(Restaurant).all()
    return jsonable_encoder(restaurants)

@restaurant_router.get('/{restaurant_id}', status_code=status.HTTP_200_OK)
async def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    return jsonable_encoder(restaurant)

@restaurant_router.post('/menu', status_code=status.HTTP_201_CREATED)
async def add_menu(menu: MenuModel, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == menu.restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    new_menu = Menu(
        name=menu.name,
        price=menu.price,
        description=menu.description,
        restaurant_id=menu.restaurant_id
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return jsonable_encoder(new_menu)

@restaurant_router.get('/{restaurant_id}/menus', status_code=status.HTTP_200_OK)
async def list_menus(restaurant_id: int, db: Session = Depends(get_db)):
    menus = db.query(Menu).filter(Menu.restaurant_id == restaurant_id).all()
    return jsonable_encoder(menus)
