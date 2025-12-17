# 🌍 Global GeoStats API

API REST de alto rendimiento construida con **FastAPI** y **SQLAlchemy**. Diseñada para ingerir datos geográficos, procesarlos y permitir análisis estadísticos complejos mediante consultas SQL optimizadas.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)

## ⚡ Características Clave

*   **Arquitectura en Capas:** Separación limpia de responsabilidades (Routers, Controllers/CRUD, Services, Schemas).
*   **ETL Offline:** Módulo de ingesta de datos capaz de poblar la base de datos desde fuentes locales (JSON) o remotas.
*   **SQL Analytics:** Endpoints dedicados a cálculos estadísticos usando funciones de agregación (`GROUP BY`, `AVG`, `SUM`) directamente en la base de datos.
*   **Validación de Datos:** Esquemas robustos con **Pydantic**.

## 🛠 Instalación y Uso

1.  **Clonar y preparar entorno:**
    ```bash
    git clone https://github.com/NaconechneyN/geo-stats-api.git
    cd geo-stats-api
    python -m venv venv
    source venv/bin/activate  # o venv\Scripts\activate en Windows
    pip install -r requirements.txt
    ```

2.  **Ejecutar Servidor:**
    ```bash
    python -m uvicorn app.main:app --reload
    ```

3.  **Explorar Documentación:**
    Abre `http://127.0.0.1:8000/docs` para interactuar con Swagger UI.
    *   Ejecuta `POST /etl/populate-db` para cargar los datos iniciales.
    *   Ejecuta `GET /stats/continent-summary` para ver el análisis SQL.

---
**Autor:** [Nicolás Naconechney](https://naconechneyn.github.io/)