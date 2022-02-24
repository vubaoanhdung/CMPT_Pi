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
import paho.mqtt.client as mqtt
import ssl
import json
from configparser import ConfigParser

# Config file 
config_file_name = "config.ini"
config = ConfigParser()
config.read(config_file_name)
iot = config["iot"]

def on_connect(client, userdata, flags, rc):
    global connected
    print("\nConnected to AWS IoT Core\n")
    connected = True

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
mqttc = mqtt.Client() # mqttc object
mqttc.on_connect = on_connect  # assign on_connect func
mqttc.on_message = on_message # assign on_message func


# Setting up mqttc
# aws_iot_endpoint = "abcbli22usgd8-ats.iot.us-west-2.amazonaws.com"      # Device data endpoint
aws_iot_endpoint = iot["aws_iot_endpoint"]
port_number = int(iot["port_number"])
ca_path = iot["ca_path"]                                  
certificate_path = iot["certificate_path"]                          
private_key_path = iot["private_key_path"]                        
mqttc.tls_set(ca_path, certfile=certificate_path, keyfile=private_key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  

# connecting
mqttc.connect(aws_iot_endpoint, port_number, keepalive=60)  # connect to aws server
mqttc.loop_start()



# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

# Connection to AWS IoT Core
connected = False  

# Set min_temperature and max_temperature
# Can change these values by using change_temperature.sh
min_value='19'
max_value='25'

# Convert min_value and max_value to min_temp and max_temp
min_temp = int(min_value) 
max_temp = int(max_value);

# Read data every <frequency_reading> seconds
frequency_reading = int(iot["frequency_reading"])

# print the current settings
print()
print("CURRENT SETTING:")
print("\t\tMIN TEMP = " + str(min_temp))
print("\t\tMAX TEMP = " + str(max_temp))
print("\t\tFREQUENCY READING: " + str(frequency_reading))

topic = iot["topic"]
while True:
    
    time.sleep(frequency_reading)
    
    try:
        # Get the temp and humidity
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
        
        if connected:
            localtime = str(time.asctime(time.localtime(time.time())))
            start = "{"
            end = "}"
            message = "{}\"timestamp\":\"{}\", \"temperature\": {:.1f}, \"humidity\": {}{}".format(start,localtime,temperature_c, humidity,end)
            message = json.dumps(message) 
            message_json = json.loads(message)       
            mqttc.publish(topic, message_json , qos=1) 
            
            # For Testing       
            # print("msg sent")
            # print(message_json)
        
        else:
            print("waiting for connection...")  

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        continue

    # If the user kills the program, exit
    except Exception as error:
        dhtDevice.exit()
        raise error
