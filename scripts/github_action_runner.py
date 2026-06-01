import os
import sys
import json
import subprocess
from app.models.schemas import PRRequest
from app.services.analyzer_service import AnalyzerService
from app.services.report_service import ReportService

def get_pr_details():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        return {"title": "Mock Title", "body": "Mock body", "commits": ["mock commit"], "diff": "+++ b/mock.py\n+def mock(): pass"}
        
    with open(event_path, 'r') as f:
        event = json.load(f)
        
    pr = event.get("pull_request", {})
    title = pr.get("title", "")
    body = pr.get("body", "")
    
    return {"title": title, "body": body or "", "commits": ["commit 1"], "diff": "+++ b/test.txt\n+test"}

def main():
    print("Running PRettySus GitHub Action...")
    
    try:
        diff_output = subprocess.check_output(["git", "diff", "origin/main...HEAD"]).decode("utf-8")
    except Exception:
        diff_output = "+++ b/src/main.py\n+def init(): pass"
        
    details = get_pr_details()
    
    req = PRRequest(
        title=details["title"],
        description=details["body"],
        commits=details["commits"],
        diff=diff_output
    )
    
    result = AnalyzerService.analyze_pr(req)
    report = ReportService.generate_markdown(result, req.title)
    
    print("\n" + report + "\n")
    
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(report)
            
    if result.riskLevel == "high" or not result.mainBranchSentry.isMainBranchSafe or result.policyViolations:
        print("PRettySus validation failed. Please improve PR communication.")
        sys.exit(1)
        
    print("PRettySus validation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
