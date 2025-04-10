from fastapi import APIRouter, UploadFile, File
from src.agents.agents import Agents

router = APIRouter(prefix="/analysis", tags=["analysis"])
agents = Agents()


@router.post("/daily")
async def daily_analysis(image: UploadFile = File(...)):
    return await agents.run_daily_analysis(image)


@router.get("/test")
async def test_endpoint():
    return {"message": "Analysis endpoint is working"}
