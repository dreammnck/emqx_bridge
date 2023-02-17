from fastapi import APIRouter
import pymongo
from pymongo import MongoClient
import threading

modelName = []
#Connect to database
conn_str = "mongodb+srv://iotHealthcare:edHdnrYXycAmvf4q@dev-iot-healthcare.dk1uvoe.mongodb.net/?retryWrites=true&w=majority"
try: 
    client = MongoClient(conn_str)
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
@router.get("/")
def trigger():
    ##stop thred
    modelName = []
    results = collection.find({})
    for result in results:
        modelName.append(result["modelName"])
    ## start Thred
    return {"trigger"}






