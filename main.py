from fastapi import FastAPI
from controller import trigger

app = FastAPI()
app.include_router(trigger.router)

@app.get("/")
def root():
    return {"started"}
    

