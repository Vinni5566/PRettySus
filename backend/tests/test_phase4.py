from app.services.analyzer_service import AnalyzerService
from app.services.report_service import ReportService
from app.models.schemas import PRRequest
from fastapi.testclient import TestClient
from main import app

def test_markdown_report_generation():
    """Ensure the markdown report contains all critical Phase 3 & 4 sections."""
    service = AnalyzerService()
    req = PRRequest(
        title="Test Report Validation",
        description="A simple description.",
        commits=["feat: initial commit"],
        diff="+++ b/src/main.py\n+def do_something(): pass\n"
    )
    
    result = service.analyze_pr(req)
    markdown = ReportService.generate_markdown(result, req.title)
    
    assert "PRettySus Analysis Report: Test Report Validation" in markdown
    assert "Repository Memory Integrity:" in markdown
    assert "Main Branch Sentry" in markdown
    assert "Communication Coverage" in markdown
    assert "Squash & Merge Analysis" in markdown
    assert "Deterministic Suggested Summary" in markdown

import asyncio

def test_report_endpoint():
    """Test the POST /api/analyze/report endpoint logic directly."""
    from app.api.endpoints import analyze_pull_request_report
    
    req = PRRequest(
        title="Endpoint Test",
        description="Validating the report endpoint.",
        commits=["fix: typo"],
        diff="+++ b/README.md\n+hello"
    )
    
    response = asyncio.run(analyze_pull_request_report(req))
    
    assert response is not None
    assert hasattr(response, "markdown")
    assert "PRettySus Analysis Report: Endpoint Test" in response.markdown
