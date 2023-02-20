import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import random
import time
#from controller.trigger import modelName
from dotenv import load_dotenv
import os
from controller.trigger import modelName

load_dotenv("/Users/marineyatajoparung/Documents/GitHub/emqx_bridge/env/.env")

brokers = os.getenv("KAFKA_ADVERTISED_HOST_NAME","").split(",")
print(brokers)
producer = KafkaProducer(bootstrap_servers=brokers)

## KAFKA
def send_message_to_kafka(topic, message):
    """
    Sends message to kafka (duh). Async by default.
    :param message:
    :return:
    """

    print("sending message to kafka: %s" % message)
    producer.send(topic, message)


## MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    """
    Callback for connect to MQTT event
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return: None
    """

    print("Connected %s, %s, %s %s" % (client, userdata, flags, rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(modelName)

def on_disconnect(client, user_data, rc):
    """
    Callback for disconnect event
    :param client:
    :param user_data:
    :param rc:
    :return: None
    """

    print("""Disconnected
    client: %s
    user_data: %s
    rc: %s
    """ % (client, user_data, rc))


def on_message(client, userdata, msg):
    """
    The callback for when a PUBLISH message is received from the server.
    :param client:
    :param userdata:
    :param msg:
    :return: None
    """
    print(msg.topic+" "+str(msg.payload))
    send_message_to_kafka(msg.topic, msg.payload)


def mqtt_to_kafka_run():
    #Pick messages off MQTT queue and put them on Kafka
    broker = os.getenv("EMQX_BROKER")
    port = os.getenv("EMQX_PORT")
    username = os.getenv("EMQX_USERNAME")
    password = os.getenv("EMQX_PASSWORD")

    client = mqtt.Client(f'python-mqtt-{random.randint(0, 1000)}')
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(broker, port, 1000)
    client.loop_forever()

def send_all_data():
    attempts = 0
    while attempts < 10:
        try:
            mqtt_to_kafka_run()

        except NoBrokersAvailable:
            print("No Brokers. Attempt %s" % attempts)
            attempts = attempts + 1
            time.sleep(2)
    
            
            
            