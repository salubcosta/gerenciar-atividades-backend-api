from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DB_DIRECTORY = "data/"
DB_CONNECTION_STRING = f"sqlite:///{DB_DIRECTORY}/data.db"

if not os.path.exists(DB_DIRECTORY):
    os.makedirs(DB_DIRECTORY)

engine = create_engine(DB_CONNECTION_STRING)

Session = sessionmaker(bind=engine)

Base = declarative_base()