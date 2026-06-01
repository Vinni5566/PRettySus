from pydantic import BaseModel
from typing import List, Optional

class PRRequest(BaseModel):
    title: str
    description: str
    commits: List[str]
    diff: str
    proposedSquashMessage: Optional[str] = None

class Issue(BaseModel):
    type: str
    description: str

class CommunicationCoverage(BaseModel):
    percentage: int
    weightedPercentage: int
    coveredEntities: List[str]
    uncoveredEntities: List[str]
    highImpactUncoveredEntities: List[str]

class PolicyViolation(BaseModel):
    policy: str
    violation: str

class BreakdownItem(BaseModel):
    score: int
    weight: int
    reason: str

class ScoringBreakdown(BaseModel):
    communicationCoverage: BreakdownItem
    specificity: BreakdownItem
    criticalPolicies: BreakdownItem
    commitQuality: BreakdownItem
    diffTextBalance: BreakdownItem

class SquashAnalysis(BaseModel):
    squashRiskLevel: str
    squashNoiseScore: int
    duplicateMessageCount: int
    genericMessageCount: int
    buriedSignalMessages: List[str]
    noisyMessages: List[str]
    recommendedFinalSummary: str
    squashWarnings: List[str]

class MainBranchSentry(BaseModel):
    isMainBranchSafe: bool
    memoryIntegrityScore: int
    failedChecks: List[str]
    passedChecks: List[str]
    historyRiskExplanation: str

class RepositoryMemoryIntegrity(BaseModel):
    score: int
    riskLevel: str
    explanation: str
    signals: List[str]

class PRResponse(BaseModel):
    score: int
    riskLevel: str
    summary: str
    communicationCoverage: CommunicationCoverage
    policyViolations: List[PolicyViolation]
    scoringBreakdown: ScoringBreakdown
    issues: List[Issue]
    genericPhrases: List[str]
    commitWarnings: List[str]
    duplicateCommitClusters: List[List[str]]
    recommendations: List[str]
    squashAnalysis: SquashAnalysis
    mainBranchSentry: MainBranchSentry
    repositoryMemoryIntegrity: RepositoryMemoryIntegrity
