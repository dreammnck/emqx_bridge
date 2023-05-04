import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from pymongo import MongoClient
from dotenv import load_dotenv
from kafka_client.init import init_producer
import os


load_dotenv("/Users/marineyatajoparung/Documents/GitHub/emqx_bridge/env/.env")

producer = KafkaProducer(init_producer())
modelName = []


#Connect to database
try:
    modelName = []
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    db = client["iotHealthcare"]
    collection = db["medicalModel"]
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
except Exception:
    print("Error:" + Exception)



## KAFKA
def send_message_to_kafka(topic, message):
    """
    Sends message to kafka (duh). Async by default.
    :param message:
    :return:
    """
    
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
        
    # Subscribing in on_connect() 

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
    
    send_message_to_kafka(msg.topic, msg.payload)    
    print(msg.topic+" "+str(msg.payload))
    


def mqtt_to_kafka_run():
    #Pick messages off MQTT queue and put them on Kafka
    
    broker = os.getenv("EMQX_BROKER")
    port = int(os.getenv("EMQX_PORT"))
    username = os.getenv("EMQX_USERNAME")
    password = os.getenv("EMQX_PASSWORD")
  

    client = mqtt.Client()
    client.username_pw_set(username, password)
    # client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    client.connect(broker, port, 1000)
    
    for model in modelName:
        client.subscribe(model, qos=2)
           
    while True:
        client.loop_start()
    



        
def send_all_data():
    attempts = 0

    while (attempts < 10):
        try:
            mqtt_to_kafka_run()

        except NoBrokersAvailable:
            print("No Brokers. Attempt %s" % attempts)
            attempts = attempts + 1
    
            
            
            