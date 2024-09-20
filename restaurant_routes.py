from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Restaurant, Menu
from schemas import RestaurantModel, MenuModel
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import joinedload

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


# @restaurant_router.get('/search/', status_code=status.HTTP_200_OK)
# async def search_restaurants(name: Optional[str] = None, location: Optional[str] = None, db: Session = Depends(get_db)):
#     query = db.query(Restaurant)
#     if name:
#         query = query.filter(Restaurant.name.ilike(f"%{name}%"))
#     if location:
#         query = query.filter(Restaurant.location.ilike(f"%{location}%"))
#     results = query.all()
#     return jsonable_encoder(results)
@restaurant_router.get('/search/', status_code=status.HTTP_200_OK)
async def search_restaurants(
    name: Optional[str] = None, 
    location: Optional[str] = None, 
    description: Optional[str] = None,  # New parameter for restaurant description
    menu_name: Optional[str] = None,    # New parameter for menu name
    min_menu_price: Optional[int] = None,  # New parameter for minimum menu price
    max_menu_price: Optional[int] = None,  # New parameter for maximum menu price
    db: Session = Depends(get_db)
):
    # Base query for restaurants
    query = db.query(Restaurant).options(joinedload(Restaurant.menus))

    # Apply filters for Restaurant model fields
    if name:
        query = query.filter(Restaurant.name.ilike(f"%{name}%"))
    if location:
        query = query.filter(Restaurant.location.ilike(f"%{location}%"))
    if description:
        query = query.filter(Restaurant.description.ilike(f"%{description}%"))

    # Apply filters for related Menu model fields
    if menu_name or min_menu_price or max_menu_price:
        # Join with the Menu model to apply menu-related filters
        query = query.join(Restaurant.menus)

        # Filtering based on menu name
        if menu_name:
            query = query.filter(Menu.name.ilike(f"%{menu_name}%"))

        # Filtering based on menu price range
        if min_menu_price is not None:
            query = query.filter(Menu.price >= min_menu_price)
        if max_menu_price is not None:
            query = query.filter(Menu.price <= max_menu_price)

    # Retrieve all matching results
    results = query.all()

    # Return JSON-encoded results
    return jsonable_encoder(results)
