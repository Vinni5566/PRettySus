from fastapi import APIRouter
from pydantic import BaseModel
from app.models.schemas import PRRequest, PRResponse
from app.services.analyzer_service import AnalyzerService
from app.services.report_service import ReportService

router = APIRouter()

@router.post("/analyze", response_model=PRResponse)
async def analyze_pull_request(request: PRRequest):
    return AnalyzerService.analyze_pr(request)

class ReportResponse(BaseModel):
    markdown: str

@router.post("/analyze/report", response_model=ReportResponse)
async def analyze_pull_request_report(request: PRRequest):
    result = AnalyzerService.analyze_pr(request)
    md = ReportService.generate_markdown(result, request.title)
    return ReportResponse(markdown=md)
