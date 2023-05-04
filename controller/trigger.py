from fastapi import APIRouter
<<<<<<< Updated upstream
=======
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from multiprocessing import Process
from bridge.mqtt_bridge import send_all_data, modelName

load_dotenv("/Users/marineyatajoparung/Documents/GitHub/emqx_bridge/env/.env")



process = Process(target=send_all_data)
process.start()


  
#Connect to database
try: 
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    db = client["iotHealthcare"]
    collection = db["medicalModel"]
    results = collection.find({})
    for result in results:
       modelName.append(result["modelName"])
except Exception:
    print("Error:" + Exception)
>>>>>>> Stashed changes


router = APIRouter(
    prefix="/trigger",
    tags=["trigger"],
)


@router.get("/")
def trigger():
<<<<<<< Updated upstream
    return {"Hello": "trigger"}
=======
    
    global process
    global modelName
    
    #Stop process
    process.terminate()
    
    modelName = []
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    db = client["iotHealthcare"]
    collection = db["medicalModel"]
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
    print(modelName)
    

    #Start new process
    process = Process(target=send_all_data)
    process.start()


    return {"triggerd"}






>>>>>>> Stashed changes
