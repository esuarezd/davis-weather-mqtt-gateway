import os
import time
import yaml
from app.reader_vantagepro2 import read_weather_data
from app.mqtt_client import publish_data

def load_config(config_path="config.yaml"):
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    # Cargar configuración
    config = load_config()

    # Obtener nombre de la estación y ruta al archivo generado por WeatherLink
    station_name = config["station"]["name"]
    file_path = os.path.join("C:\\WeatherLink", station_name, "download.txt")

    # Leer intervalo de archivo (en minutos) y convertir a segundos para el sleep
    archive_interval_min = config["station"].get("archive_interval_min", 5)
    archive_interval_sec = archive_interval_min * 60

    # Configuración de MQTT
    mqtt_config = config["mqtt"]

    print(f"[INFO] Iniciando publicación de datos para estación {station_name}")
    print(f"[INFO] Archivo fuente: {file_path}")
    print(f"[INFO] Intervalo de lectura: {archive_interval_min} minutos")

    while True:
        try:
            data = read_weather_data(file_path)
            publish_data(data, mqtt_config)
            print(f"[OK] Datos publicados: {data}")
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(archive_interval_sec)
