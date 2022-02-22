"""
    Damon Vu
    11261393
    bav965
    ----------
    Raspberry Pi + DHT22 Temperature and Humidifier Sensor
"""

import paho.mqtt.client as mqtt
import ssl
from configparser import ConfigParser

# Config file 
config_file_name = "config.ini"
config = ConfigParser()
config.read(config_file_name)
iot = config["iot"]

# func for making connection
def on_connect(client, userdata, flags, rc):                
    client.subscribe("#" , 1 ) # Subscribe to all topics

# Func for receiving msgs
def on_message(client, userdata, msg):                      
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))
 
mqttc = mqtt.Client() 
mqttc.on_connect = on_connect    
mqttc.on_message = on_message

aws_iot_endpoint = iot["aws_iot_endpoint"]
port_number = int(iot["port_number"])
ca_path = iot["ca_path"]                                  
certificate_path = iot["certificate_path"]                          
private_key_path = iot["private_key_path"]  

mqttc.tls_set(ca_path, certfile=certificate_path, keyfile=private_key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      
 
mqttc.connect(aws_iot_endpoint, port_number, keepalive=60)               # connect to aws server
 
mqttc.loop_forever()                                        # Start receiving in loop