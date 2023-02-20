from fastapi import FastAPI
import threading
from controller import trigger
from bridge.mqtt_bridge import send_all_data


app = FastAPI()
app.include_router(trigger.router)


#x = threading.Thread(target=send_all_data(), args=(1,))
#x.start()

@app.get("/")
def root():
    return {"Hello":"World"}
    
    
    

