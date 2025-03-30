from fastapi import APIRouter

router = APIRouter('/agents')


@router.get("/")
async def root():
    return {"message": "Hello World"}