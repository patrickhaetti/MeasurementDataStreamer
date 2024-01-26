setup telegraf (telegraf will push info to influxdb)


sudo apt update
sudo apt install telegraf


configure influxDB config file
(-> influxdb server url )

1) nano /etc/telegraf/telegraf.conf
	* go to [outputs.influxdb] and uncomment it
	* add ip of raspi where grafana is also running on to urls=[x.x.x.x:8086]
	* add username "admin" and password "admin"
	* set database = "newmeasurementdatabase" # the one from influxDB

2) look if all is ok in influx config
nano /etc/influxdb/influxdb.conf

3) systemctl restart grafana-server
3) systemctl restart influxdb
3) systemctl restart telegraf





