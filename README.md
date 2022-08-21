# DHT-22-Guide
Just a small python script that get's the humidity and temprature and stores it in a text file.

This is a simple set up for the DHT-22 thermometer that can be used with the raspberry pi.

I was not a fan of the guides that were out there so I set out to make my own building off the guides.

There are two forms of this, the basic and advanced.

The Basic will just print the information and write it to a text file that will just keep growing till it reaches max file size.
UNLESS You use the renamer script

I would recomend using crontab for this, below is what I have mine running on, with the temp checking script running every 5 minuites. 
Then the renamer to store it in a seprate location running 2 minuites to midnight.

`*/5 * * * * python3 humidity2.py`
`58 23 * * * python3 rename.py`

You will need to add the file path to these locations if they are not in your home derectory. You should not need sudo for these scripts eaither so just `crontab -e` will work.

The advanced will write it to a SQL database and a basic API system is present should you want to make use of that. 

There are some commands that need to be run first. And all asuming it is on a raspberry pi.

Make sure you have Python as most of this is written in it. 

`python -m pip install cursor`

`python -m pip install mysql-connector-python`

The advanaced is still much more in a work in progress and I am debating it's implimentation. Eaither a public facing SQL database, or some kind of rest API service written in C# that will parse the data to SQL.

One is safer but harder to set up and I don't want to make this to complicated. 

Want to have a service on the pi that reads the most recent entry to the temp file and sends that data to some other service, be it on the pi or on a seprate server.

