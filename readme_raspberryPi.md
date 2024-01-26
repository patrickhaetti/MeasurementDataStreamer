# MeasurementDataStreamer


## Instructions for setting up Grafana, InfluxDB and Telegraf on RaspberryPi



#### Arduino
- connect Arduino to RaspberryPi
- run [temperature_co2_json.ino](https://github.com/patrickhaetti/MeasurementDataStreamer/blob/main/arduino_files/temperature_co2_json/temperature_co2_json.ino)

- check ip

- Ǹow stream data from Arduino with Python to Influx DB: 
    go to folder /stream_data and run ```python arduino_to_influxdb.py```


#### Grafana
+ Installation Guide: [https://pimylifeup.com/raspberry-pi-influxdb/](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)
- open in Browser http://\<ip from streaming machine\>:3000
- username + password is 'admin'
- in Dashboards chose DataSource (name given from setting up)
- From -> select Measurement. This is "measurement":"Co2&Temperature with Arduino" from python file
- Select: this are "fields": {...} from Python file


#### InfluxDB
+ Installation Guide: https://pimylifeup.com/raspberry-pi-influxdb/
