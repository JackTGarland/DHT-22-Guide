import os
from datetime import date
from sys import exit

location = os.getcwd()
os.chdir(location)
items = os.listdir(location)
for i in range(len(os.listdir(location))):
    print (items[i])
    if items[i] == "temp.txt":
        today = str(date.today())
        if os.path.exists(location + '/history/') == True:
            os.replace(location + "/temp.txt", location + "/history/"+ today + ".txt")
            print("file found")
            print(location + "/temp.txt",)
            print(location + "/history/"+ today + ".txt")
            exit()
        else:
            print("creating dir")
            print(location + "/temp.txt")
            print(location + "/history/"+ today + ".txt")
            os.mkdir("history")
            os.replace(location + "/temp.txt", location + "/history/"+ today + ".txt")
            exit()
