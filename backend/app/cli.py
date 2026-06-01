import argparse
import sys
import json
from app.models.schemas import PRRequest
from app.services.analyzer_service import AnalyzerService
from app.services.report_service import ReportService

def main():
    parser = argparse.ArgumentParser(description="PRettySus: Deterministic PR Communication Quality Analyzer")
    parser.add_argument("command", choices=["analyze"], help="Command to run")
    parser.add_argument("--title", required=True, help="PR Title")
    parser.add_argument("--description-file", required=True, help="Path to PR description markdown/text file")
    parser.add_argument("--diff-file", required=True, help="Path to raw git diff file")
    parser.add_argument("--commits-file", help="Path to list of commit messages (one per line)")
    parser.add_argument("--squash-file", help="Path to proposed squash commit message")
    parser.add_argument("--output", help="Path to write JSON report")
    
    args = parser.parse_args()
    
    try:
        with open(args.description_file, 'r', encoding='utf-8') as f:
            desc = f.read()
        with open(args.diff_file, 'r', encoding='utf-8') as f:
            diff = f.read()
            
        commits = []
        if args.commits_file:
            with open(args.commits_file, 'r', encoding='utf-8') as f:
                commits = [c.strip() for c in f.readlines() if c.strip()]
                
        squash = None
        if args.squash_file:
            with open(args.squash_file, 'r', encoding='utf-8') as f:
                squash = f.read().strip()
                
        req = PRRequest(
            title=args.title,
            description=desc,
            commits=commits,
            diff=diff,
            proposedSquashMessage=squash
        )
        
        result = AnalyzerService.analyze_pr(req)
        
        # Print readable terminal summary
        print(f"--- PRettySus Analysis ---")
        print(f"Memory Integrity: {result.repositoryMemoryIntegrity.riskLevel.upper()} ({result.repositoryMemoryIntegrity.score}/100)")
        print(f"Base PR Risk: {result.riskLevel.upper()} ({result.score}/100)")
        sentry = "SAFE" if result.mainBranchSentry.isMainBranchSafe else "UNSAFE"
        print(f"Main Branch Sentry: {sentry}")
        
        if result.policyViolations:
            print("\n! Policy Violations:")
            for pv in result.policyViolations:
                print(f" - {pv.policy}: {pv.violation}")
                
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result.model_dump_json(indent=2))
            print(f"\nReport written to {args.output}")
            
        # Exit codes: 0=low/medium risk, 1=high risk/failed sentry/policy violation, 2=error
        if result.riskLevel == "high" or not result.mainBranchSentry.isMainBranchSafe or result.policyViolations:
            sys.exit(1)
        sys.exit(0)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
