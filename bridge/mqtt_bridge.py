import paho.mqtt.client as mqtt
from kafka.errors import NoBrokersAvailable
from pymongo import MongoClient
import random
import time
from dotenv import load_dotenv
import os
from  kafka_client.init import init_producer
from repository.init import get_model
load_dotenv(".env")




## KAFKA
def send_message_to_kafka(topic, message, producer):
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
    if rc==0:
        print("connected OK Returned code=",rc)
        #print("Connected %s, %s, %s %s" % (client, userdata, flags, rc))
    else:
        print("Bad connection Returned code=",rc)
        
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    modelName = userdata["model"]
    for model in modelName:
        client.subscribe(model)

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
    send_message_to_kafka(msg.topic, msg.payload, userdata["producer"])


def mqtt_to_kafka_run(model):
    #Pick messages off MQTT queue and put them on Kafka
    broker = os.getenv("EMQX_BROKER")
    port = int(os.getenv("EMQX_PORT"))
    username = os.getenv("EMQX_USERNAME")
    password = os.getenv("EMQX_PASSWORD")
  
    producer = init_producer()
    client_userdata = {"producer": producer, "model": model}
    client = mqtt.Client(f'python-mqtt-{random.randint(0, 1000)}', userdata=client_userdata)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    client.connect(broker, port, 1000)
    client.loop_forever()


def send_all_data():
    attempts = 0
    model = get_model()
    while attempts < 10:
        try:
            mqtt_to_kafka_run(model)

        except NoBrokersAvailable:
            print("No Brokers. Attempt %s" % attempts)
            attempts = attempts + 1
            time.sleep(2)
    
            
            
            