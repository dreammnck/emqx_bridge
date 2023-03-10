from fastapi import FastAPI
from controller.trigger import thread, router


app = FastAPI()
app.include_router(router)

thread.start()

@app.get("/")
def root():
    return {"Hello":"World"}
    
    
    

