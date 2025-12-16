from pydantic import BaseModel
from typing import Optional

# Base común
class CountryBase(BaseModel):
    name: str
    continent: str
    capital: Optional[str] = None
    population: int
    area_sq_km: Optional[float] = None
    region: str
    flag_emoji: Optional[str] = None

# Para crear (Input)
class CountryCreate(CountryBase):
    pass

# Para leer (Output - agregamos el ID y una propiedad calculada)
class CountryResponse(CountryBase):
    id: int
    population_density: Optional[float] = None  # Calcularemos esto al vuelo

    class Config:
        from_attributes = True # Antes conocido como orm_mode