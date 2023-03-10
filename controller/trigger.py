from fastapi import APIRouter
from pymongo import MongoClient
import threading
from dotenv import load_dotenv
import os
from bridge.mqtt_bridge import send_all_data, modelName


load_dotenv("/Users/marineyatajoparung/Documents/GitHub/emqx_bridge/env/.env")

stop_threads = False
thread = threading.Thread(target=send_all_data, args =(lambda : stop_threads))
 
#Connect to database
try: 
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    #print(client.list_database_names())
    db = client["iotHealthcare"]
    collection = db["medicalModel"]
    results = collection.find({})
    for result in results:
       modelName.append(result["modelName"])
    #print(modelName)
except Exception:
    print("Error:" + Exception)



router = APIRouter(
    prefix="/trigger",
    tags=["trigger"],
)

#Trigger
@router.get("/")
def trigger():
    ##stop thred
    stop_threads = True
    print('thread killed')
    
    modelName = []
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
    stop_threads = False   
    
        
    ## start Thred
    #new_thread = threading.Thread(target=send_all_data, args =(lambda : stop_threads))
    #new_thread.start()

    return {"triggered"}





