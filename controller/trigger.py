from fastapi import APIRouter


router = APIRouter(
    prefix="/trigger",
    tags=["trigger"],
)


@router.get("/")
def trigger():
    return {"Hello": "trigger"}