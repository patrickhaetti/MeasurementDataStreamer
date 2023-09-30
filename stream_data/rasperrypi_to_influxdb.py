import ccs811LIBRARY
import time
import sys
from influxdb import InfluxDBClient
from datetime import datetime

# InfluxDB settings
HOST = 'localhost'
PORT = 8086
DB_NAME = 'measurestream'
client = InfluxDBClient(host=HOST, port=PORT)
client.switch_database(DB_NAME)

# Initialize the CCS811 sensor
sensor = ccs811LIBRARY.CCS811()

def setup(mode=1):
    print('Starting CCS811 Read')
    sensor.configure_ccs811()
    sensor.set_drive_mode(mode)

    if sensor.check_for_error():
        sensor.print_error()
        raise ValueError('Error at setDriveMode.')

    result = sensor.get_base_line()
    sys.stdout.write("baseline for this sensor: 0x")
    if result < 0x100:
        sys.stdout.write('0')
    if result < 0x10:
        sys.stdout.write('0')
    sys.stdout.write(str(result) + "\n")

def log_error_to_file(error_message):
    with open("logs.txt", "a") as log_file:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{current_time}: {error_message}\n")

setup(1)  # Setting mode

while True:
    try:
        if sensor.data_available():
            sensor.read_logorithm_results()
            print("eCO2[%d] TVOC[%d]" % (sensor.CO2, sensor.tVOC))
            
            # Prepare data for InfluxDB
            json_body = [
                {
                    "measurement": "air_quality",
                    "tags": {
                        "location": "living_room"  # You can add more tags if needed
                    },
                    "fields": {
                        "eCO2": sensor.CO2,
                        "TVOC": sensor.tVOC
                    }
                }
            ]
            
            # Send data to InfluxDB
            client.write_points(json_body)
            
        elif sensor.check_for_error():
            sensor.print_error()
            
    except Exception as e:
        print(f"Error occurred: {e}")
        log_error_to_file(str(e))

    time.sleep(1)
