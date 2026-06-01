from app.services.analyzer_service import AnalyzerService
from app.models.schemas import PRRequest

def test_analyzer_high_risk():
    service = AnalyzerService()

    req = PRRequest(
        title="Update",
        description="fix logic.",
        commits=["fix logic", "refactor"],
        diff="""+++ b/src/auth/jwt_handler.py
+def verify_token():
+    pass
+++ b/src/db/redis_cache.py
+def connect_redis():
+    pass
"""
    )

    response = service.analyze_pr(req)

    assert response.score <= 50
    assert response.riskLevel in ["high", "medium"]
    assert "fix logic" in response.genericPhrases
    # Check that changed files are flagged as uncovered high-impact entities
    uncov = response.communicationCoverage.uncoveredEntities + response.communicationCoverage.highImpactUncoveredEntities
    assert any("jwt_handler" in e or "redis_cache" in e for e in uncov)
    assert len(response.commitWarnings) > 0

def test_analyzer_low_risk():
    service = AnalyzerService()

    req = PRRequest(
        title="Implement JWT token verification and Redis caching",
        description="This PR implements the JWT token verification flow in jwt_handler and connects to Redis cache for session storage. It prevents frequent DB lookups.",
        commits=["Implement JWT verification logic", "Add Redis connection handler"],
        diff="""+++ b/src/auth/jwt_handler.py
+def verify_token():
+    pass
+++ b/src/db/redis_cache.py
+def connect_redis():
+    pass
"""
    )

    response = service.analyze_pr(req)

    assert response.score >= 70  # Good PR scores high but internal symbols may still reduce coverage
    assert response.riskLevel in ["low", "medium"]
    assert len(response.genericPhrases) == 0
    assert len(response.policyViolations) == 0
    assert len(response.commitWarnings) == 0
