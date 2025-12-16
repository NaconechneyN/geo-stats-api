import json
import os

def load_countries_data(file_path: str = "countries.json"):
    """
    Servicio encargado de la lógica de extracción de datos (ETL).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo '{file_path}'.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Error leyendo el JSON: {str(e)}")