from fastapi import APIRouter, UploadFile, File
from src.agents.agents import Agents

router = APIRouter(prefix="/analysis", tags=["analysis"])
agents = Agents()


@router.post("/hourly")
async def hourly_analysis(image: UploadFile = File(...)):
    return await agents.run_hourly_analysis(image)


@router.post("/daily")
async def daily_analysis(image: UploadFile = File(...)):
    return await agents.run_daily_analysis(image)


@router.post("/weekly")
async def weekly_analysis(image: UploadFile = File(...)):
    return await agents.run_weekly_analysis(image)
