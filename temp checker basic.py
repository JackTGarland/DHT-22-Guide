import Adafruit_DHT
from datetime import datetime
from time import sleep

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
sleep(1)


humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

if humidity is not None and temperature is not None:
        date_time = datetime.now()
        ts = date_time.strftime("%d-%m-%Y, %H:%M:%S")
        writedata = (ts + "Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        print(writedata)
        f = open("temp.txt", "w")
        f.write("\n")
        f.write(writedata)
        print(writedata)
else:
        print("Failed to retrieve data from humidity sensor")

