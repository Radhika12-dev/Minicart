#Import necessary modules and classes from SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Define database URL and create an engine
DATABASE_URL = "sqlite:///./minicart.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#Create a session bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#All our database models will inherit from this base class
Base = declarative_base()