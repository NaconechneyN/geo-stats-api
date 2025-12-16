from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database, services, crud # Importamos los nuevos módulos

# Crear las tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Global GeoStats API", version="1.0.0")

@app.post("/etl/populate-db", status_code=201)
def populate_database(db: Session = Depends(database.get_db)):
    # 1. Verificar datos existentes
    if db.query(models.Country).count() > 0:
        return {"message": "La base de datos ya tiene información."}

    # 2. Usar SERVICE para obtener datos
    try:
        data = services.load_countries_data()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 3. Usar CRUD para guardar
    count = 0
    for item in data:
        try:
            crud.create_country(db, item)
            count += 1
        except:
            continue
    
    db.commit()
    return {"message": "Carga exitosa", "importados": count}

@app.get("/countries/", response_model=list[schemas.CountryResponse])
def read_countries(continent: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    countries = crud.get_countries(db, continent, skip, limit)
    
    # Lógica de presentación (densidad)
    for c in countries:
        c.population_density = round(c.population / c.area_sq_km, 2) if c.area_sq_km else 0
    return countries

@app.get("/stats/continent-summary")
def get_continent_stats(db: Session = Depends(database.get_db)):
    stats = crud.get_continent_stats(db)
    # Formateo de respuesta
    return [
        {
            "continent": s.continent,
            "countries_count": s.total_countries,
            "total_population": s.total_population,
            "average_area_sq_km": round(s.avg_area, 2) if s.avg_area else 0
        } for s in stats
    ]