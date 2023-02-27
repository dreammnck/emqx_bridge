from fastapi import APIRouter
from pymongo import MongoClient
import threading
from dotenv import load_dotenv
import os
from bridge.mqtt_bridge import send_all_data, modelName

load_dotenv("/Users/marineyatajoparung/Documents/GitHub/emqx_bridge/env/.env")

thread = threading.Thread(target=send_all_data(), args=(1,))


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
@router.get("/trigger")
def trigger():
    ##stop thred
    thread.stop()
    
    modelName = []
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
        
    
        
    ## start Thred
    thread.start()
    return {"triggered"}





