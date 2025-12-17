from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, security, schemas

def get_country_by_name(db: Session, name: str):
    return db.query(models.Country).filter(models.Country.name == name).first()

def create_country(db: Session, country_data: dict):
    # Lógica de mapeo de JSON a Modelo SQL
    db_country = models.Country(
        name=country_data.get("name", {}).get("common", "Unknown"),
        continent=country_data.get("continents", ["Unknown"])[0],
        capital=country_data.get("capital", ["N/A"])[0],
        population=country_data.get("population", 0),
        area_sq_km=country_data.get("area", 0.0),
        region=country_data.get("region", "Unknown"),
        flag_emoji=country_data.get("flag", "")
    )
    db.add(db_country)
    return db_country

def get_countries(db: Session, continent: str = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Country)
    if continent:
        query = query.filter(models.Country.continent == continent)
    return query.offset(skip).limit(limit).all()

def get_continent_stats(db: Session):
    return db.query(
        models.Country.continent,
        func.count(models.Country.id).label("total_countries"),
        func.sum(models.Country.population).label("total_population"),
        func.avg(models.Country.area_sq_km).label("avg_area")
    ).group_by(models.Country.continent).all()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user    