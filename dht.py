import Adafruit_DHT
import sqlite3 as sql
 
# Set sensor type : Options are DHT11,DHT22 or AM2302
sensor=Adafruit_DHT.DHT11
 
# Set GPIO sensor is connected to
gpio=17
def get_data():
    # Use read_retry method. This will retry up to 15 times to
    # get a sensor reading (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
    con = sql.connect("/var/www/rover/sensordata.db")
    cur = con.cursor()
    data = cur.execute("insert into readings (temperature, humidity) values (" + temperature + ","+ humidity +")")
    # Reading the DHT11 is very sensitive to timings and occasionally
    # the Pi might fail to get a valid reading. So check if readings are valid.
    if humidity is not None and temperature is not None:
        data={"temp":temperature,"humidity":humidity,"result":"passed"}
        return data
    else:
        data={"temp":temperature,"humidity":humidity,"result":"failed"}
        return data

print(get_data())
