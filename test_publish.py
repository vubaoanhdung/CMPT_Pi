"""
    Damon Vu
    11261393
    bav965
    ----------
    Raspberry Pi + DHT22 Temperature and Humidifier Sensor
"""

import paho.mqtt.client as mqtt
import ssl
import json
from time import sleep
from configparser import ConfigParser
import time
 
connected = False

# Config file 
config_file_name = "config.ini"
config = ConfigParser()
config.read(config_file_name)
iot = config["iot"]
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connected
    print("Connected to AWS")
    connected = True
    print("Connection returned result: " + str(rc) )
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func
#mqttc.on_log = on_log

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
 
while True:
    sleep(2)
    if connected:
        localtime = str(time.asctime(time.localtime(time.time())))
        start = "{"
        end = "}"
        message = "{}\"time\": \"{}\", \"temperature\": \"20\", \"humidity\": \"45\"{}".format(start,localtime,end)
        message = json.dumps(message) 
        message_json = json.loads(message)       
        mqttc.publish("test/CMPT_Pi", message_json , qos=1)        
        print("msg sent")
        print(message_json)

    else:
        print("waiting for connection...")                      