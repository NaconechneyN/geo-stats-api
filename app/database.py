import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv # <--- Import nuevo

# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Leer la variable. Si no existe, lanza error o usa un default (pero mejor no usar default en prod)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Validación de seguridad:
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("FATAL: La variable DATABASE_URL no está configurada en el archivo .env")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()