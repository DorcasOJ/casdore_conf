import sqlalchemy
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import create_engine 
import databases

DATABASE_URL = "sqlite:///./food.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

Food = Table('Food', metadata, Column('id', Integer, primary_key = True),\
    Column('food_name', String), Column('description', String), \
        Column('price', Integer), Column('quantity_available', Integer),)


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)