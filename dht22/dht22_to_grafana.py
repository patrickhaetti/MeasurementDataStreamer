"""
+ Measuring with dht22 and displaying data in console
+ Sending data to with InfluxDB and Telegraf to Grafana 
+ In Grafana Data can be selected in 
    - FROM <add measurement> by seleting "environment"
    - SELECT field <temperature_c / temperature_f / humidity>
data = [
            {
                "measurement": "environment",
                "time": current_time,
                "fields": {
                    "temperature_c": float(temperature_c),
                    "temperature_f": float(temperature_f),
                    "humidity": float(humidity)
                }
            }
"""


import time
import board
import adafruit_dht
from influxdb import InfluxDBClient
from datetime import datetime

# InfluxDB settings
HOST = 'localhost'
PORT = 8086
DB_NAME = 'newmeasurementdatabase'

# Initialize the DHT22 sensor
dht_device = adafruit_dht.DHT22(board.D4)

# Setup InfluxDB client
client = InfluxDBClient(host=HOST, port=PORT)
client.switch_database(DB_NAME)

while True:
    try:
        # Read temperature in Celsius and Fahrenheit
        temperature_c = dht_device.temperature
        temperature_f = temperature_c * (9 / 5) + 32

        # Read humidity
        humidity = dht_device.humidity

        # Print the readings
        print("Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(temperature_c, temperature_f, humidity))

        # Prepare data for InfluxDB
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = [
            {
                "measurement": "environment",
                "time": current_time,
                "fields": {
                    "temperature_c": float(temperature_c),
                    "temperature_f": float(temperature_f),
                    "humidity": float(humidity)
                }
            }
        ]

        # Write data to InfluxDB
        client.write_points(data)

    except RuntimeError as err:
        print(err.args[0])
    except Exception as e:
        print("Failed to write to InfluxDB", e)

    time.sleep(2.0)
