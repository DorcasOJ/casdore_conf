from fastapi import FastAPI, Request
import uvicorn
from pydantic import BaseModel
from typing import List, Optional, Dict
import sqlalchemy
from sqlalchemy import update
from database import *
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


metadata.create_all(engine)


class FoodIn(BaseModel):
    food_name: str 
    description: str
    price: int
    quantity_available: int

class FoodOut(BaseModel):
    food_name: str 
    description: str
    price: int
    quantity_available: int
    id: int

class FoodUpdate(BaseModel):
    food_name: str
    description: str = None
    price: int = None
    quantity_available: int = None

class FoodDelete(BaseModel):
    row1: int = None
    row2: int = None
    row3: int = None

app = FastAPI()


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


#read database
@app.get('/getfood/', response_model= List[FoodOut])
async def read_db():
    query = Food.select()
    return await database.fetch_all(query)


@app.post('/postfood/', response_model= FoodOut)
async def create_db(food: FoodIn):
    query = Food.insert().values(food_name = food.food_name, description = food.description,\
         price = food.price, quantity_available =  food.quantity_available )
    last_record_id = await database.execute(query)
    return  {**food.dict(), 'id': last_record_id}


@app.post('/updatefood/')
async def update_db(food_update: FoodUpdate):
    if food_update:
        query = Food.update().\
            where(Food.c.food_name == food_update.food_name).\
                values(price = food_update.price, \
                    description = food_update.description, \
                        quantity_available = food_update.quantity_available)
        update_db = await database.execute(query)
        return 'Sucessful!'


@app.post('/deletefood/')
async def delete_row(food_rows: FoodDelete):
    if food_rows.row1:  
        query1 = Food.delete().where(Food.c.id == food_rows.row1)
        delete_db = await database.execute(query1)
    if food_rows.row2:
        query2 = Food.delete().where(Food.c.id == food_rows.row2)
        delete_db = await database.execute(query2)
    if food_rows.row3:
        query3 = Food.delete().where(Food.c.id == food_rows.row3)
        delete_db = await database.execute(query3)
    return 'The rows has been deleted successfully'
