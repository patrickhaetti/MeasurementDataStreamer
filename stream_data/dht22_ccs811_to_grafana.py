import time
import sys
from datetime import datetime
import adafruit_dht
import board
import busio
import adafruit_ccs811
from influxdb import InfluxDBClient
import urllib3
import json

# InfluxDB settings
HOST = 'localhost'
PORT = 8086
DB_NAME = 'newmeasurementdatabase'
client = InfluxDBClient(host=HOST, port=PORT)
client.switch_database(DB_NAME)

# Initialize sensors
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ccs811.CCS811(i2c)
dht_device = adafruit_dht.DHT22(board.D4)

def log_error_to_file(error_message):
    with open("logs.txt", "a") as log_file:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{current_time}: {error_message}\n")

def fetch_weather():
    http = urllib3.PoolManager()
    url = "https://api.openweathermap.org/data/2.5/weather?lat=52.48470&lon=13.43063&appid=f0134317d5bd1033e3d67a1f5184549f&units=metric"
    try:
        response = http.request("GET", url)
        if response.status == 200:
            weather_data = json.loads(response.data.decode('utf-8'))
            temperature_api = weather_data["main"]["temp"]
            humidity_api = weather_data["main"]["humidity"]
            return [temperature_api, humidity_api]
        else:
            print("HTTP error occurred: Status", response.status)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

while True:
    try:
        temperature_c = None
        humidity = None

        # Try to read from DHT22
        try:
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
        except RuntimeError as err:
            print(f"Error reading DHT22: {err.args[0]}")

        # Fetch weather data from API
        weather_data = fetch_weather()
        if weather_data is not None:
            temperature_api, humidity_api = weather_data

        if sensor.data_ready:
            print(f"eCO2: {sensor.eco2} PPM, TVOC: {sensor.tvoc} PPB, Temp: {temperature_c} C, Humidity: {humidity}%")

            # Prepare data for InfluxDB
            json_body = [
                {
                    "measurement": "air_quality",
                    "tags": {
                        "location": "living_room"
                    },
                    "fields": {
                        "eCO2": sensor.eco2,
                        "TVOC": sensor.tvoc,
                        "temperature": temperature_c if temperature_c is not None else float('nan'),
                        "humidity": humidity if humidity is not None else float('nan'),
                        "api_temperature": temperature_api if weather_data is not None else float('nan'),
                        "api_humidity": humidity_api if weather_data is not None else float('nan')
                    }
                }
            ]
            client.write_points(json_body)

    except Exception as e:
        print(f"Error occurred: {e}")
        log_error_to_file(str(e))

    time.sleep(1)
