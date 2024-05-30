#importing all necessary packages
import requests
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import RPi.GPIO as RPi
import dht11
import time
# initialize GPIO
RPi.setwarnings(False)
RPi.setmode(RPi.BCM)

#print(5)
import json
clouddata = requests.get('https://thingspeak.com/channels/343018/feed.json')
clouddata=str(clouddata.text)
# Conversion of string message to a JSON message object
clouddata_json = json.loads(clouddata)
# Getting a channel from the JSON message
channels = clouddata_json['channel']
# Getting the feeds from the selected channel
feeds = clouddata_json['feeds']
# Example for accessing single entries (feeds) and fields
data = feeds[0]['field1']
print("Field 1 of first entry: ")
print(data)
data = feeds[5]['field2']
print("Field 2 of sixth entry: ")
print(data)
field_1=[]
field_2=[]
field_3=[]
field_4=[]
field_5=[]
field_6=[]
field_7=[]
field_8=[]
i=0
while i<=99:
    data=feeds[i]['field1']
    field_1.append(data)
    data = feeds[i]['field2']
    field_2.append(data)
    data = feeds[i]['field3']
    field_3.append(data)
    data = feeds[i]['field4']
    field_4.append(data)
    data = feeds[i]['field5']
    field_5.append(data)
    data = feeds[i]['field6']
    field_6.append(data)
    data = feeds[i]['field7']
    field_7.append(data)
    #value = feeds[i]['field8']
    #field_8.append(value)
    i+=1
print("The values in field1 are\n",field_1)
print("The values in field2 are\n",field_2)
print("The values in field3 are\n",field_3)
print("The values in field4 are\n",field_4)
print("The values in field5 are\n",field_5)
print("The values in field6 are\n",field_6)
print("The values in field7 are\n",field_7)
#print(field_8)
#Calculation of the mean values:
field_1 = [float(val) for val in field_1 if val is not None]
if field_1:
    field1_mean = mean(field_1)
    print("The mean of field1 value is", field1_mean)
else:
    print("Data in field1 is not valid")

field_2 = [float(val) for val in field_2 if val is not None]
if field_2:
    field2_mean = mean(field_2)
    print("The mean of field2 value is", field2_mean)
else:
    print("Data in field2 is not valid")

field_3 = [float(val) for val in field_3 if val is not None]
if field_3:
    field3_mean = mean(field_3)
    print("The mean of field3 value is", field3_mean)
else:
    print("Data in field3 is not valid")
#visualizing the PM values and mean values:
fig, axs = plt.subplots(5, 1, figsize=(8, 10))

# First subplot
axs[0].plot(range(len(field_1)), field_1, "-ro")
axs[0].axhline(y=field1_mean, color="r", linestyle="--")
axs[0].set_xlabel("sample")
axs[0].set_ylabel("ATM")
axs[0].set_title("PM 1.0")

# Second subplot
axs[1].plot(range(len(field_2)), field_2, "-ko")
axs[1].axhline(y=field2_mean, color="black", linestyle="--")
axs[1].set_xlabel("sample")
axs[1].set_ylabel("ATM")
axs[1].set_title("PM 2.5")

# Third subplot
axs[2].plot(range(len(field_3)), field_3, "-bo")
axs[2].axhline(y=field3_mean, color="b", linestyle="--")
axs[2].set_xlabel("sample")
axs[2].set_ylabel("ATM")
axs[2].set_title("PM 10")

plt.tight_layout()
#plt.show()

#-----Local Temperature and Humidity values----#
#conversion of temperature to celsius values
field_6 = [float(val) for val in field_6 if val is not None]
if field_6:
    field6_mean = mean(field_6)
    print("The mean of field6 value is", field6_mean)
else:
    print("Data in field6 is not valid")
new_field_6=[]
for i in field_6:
    t=(i-32)*0.555
    new_field_6.append(t)
    i+=1
new_field_6_celsius=list(map(float,new_field_6))
field_7 = [float(val) for val in field_7 if val is not None]
if field_7:
    field7_mean = mean(field_7)
    print("The mean of field7 value is", field7_mean)
else:
    print("Data in field7 is not valid")
humidity=field_7
print("The degree celsius temperature is",new_field_6_celsius)
print("The humidity is",humidity)

#local temperature and humidity values
while True:
    instance=dht11.DHT11(pin=4)
    result=instance.read()
    while not result.is_valid():
        result=instance.read()
    temp=result.temperature
    hum=result.humidity
    print("temperature is {0} and humidity is {1}".format(temp,hum))
    #fifo buffer
    if len(new_field_6_celsius)>100:
        new_field_6_celsius.pop(0)
    if len(humidity)>100:
        humidity.pop(0)

    #visualizing the temp humidity and mean values
    #fig, axs = plt.subplots(2, 1, figsize=(8, 10))
    avg_temp=mean(new_field_6_celsius)
    # First subplot
    axs[3].plot(range(len(new_field_6_celsius)), new_field_6_celsius, "-ro")
    axs[3].axhline(y=avg_temp, color="r", linestyle="--")
    axs[3].set_ylabel("celsius temperature")
    axs[3].set_title("temp")

    # Second subplot
    avg_hum=mean(humidity)
    axs[4].plot(range(len(field_2)), field_2, "-ko")
    axs[4].axhline(y=field2_mean, color="black", linestyle="--")
    axs[4].set_ylabel("humidity")
    axs[4].set_title("humidity")
    plt.show()
    plt.close()
    break


