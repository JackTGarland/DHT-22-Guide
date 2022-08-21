import Adafruit_DHT #This is the core, it takes data from the sensor.
from datetime import datetime #Used to get date time
from time import sleep # used to be able to sleep. I noticed my sensor would need two checks to get the right reading.

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4 # Being honest, no idea. But I assume it is the pin it's reading the data from on the pi.
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
sleep(1)

humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN) # getting the second accurate reading. Can add a print line if you don't belive me.

if humidity is not None and temperature is not None: # Lets make sure we got some data. 
        date_time = datetime.now()
        ts = date_time.strftime("%d-%m-%Y, %H:%M:%S")#Setting the string format for date time.
        writedata = (ts + "Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity)) # Assinging all the data to a single varible.
        print(writedata)
        f = open("temp.txt", "w") #The file we are writing to, and Wright permissions. It will make that file if not exsisting.
        f.write("\n") #Creates a new line so the data looks nice.
        f.write(writedata) #The write funtion can only take one argument so we had to reduce it down ealier. See there was a reason
else:
        print("Failed to retrieve data from humidity sensor")

