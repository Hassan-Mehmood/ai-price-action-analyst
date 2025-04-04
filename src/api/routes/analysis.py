from fastapi import APIRouter, UploadFile, File
from src.services.analysis_service import AnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])
analysis_service = AnalysisService()

@router.post("/daily")
async def daily_analysis(image: UploadFile = File(...)):
    file_content = await image.read()
    result = await analysis_service.analyze_daily(file_content)
    return result

@router.get("/test")
async def test_endpoint():
    return {"message": "Analysis endpoint is working"} 