from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Aquí usamos SQLite, pero cambiar a PostgreSQL es solo cambiar esta URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./geostats.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()