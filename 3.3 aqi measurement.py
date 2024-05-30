from file1 import field_2
from file1 import field_3

import thingspeak
import time
#the new thinkspeak Channel
channel_id = 2227426
write_key = '5RZ6KVVYHQLKAZ92'
channel = thingspeak.Channel(id=channel_id, api_key=write_key)
#aqi measurements
def AQI_pm25(x):
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

# Initialize a list to store the maximum AQI values
Maximum_AQI = []

# Iterate through the first 100 elements in aqi_pm25 and aqi_pm10
for z in range(99):
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
