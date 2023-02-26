from fastapi import FastAPI
from controller import trigger


app = FastAPI()
app.include_router(trigger.router)


"controller.thread".start()

@app.get("/")
def root():
    return {"Hello":"World"}
    
    
    

