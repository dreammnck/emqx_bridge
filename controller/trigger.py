from fastapi import APIRouter
from pymongo import MongoClient
import threading
from dotenv import load_dotenv
import os
from os import getppid, kill
import time
from signal import SIGKILL
from bridge.mqtt_bridge import send_all_data, modelName, exitflag1

load_dotenv("/Users/marineyatajoparung/Documents/GitHub/emqx_bridge/env/.env")



#stop_threads = False
#thread = threading.Thread(target=send_all_data)
#thread = threading.Thread(target=send_all_data, args =(lambda : stop_threads))
#n = 1

thread = threading.Thread(target=send_all_data, args =(lambda : exitflag1, ))
thread.start()
#exec("process" + str(n) + " = Process(target=send_all_data)")
#exec("process" + str(n) + ".start()")

  

#Connect to database
try: 
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    #print(client.list_database_names())
    db = client["iotHealthcare"]
    collection = db["medicalModel"]
    results = collection.find({})
    for result in results:
       modelName.append(result["modelName"])
except Exception:
    print("Error:" + Exception)


router = APIRouter(
    prefix="/trigger",
    tags=["trigger"],
)

             
#Trigger
@router.get("/")
def trigger():
    
    #global n
    global exitflag1
    global thread

    exitflag1 = True
    thread.join()
    
    #exec("process" + str(n) + ".kill()")
    #n+=1
    #print(n)
    modelName = []
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    db = client["iotHealthcare"]
    collection = db["medicalModel"]
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
    print(modelName)
    
 

    thread = threading.Thread(target=send_all_data, args =(lambda : exitflag1, ))
    thread.start()
    #exec("process" + str(n) + " = Process(target=send_all_data)")
    #exec("print('process" + str(n) + " = Process(target=send_all_data)')")
    #exec("process" + str(n) + ".start()")

    return {"triggerd"}






