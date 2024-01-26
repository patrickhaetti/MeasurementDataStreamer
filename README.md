# MeasurementDataStreamer
 * Instructions for setting up Grafana, InfluxDB and Telegraf on RaspberryPi
 * Database name in this case is "newmeasurementdatabase" 
 * Only for measuring with RaspberryPi, for RaspberryPi combined with Arduino see in info_files & arduino_files

<br><br>

### I. InfluxDB
+ Installation Guide: https://pimylifeup.com/raspberry-pi-influxdb/


#### After InfluxDB is installed

1. run
 ```bash
 influx
 ```

2. create DB
  ```bash
  CREATE DATABASE newmeasurementdatabase
  ```

2. use DB
  ```bashUSE 
  newmeasurementdatabase
  ```

<br><br><br>

### II. Telegraf (Telegraf will push measurement data to Influxdb)

```bash
sudo apt update
sudo apt install telegraf
```

#### configure influxDB config file

1)  ```bash
    nano /etc/telegraf/telegraf.conf
    ```
    * (a) go to [outputs.influxdb] and uncomment it
    * (b) add ip of raspi where grafana is also running on to urls=[x.x.x.x:8086]
    * (c) add username "admin" and password "admin"
    * (d) set database = "newmeasurementdatabase" # the one from influxDB

2) look if all is ok in influx config
    ```bash
    nano /etc/influxdb/influxdb.conf
    ```

3) Restart Services
    ```bash
    systemctl restart grafana-server
    ```
    ```bash
    systemctl restart influxdb
    ```
    ```bash
    systemctl restart telegraf
    ```
<br><br><br

### Grafana
+ Installation Guide: [https://pimylifeup.com/raspberry-pi-influxdb/](https://grafana.com/tutorials/install-grafana-on-raspberry-pi/)
- open in Browser http://\<ip from streaming machine\>:3000
- username + password is 'admin'
- in Dashboards chose DataSource (name given from setting up)

#### Datasource
    + add data source -> choose influxdb
    + url: ip of raspi:8086
    + db as set in influxdb + telegraf setup 1*d

+ Create new Dashboard. Data can be selected in 
    - FROM <add measurement> by seleting "environment"
    - SELECT field <temperature_c / temperature_f / humidity>
    - In the Python file dht22_to_grafana.py for example this structure is used
```json
data = [
            {
                "measurement": "environment",
                "time": current_time,
                "fields": {
                    "temperature_c": float(temperature_c),
                    "temperature_f": float(temperature_f),
                    "humidity": float(humidity)
                }
            }]
```