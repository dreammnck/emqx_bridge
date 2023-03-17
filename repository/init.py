from pymongo import MongoClient
import os
import ssl
from dotenv import load_dotenv

load_dotenv(".env")

def get_model():
    try:
        modelName = []
        client = MongoClient(os.getenv("CONNECTION_STRING"),ssl=True,tlsAllowInvalidCertificates=True)
        db = client["iotHealthcare"]
        collection = db["medicalModel"]
        results = collection.find({})
        for result in results:
            modelName.append(result["modelName"])
        print(modelName)
        return modelName
    except Exception:
        print("Error:" + Exception)

