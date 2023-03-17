from fastapi import APIRouter
from multiprocessing import Process
from dotenv import load_dotenv
import os
from bridge.mqtt_bridge import send_all_data
    


load_dotenv("/Volumes/project/capstone-project/emqx_bridge/.env")

#stop_threads = False
#thread = threading.Thread(target=send_all_data)
#thread = threading.Thread(target=send_all_data, args =(lambda : stop_threads))
process = Process(target=send_all_data)
process.start()




router = APIRouter(
    prefix="/trigger",
    tags=["trigger"],
)

#Trigger
@router.get("/")
def trigger():
    ##stop thred
    #stop_threads = True
    process.kill()
    
    # client = MongoClient(os.getenv("CONNECTION_STRING"))
    # db = client["iotHealthcare"]
    # collection = db["medicalModel"]
    # results = collection.find({})
    # for result in results:
    #     modelName.append(result["modelName"])
    # print(modelName)
    
    #stop_threads = False   
    ## start Thred
    new_process = Process(target=send_all_data)
    new_process.start()
    #process = Process(target=send_all_data)
    #process.start()

    return {"triggered"}





