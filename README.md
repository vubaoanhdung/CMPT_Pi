## CMPT Pi

The setup contains a Raspberry Pi, a DHT22 temperature and humidity sensor, and various AWS services. It was used to self-correct the temperature in my bedroom. The Raspberry Pi reads data from the sensor, sends messages to IoT Core (using MQTT protocol). Then the IoT service puts data from the messages into DynamoDB. And at the same time, the Raspberry Pi will trigger Lambda functions which in turn will call some API requests to change the temperature setting of the thermostat (registered with Google Device Access Console).

![cmpt_pi drawio](https://user-images.githubusercontent.com/39688337/158084012-fbeed617-e129-47e5-a88d-9ca81c52d32b.png)

![pi1](https://user-images.githubusercontent.com/39688337/158084977-324305bd-d97c-44d8-b525-d153c45df8db.png)
![pi2](https://user-images.githubusercontent.com/39688337/158084978-c0190cd7-8e49-4e11-84df-f26f806d6fa8.png)
![pi3](https://user-images.githubusercontent.com/39688337/158084979-c48d02ef-b3c9-4e52-95b4-ad93e17e0f9d.png)
![pi4](https://user-images.githubusercontent.com/39688337/158084980-6d32f99b-73e6-4eab-8bc7-76bf7fe88f47.png)
![pi5](https://user-images.githubusercontent.com/39688337/158084981-225e5db2-d7ab-4f50-beb0-56eec38dd946.png)


