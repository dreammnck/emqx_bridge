from fastapi import APIRouter
import pymongo
from pymongo import MongoClient
import threading
from main import x
from dotenv import load_dotenv
import os

load_dotenv()


modelName = []
#Connect to database
try: 
    client = MongoClient(os.getenv("CONNECTION_STRING"))
    print(client.list_database_names())
    db = client["iotHealthcare"]
    collection = db["medicalModel"]
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
    print(modelName)
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
    x.stop()
    
    modelName = []
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
        
    
        
    ## start Thred
    x.start()
    return {"triggered"}






