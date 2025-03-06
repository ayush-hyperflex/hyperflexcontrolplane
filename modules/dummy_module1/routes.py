from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def say_hello():
    """Returns a simple message from Dummy Module 2."""
    return {"message": "Hello from Dummy Module 1!"}
