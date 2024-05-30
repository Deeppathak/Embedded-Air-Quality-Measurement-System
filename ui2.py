import RPi.GPIO as GPIO
from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from time import sleep
from Adafruit_LED_Backpack import SevenSegment
from file1 import field1_mean, humidity, field2_mean, field3_mean, avg_temp, avg_hum, field_1, field_2, field_3, new_field_6_celsius

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

p = 0 #Pointer for iteration
r = [0, 1, 2, 3, 4] #array for switching the values

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
