from app.services.analyzer_service import AnalyzerService
from app.models.schemas import PRRequest

def test_coverage_and_policies():
    service = AnalyzerService()
    
    # Simulate a risky migration PR missing rollback note
    req = PRRequest(
        title="Update database",
        description="minor fixes.",
        commits=["update things", "update things"],
        diff="""+++ b/src/db/migration_001.sql
+ALTER TABLE users DROP COLUMN email;
"""
    )
    
    response = service.analyze_pr(req)
    
    # 1. Policy violation check
    assert any(pv.policy == "Database Risk" for pv in response.policyViolations)
    
    # 2. Duplicate commits check
    assert len(response.duplicateCommitClusters) > 0
    assert "update things" in response.duplicateCommitClusters[0]
    
    # 3. Coverage check (uncovered high-impact entity: migration_001 or sql)
    assert len(response.communicationCoverage.highImpactUncoveredEntities) > 0
    
    # 4. Breakdown check
    assert response.scoringBreakdown.communicationCoverage.score < 100
    assert response.scoringBreakdown.commitQuality.score < 100
