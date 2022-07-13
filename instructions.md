# MeasurementDataStreamer


## Instructions


### RaspberryPi & Arduino


#### Arduino
- connect Arduino to Raspi
- run [temperature_co2_json.ino](https://github.com/patrickhaetti/MeasurementDataStreamer/blob/main/arduino_files/temperature_co2_json/temperature_co2_json.ino)

- check ip

- Ǹow stream data from Arduino with Python to Influx DB: 
    go to folder /stream_data and run ```python arduino_to_influxdb.py```


#### Grafana
- open in Browser http://<ip from streaming machine>:3000
- username + password is 'admin'
- in Dashboards chose DataSource (name given from setting up)
- From -> select Measurement. This is "measurement":"Co2&Temperature with Arduino" from python file
- Select: this are "fields": {...} from Python file
