from fastapi import FastAPI
from controller.trigger import thread


app = FastAPI()
app.include_router(trigger.router)


thread.start()

@app.get("/")
def root():
    return {"Hello":"World"}
    
    
    

