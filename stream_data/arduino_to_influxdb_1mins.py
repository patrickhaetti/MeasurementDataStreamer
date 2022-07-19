from influxdb import InfluxDBClient
from datetime import datetime
import time
import serial
import json


ip  = '192.168.178.142'
port = 8086  # from influx db, must be also in grafana
username = 'admin'  # from influx
password = 'admin'  # from influx
database_name = 'telegraf'


client = InfluxDBClient(ip, port, username, password, database_name)
#client = InfluxDBClient('192.168.178.142', 8086, 'admin', 'admin', db_running)

client.create_database(database_name)
client.get_list_database()
client.switch_database(database_name)

# set up payload
json_payload = []

#print(client.write_points(json_payload))

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)   # connection to arduino
    ser.flush()
    
    while True:
               
        if ser.in_waiting > 0:
            #line = ser.readline().decode('utf-8').rstrip()
            line = ser.readline().rstrip()
            try:
                y = json.loads(line)
                data = {
                "measurement":"Co2&Temperature with Arduino",
                "tags": {
                    "ticker": "co2t"
                    },
                "time": datetime.now(),
                "fields": {
                    'CO2':y["CO2"],
                    'Temperature': y["Temperature"],
                    'TVOC': y["TVOC"]
                    }
                }
                json_payload.append(data)    

                client.write_points(json_payload)
            
                #print(line)
                print(data)
                time.sleep(60)
            except:
                print("Error, couldn't parse json")
                
