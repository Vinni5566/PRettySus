from app.services.analyzer_service import AnalyzerService
from app.models.schemas import PRRequest

def test_noisy_squash_merge():
    """15 noisy commits with 1 buried signal. Expect high squash risk."""
    service = AnalyzerService()

    noisy_commits = [
        "fix logic", "improve code", "refined internal structure",
        "updated auth flow", "fix logic", "minor changes",
        "improve code", "tweaks", "update things", "clean up",
        "fix logic", "optimizations", "various changes",
        "fix logic", "Fix Redis session invalidation race during JWT refresh"
    ]

    req = PRRequest(
        title="Auth updates",
        description="Improved authentication flow and optimized performance.",
        commits=noisy_commits,
        diff="+++ b/src/auth/session.py\n+def invalidate_session(): pass\n+++ b/src/cache/redis_store.py\n+class RedisStore: pass\n"
    )

    response = service.analyze_pr(req)

    # Squash analysis
    assert response.squashAnalysis.squashRiskLevel == "high"
    assert response.squashAnalysis.duplicateMessageCount >= 1
    assert response.squashAnalysis.genericMessageCount >= 10
    assert len(response.squashAnalysis.buriedSignalMessages) >= 1
    assert "Redis" in response.squashAnalysis.buriedSignalMessages[0]
    assert len(response.squashAnalysis.squashWarnings) >= 2

    # Main branch sentry
    assert response.mainBranchSentry.isMainBranchSafe is False
    assert len(response.mainBranchSentry.failedChecks) >= 1

    # Repository memory integrity
    assert response.repositoryMemoryIntegrity.riskLevel in ["medium", "high"]
    assert response.repositoryMemoryIntegrity.score < 80

    # Recommended summary mentions covered/uncovered entities
    assert len(response.squashAnalysis.recommendedFinalSummary) > len("Auth updates")


def test_clean_squash_merge():
    """Clean commits with a strong squash message. Expect low squash risk."""
    service = AnalyzerService()

    req = PRRequest(
        title="Implement JWT session validation with Redis caching",
        description="This PR adds secure JWT session validation to prevent unauthorized access. Redis caching reduces database lookups for session tokens.",
        commits=[
            "feat: add JWT session validation to prevent expired token reuse",
            "feat: integrate Redis caching for session lookups"
        ],
        diff="+++ b/src/auth/jwt_manager.py\n+def validate_session(): pass\n+++ b/src/cache/redis_store.py\n+class RedisStore: pass\n",
        proposedSquashMessage="Implement JWT session validation with Redis caching to prevent unauthorized access and reduce DB lookups."
    )

    response = service.analyze_pr(req)

    assert response.squashAnalysis.squashRiskLevel == "low"
    assert response.squashAnalysis.duplicateMessageCount == 0
    assert response.squashAnalysis.genericMessageCount == 0
    assert len(response.squashAnalysis.buriedSignalMessages) == 0

    assert response.mainBranchSentry.isMainBranchSafe is True
    assert response.mainBranchSentry.memoryIntegrityScore >= 80

    assert response.repositoryMemoryIntegrity.riskLevel in ["low", "medium"]
    assert response.repositoryMemoryIntegrity.score >= 60


def test_api_response_contract():
    """Verify all Phase 1/2/3 fields exist in the response."""
    service = AnalyzerService()

    req = PRRequest(
        title="Test",
        description="Test description for contract validation.",
        commits=["initial commit"],
        diff="+++ b/readme.md\n+hello\n"
    )

    response = service.analyze_pr(req)

    # Phase 1/2 fields
    assert hasattr(response, "score")
    assert hasattr(response, "riskLevel")
    assert hasattr(response, "communicationCoverage")
    assert hasattr(response, "policyViolations")
    assert hasattr(response, "scoringBreakdown")
    assert hasattr(response, "genericPhrases")
    assert hasattr(response, "commitWarnings")
    assert hasattr(response, "recommendations")

    # Phase 3 fields
    assert hasattr(response, "squashAnalysis")
    assert hasattr(response, "mainBranchSentry")
    assert hasattr(response, "repositoryMemoryIntegrity")

    # Nested shapes
    assert hasattr(response.squashAnalysis, "squashRiskLevel")
    assert hasattr(response.squashAnalysis, "recommendedFinalSummary")
    assert hasattr(response.mainBranchSentry, "isMainBranchSafe")
    assert hasattr(response.repositoryMemoryIntegrity, "score")
