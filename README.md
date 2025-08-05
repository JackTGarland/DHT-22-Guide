# DHT-22-Guide
Just a small python script that get's the humidity and temprature and stores it in a text file.

This is a simple set up for the DHT-22 thermometer that can be used with the raspberry pi.

I was not a fan of the guides that were out there so I set out to make my own building off the guides.

There are two forms of this, the basic and advanced. The basic has comments from 3 years ago. I've learned more since then so the Advanced options have less comments and being honest was written with AI help.

The Basic will just print the information and write it to a text file that will just keep growing till it reaches max file size.
UNLESS You use the renamer script

I would recomend using crontab for this, below is what I have mine running on, with the temp checking script running every 5 minuites. 
Then the renamer to store it in a seprate location running 2 minuites to midnight.

`*/5 * * * * python3 humidity2.py`
`58 23 * * * python3 rename.py`

You will need to add the file path to these locations if they are not in your home derectory. You should not need sudo for these scripts eaither so just `crontab -e` will work.

# Advanced mode

If you want something a bit more fancy there is the advacned options.
This is more of a client server set-up.
We have 3 folders inside Advanced, Pico is for the PI Pico, this should work out the box, though if you are new a small note you will need to rename the file to "main.py" for it to run when you plug in the Pico. (I made this mistake and wasted a few hours.)

Pi Client contains the code for a regular raspberry Pi in my case it was a Pi 3, though it should work on any of them. 
You can run the python script however you want though I would recomend running it as a service:
sudo cp raspberry-pi-3-sensor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable raspberry-pi-3-sensor.service
sudo systemctl start raspberry-pi-3-sensor.service

You will need to update the .service file with the user you want to use and path to the files location. E.G. /home/pi/DHT-22/Advanced

Server contains code for the server. Same as above:
sudo cp central-sensor-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable central-sensor-dashboard.service
sudo systemctl start central-sensor-dashboard.service

The ports used as 5000,5001,5002 & 5003 this is partly due to me already having services on ports 80, but you can change these at the bottom of the .py files acordingly.

In the server file you will see that each device uses a seprate port. You can use the same port across devices so it runs on 5000 for all of them. I have done it this way for ilistration and for if you run both client and server on the same device.


# website usage

![Logo](https://raw.githubusercontent.com/JackTGarland/DHT-22-Guide/refs/heads/main/Temprature%20website.PNG)


Force Refresh fetches data, otherwise it will ping the devices every 5 minuites.
Locations are hard coded in the server HTML section. I may make this more customizable in the future.

Reload page just dose an F5 assuming that this will be displayed on a tablet or some other touch screen device.
## Installation

No install script, as of yet all manual sadly, though hopfully self explntory. 
You will need to run `pip install flask` on the client and server but not the Pico if you are uesing that.

The service files you need to edit the path to wherever you stored the files and the username you want the service to run on. This can be `pi` unless you have removed that user.

