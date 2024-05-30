#importing all neccessary pakages
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

import json
clouddata = requests.get('https://thingspeak.com/channels/343018/feed.json')
clouddata=str(clouddata.text)
# String message onversion to json
clouddata_json = json.loads(clouddata)
# Defining the channel
channels = clouddata_json['channel']
# Extracting the feeds
feeds = clouddata_json['feeds']
# Example for accessing single entries (feeds) and fields
data = feeds[0]['field1']
print("Field 1 of first entry: ")
print(data)
data = feeds[5]['field2']
print("Field 2 of sixth entry: ")
print(data)
# implementing the above concept below to extract all the value from cloud by using a loop
#creating field arrays to store the accessed value
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
import thingspeak
import time
# the new thinkspeak Channel
channel_id = 2227426
write_key = '5RZ6KVVYHQLKAZ92'
channel = thingspeak.Channel(id=channel_id, api_key=write_key)


# aqi measurements
def AQI_pm25(x):
    x=float(x)
    if 0 <= x <= 12.0:
        AQI_Formula = (((50 - 0) * (x - 0)) / (12 - 0)) + 0
    elif 12.1 <= x <= 35.4:
        AQI_Formula = (((100 - 51) * (x - 12.1)) / (35.4 - 12.1)) + 51
    elif 35.5 <= x <= 55.4:
        AQI_Formula = (((150 - 101) * (x - 35.5)) / (55.5 - 35.5)) + 101
    elif 55.5 <= x <= 150.4:
        AQI_Formula = (((200 - 151) * (x - 55.5)) / (150.4 - 55.5)) + 151
    elif 150.5 <= x <= 250.4:
        AQI_Formula = (((300 - 201) * (x - 150.5)) / (250.4 - 150.5)) + 201
    elif 250.5 <= x <= 350.4:
        AQI_Formula = (((400 - 301) * (x - 250.5)) / (350.4 - 250.5)) + 301
    elif 350.5 <= x <= 500.4:
        AQI_Formula = (((500 - 401) * (x - 350.5)) / (500.4 - 350.5)) + 401
    AQI_Formula = "{:.2f}".format(AQI_Formula)
    return AQI_Formula


def AQI_pm10(x):  # for pm10
    x=float(x)
    if 0 <= x <= 54.0:
        AQI_Formula = (((50 - 0) * (x - 0)) / (54 - 0)) + 0
    elif 55 <= x <= 154:
        AQI_Formula = (((100 - 51) * (x - 55)) / (154 - 55)) + 51
    elif 155 <= x <= 254:

        AQI_Formula = (((150 - 101) * (x - 155)) / (254 - 155)) + 101
    elif 255 <= x <= 354:
        AQI_Formula = (((200 - 151) * (x - 255)) / (354 - 255)) + 151
    elif 355 <= x <= 424:
        AQI_Formula = (((300 - 201) * (x - 355)) / (424 - 355)) + 201
    elif 425 <= x <= 504:
        AQI_Formula = (((400 - 301) * (x - 425)) / (504 - 425)) + 301
    elif 505 <= x <= 604:
        AQI_Formula = (((500 - 401) * (x - 505)) / (604 - 505)) + 401
    AQI_Formula = "{:.2f}".format(AQI_Formula)
    return AQI_Formula


# Initialize empty lists to store AQI values
aqi_pm25 = []
aqi_pm10 = []

# Calculate AQI for PM2.5 values and store them in aqi_pm25
for i in field_2:
    v = AQI_pm25(i)
    aqi_pm25.append(v)

# Calculate AQI for PM10 values and store them in aqi_pm10
for i in field_3:
    v = AQI_pm10(i)
    aqi_pm10.append(v)

# Print the calculated AQI values for PM2.5 and PM10
print("AQI values for PM2.5:", aqi_pm25)
print("AQI values for PM10:", aqi_pm10)
print("wait for channel to update")
# Initialize a list to store the maximum AQI values
Maximum_AQI = []

