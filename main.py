from fastapi import FastAPI
<<<<<<< Updated upstream
from controller import trigger
=======
from controller.trigger import router
from bridge.mqtt_bridge import send_all_data

>>>>>>> Stashed changes

app = FastAPI()
app.include_router(trigger.router)

<<<<<<< Updated upstream
=======
@app.get("/")
def root():
    return {"started"}
    
    
    
>>>>>>> Stashed changes

if __name__ == "__main__":
    @app.get("/")
    def root():
        return {"Hello": "World"}
