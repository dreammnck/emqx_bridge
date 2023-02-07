from fastapi import FastAPI
from controller import trigger

app = FastAPI()
app.include_router(trigger.router)


if __name__ == "__main__":
    @app.get("/")
    def root():
        return {"Hello": "World"}