# Iterate through the first 100 elements in aqi_pm25 and aqi_pm10
for z in range(len(field_2)):
    # Check which AQI value is greater, PM2.5 or PM10
    if aqi_pm25[z] < aqi_pm10[z]:  # If PM2.5 AQI is less than PM10 AQI
        v = aqi_pm10[z]  # Assign the PM10 AQI value to v
        Maximum_AQI.append(v)  # Append the PM10 AQI to the Maximum_AQI list
    else:  # If PM10 AQI is less than PM2.5 AQI
        v = aqi_pm25[z]  # Assign the PM2.5 AQI value to v
        Maximum_AQI.append(v)  # Append the PM2.5 AQI to the Maximum_AQI list

    # Update the cloud channel with AQI values for PM2.5, PM10, and Maximum AQI
    channel.update({'field1': aqi_pm25[z], 'field2': aqi_pm10[z], 'field3': Maximum_AQI[z]})

    # Add a small delay to avoid excessive updates
    time.sleep(0.25)

import RPi.GPIO as GPIO
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from time import sleep
from Adafruit_LED_Backpack import SevenSegment

# Initialize LED matrix and 7-segment display
serial = spi(port=0, device=1, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)
segment_7SD = SevenSegment.SevenSegment(address=0x70)
segment_7SD.begin()

