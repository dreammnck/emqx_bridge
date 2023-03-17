from fastapi import FastAPI
from controller.trigger import router


app = FastAPI()
app.include_router(router)


@app.get("/")
def root():
    return {"Hello":"World"}
    
    
    

