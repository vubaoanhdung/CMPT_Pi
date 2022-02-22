"""
    Damon Vu
    11261393
    bav965
    ----------
    Raspberry Pi + DHT22 Temperature and Humidifier Sensor
"""

import paho.mqtt.client as mqtt
import ssl
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    print("Connection returned result: " + str(rc) )
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#" , 1 )                              # Subscribe to all topics
 
def on_message(client, userdata, msg):                      # Func for receiving msgs
    print("topic: "+msg.topic)
    print("payload: "+str(msg.payload))
 
mqttc = mqtt.Client()                                       # mqttc object
mqttc.on_connect = on_connect                               # assign on_connect func
mqttc.on_message = on_message                               # assign on_message func

aws_iot_endpoint = "abcbli22usgd8-ats.iot.us-west-2.amazonaws.com"      
port_number = 8883                                            
ca_path = "/home/pi/CMPT_Pi/aws_config/AmazonRootCA1.pem"                                      
certificate_path = "/home/pi/CMPT_Pi/aws_config/8f3b4b8f2c385bf994c2293f21a9487e2b7df0e7de0f1c9e10b25e79739c55d8-certificate.pem.crt"                            # <Thing_Name>.cert.pem
private_key_path = "/home/pi/CMPT_Pi/aws_config/8f3b4b8f2c385bf994c2293f21a9487e2b7df0e7de0f1c9e10b25e79739c55d8-private.pem.key"                          # <Thing_Name>.private.key

mqttc.tls_set(ca_path, certfile=certificate_path, keyfile=private_key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)      
 
mqttc.connect(aws_iot_endpoint, port_number, keepalive=60)               # connect to aws server
 
mqttc.loop_forever()                                        # Start receiving in loop