# Initialize GPIO with RPi.GPIO
lft_btn = 25
rgt_btn = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(lft_btn, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(rgt_btn, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

p = 0  # Pointer for iteration
r = [0, 1, 2, 3, 4]  # array for switching the values
t=1 # this is for timing code in overall program structure
# Infinite loop to continuously update and display value based on 'p'
while True:
    print("PM1 value - press button to change for 2 sec", p)

    # Visualize the current value of 'p' using LED Matrix Display (MLD)
    with canvas(device) as draw:
        for i in range(5):
            if i == p:
                draw.point((i, 0), fill="white")  # Turn on the pixel (white) to indicate the selected value
            else:
                draw.point((i, 0), fill="black")  # Turn off the pixel (black) for other value options

    sleep(0.5)

    # Check if the right button is pressed for 2 seconds
    if not GPIO.input(rgt_btn):
        p = p + 1 if p < 4 else 0  # Increment 'p' to cycle through values 0 to 4
        print("right button is pressed!")
    # Check if the left button is pressed for 2 seconds
    elif not GPIO.input(lft_btn):
        p = p - 1 if p > 0 else 4  # Decrement 'p' to cycle through values 4 to 0
        print("left button is pressed!")

    # Visualize and process value based on the value of 'p'
    if p == 0:
        # Display and visualize value for PM1 (Particulate Matter 1)
        mean_PM1 = field1_mean
        StrMeasurement = str(float(round(mean_PM1, 2)))
        for y in range(0, len(StrMeasurement)):
            segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)  # Display value on 7-segment display
            segment_7SD.set_decimal(1, 1)  # Set decimal point at the second position (if applicable)
        segment_7SD.write_display()

        # Calculate and visualize bar graph for PM1
        d = [int(round((sum(field_1[j * 12:(j * 12) + 12]) / 12) / 10)) for j in range(8)]
        with canvas(device) as draw:
            for i in range(8):
                draw.point((i, 7 - d[i]), fill="white")  # Visualize the measurements on the LED Matrix Display (MLD)
        sleep(0.8)

    elif p == 1:
        # Display and visualize value for PM2.5 (Particulate Matter 2.5)
        mean_PM2_5 = field2_mean
        StrMeasurement = str(float(round(mean_PM2_5, 2)))
        for y in range(0, len(StrMeasurement)):
            segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
            segment_7SD.set_decimal(1, 1)
        segment_7SD.write_display()

        # Calculate and visualize bar graph for PM2.5
        d = [int(round((sum(field_2[j * 12:(j * 12) + 12]) / 12) / 10)) for j in range(8)]
        with canvas(device) as draw:
            for i in range(8):
                draw.point((i, 7 - d[i]), fill="white")
        sleep(0.8)

    elif p == 2:
        # Display and visualize value for PM10 (Particulate Matter 10)
        mean_PM10 = field3_mean
        StrMeasurement = str(float(round(mean_PM10, 2)))
        for y in range(0, len(StrMeasurement)):
            segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
            segment_7SD.set_decimal(1, 1)
        segment_7SD.write_display()

        # Calculate and visualize bar graph for PM10
        d = [int(round((sum(field_3[j * 12:(j * 12) + 12]) / 12) / 10)) for j in range(8)]
        with canvas(device) as draw:
            for i in range(8):
                draw.point((i, 7 - d[i]), fill="white")  # Visualize the measurements on the LED Matrix Display (MLD)
        sleep(0.8)

    elif p == 3:
        # Display and visualize value for Cloud Average Temperature
        mean_temp = avg_temp * 100
        print("cloud average temperature", avg_temp)
        StrMeasurement = str(float(round(mean_temp, 2)))
        for y in range(0, len(StrMeasurement)):
            segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
            segment_7SD.set_decimal(2, 2)  # Set decimal point at the third position (if applicable)
        segment_7SD.write_display()

        # Calculate and visualize bar graph for Cloud Average Temperature
        d = [int(round((sum(new_field_6_celsius[j * 12:(j * 12) + 12]) / 12) / 100)) for j in range(8)]
        with canvas(device) as draw:
            for i in range(8):
                draw.point((i, 7 - d[i]), fill="white")
        sleep(0.8)

    elif p == 4:
        # Display and visualize value for Cloud Average Humidity
        mean_hum = avg_hum * 100
        print("cloud average humidity", mean_hum)
        StrMeasurement = str(float(round(mean_hum, 2)))
        for y in range(0, len(StrMeasurement)):
            segment_7SD.set_digit(y, StrMeasurement[y], decimal=False)
            segment_7SD.set_decimal(1, 1)
        segment_7SD.write_display()

        # Calculate and visualize bar graph for Cloud Average Humidity
        d = [int(round((sum(humidity[j * 12:(j * 12) + 12]) / 12) / 100)) for j in range(8)]
        with canvas(device) as draw:
            for i in range(8):
                draw.point((i, 7 - d[i]), fill="white")
        sleep(0.8)

#from here the timing code runs every 60 seconds as per overall program
    if t % 60 == 0:
        #thingspeak channel
        field_data = requests.get('https://thingspeak.com/channels/343018/feed.json')
        # decoding json value
        fields = json.loads(field_data.text)
        channels = fields['channel']
        feeds = fields['feeds']
        field_1 = []
        field_2 = []
        field_3 = []
        field_4 = []
        field_5 = []
        field_6 = []
        field_7 = []
        field_8 = []

        # Appending values using while loop.
        m = 0
        while m <= 99:
            data = feeds[m]['field1']
            field_1.append(data)

            data = feeds[m]['field2']
            field_2.append(data)

            data = feeds[m]['field3']
            field_3.append(data)

            data = feeds[m]['field4']
            field_4.append(data)

            data = feeds[m]['field5']
            field_5.append(data)

            data = feeds[m]['field6']
            field_6.append(data)

            data = feeds[m]['field7']
            field_7.append(data)

            #value = feeds[m]['field8']
            #field_8.append(value)
            m += 1

        # Printing the field Datas
        print("60 seconds completed value is been fetched from the cloud")
        print('Field 1 value is -', field_1)
        print('\nField 2 value is -', field_2)
        print('\nField 3 value is -', field_3)
        print('\nField 4 value is -', field_4)
        print('\nField 5 value is -', field_5)
        print('\nField 6 value is -', field_6)
        print('\nField 7 value is -', field_7)
        #print('\nField 8 value is -', field_8)
        # part 2
        # Mean Values of the field Datas
        field_1 = [float(val) for val in field_1 if val is not None]
        field_1 = list(map(float, field_1))
        mean_field1 = mean(field_1)
        print('Mean value of field1 is', mean_field1)
        field_2 = [float(val) for val in field_2 if val is not None]
        field_2 = list(map(float, field_2))
        mean_field2 = mean(field_2)
        print('Mean value of field2 is', mean_field2)
        field_3 = [float(val) for val in field_3 if val is not None]
        field_3 = list(map(float, field_3))
        mean_field3 = mean(field_3)
        print('Mean value of field3 is', mean_field3)
        field_6 = [float(val) for val in field_6 if val is not None]
        field_6 = list(map(float, field_6))
        #convert temperature in degree celsius
        field_6_c = []
        for f in field_6:
            tc = (f - 32) * (5 / 9)
            field_6_c.append(tc)
            f = f + 1
        temp_cld_in_degreeC = list(map(float, field_6_c))
        field_7 = [float(val) for val in field_7 if val is not None]
        field_7 = list(map(float, field_7))
        humi_cld = field_7

        print(temp_cld_in_degreeC)
        print(humi_cld)


    #taking Local temperature and humidity values every 10 seconds
    if t % 10 == 0 or t == 1 :
        instance = dht11.DHT11(pin=4)
        result = instance.read()
        while not result.is_valid():
            result = instance.read()

        temp = result.temperature
        hum = result.humidity
        print("10 seconds completed temperature and humidity updated")
        print("Temperature: %-3.1f C" % temp)
        print("Humidity: %-3.1f %%" % hum)
        new_field_6_celsius.append(temp)
        humidity.append(hum)
        #fifo buffer
        if len(new_field_6_celsius) > 100:
            new_field_6_celsius.pop(0)
        if len(humidity) > 100:
            humidity.pop(0)

        #visualizing the temperature humidity and mean values.
        plt.subplot(5, 1, 1)
        plt.plot(range(len(field_1)), field_1, 'rd-')
        plt.axhline(y=field1_mean, color='r', linestyle='--')
        plt.xlabel('sample')
        plt.ylabel('ATM')
        plt.title('PM 1.0')

        plt.subplot(5, 1, 2)
        plt.plot(range(len(field_2)), field_2, 'ko-')
        plt.axhline(y=field2_mean, color='black', linestyle='--')
        plt.xlabel('sample')
        plt.ylabel('ATM')
        plt.title('PM 2.5')

        plt.subplot(5, 1, 3)
        plt.plot(range(len(field_3)), field_3, 'bo-')
        plt.axhline(y=field3_mean, color='b', linestyle='--')
        plt.xlabel('sample')
        plt.ylabel('ATM')
        plt.title('PM 10')
        plt.subplot(5, 1, 4)
        average_temp = sum(new_field_6_celsius) / len(new_field_6_celsius)
        plt.plot(range(len(new_field_6_celsius)), new_field_6_celsius, 'rd-')
        plt.axhline(y=avg_temp, color='r', linestyle='--')
        plt.ylabel('Temp in deg C')
        plt.title('Temperature')
        plt.subplot(5, 1, 5)
        average_hum = int(sum(humidity)) / int(len(humidity))
        plt.plot(range(len(humidity)), humidity, 'bo-')
        plt.axhline(y=avg_hum, color='b', linestyle='--')
        plt.ylabel('Humidity %')
        plt.title('Humidity')
        plt.show()
        #transfer of aqi value every minute.
        aqi_pm25 = []
        for i in field_2:
            v = AQI_pm25(i)
            aqi_pm25.append(v)
        aqi_pm10 = []
        for i in field_3:
            v = AQI_pm10(i)
            aqi_pm10.append(v)
        print(aqi_pm25)
        print(aqi_pm10)
        Maximum_AQI = []
        z = 0
        q = z + 99
        while z < 1 and q < len(field_3):
            aqi_pm10_value = AQI_pm10(field_3[q])
            aqi_pm25_value = AQI_pm25(field_2[q])


            if aqi_pm10_value > aqi_pm25_value:
                v = aqi_pm25_value
                Maximum_AQI.append(v)
                print(v)
            else:
                v = aqi_pm10_value
                Maximum_AQI.append(v)
            print('the channel has been updated')
            channel.update({'field1': aqi_pm25_value, 'field2': aqi_pm10_value, 'field3': Maximum_AQI[z - 1]})
            time.sleep(0.25)
            z = z + 1
        t = t + 1
    t = t + 1
