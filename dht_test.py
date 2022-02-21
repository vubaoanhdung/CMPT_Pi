"""
    Damon Vu
    11261393
    bav965
    ----------
    Raspberry Pi + DHT22 Temperature and Humidifier Sensor
"""


import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT22(board.D18)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Set min_temperature and max_temperature if user called change_temperature.sh
min_value='19'
max_value='25'

# Preferred Temperature
min_temp = int(min_value) 
max_temp = int(max_value);
frequency_reading = 10

# print the current setting
print("\t\tCURRENT SETTING")
print("\t\tMIN TEMP = " + str(min_temp))
print("\t\tMAX TEMP = " + str(max_temp))
print("\t\tFREQUENCY READING: 10s")

print()
print("START COLLECTING DATA...")
print()

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        # print(error.args[0])
        time.sleep(2.0)
        continue

    # If the user kills the program, exit
    except Exception as error:
        dhtDevice.exit()
        raise error

    # Read data from sensor every frequency_reading seconds (if no error occurs)
    time.sleep(frequency_reading)
