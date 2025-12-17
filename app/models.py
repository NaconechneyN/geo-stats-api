from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    continent = Column(String, index=True)  # Ej: Africa, Europe
    capital = Column(String, nullable=True)
    population = Column(Integer)
    area_sq_km = Column(Float, nullable=True)
    region = Column(String) # Ej: South America
    
    # Dato curioso: Guardaremos la bandera (emoji o url) y un dato extra
    flag_emoji = Column(String, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String) # NUNCA se guarda una contraseña real