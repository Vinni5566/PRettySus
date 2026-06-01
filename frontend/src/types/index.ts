export interface PRRequest {
  title: string;
  description: string;
  commits: string[];
  diff: string;
  proposedSquashMessage?: string;
}

export interface Issue {
  type: string;
  description: string;
}

export interface CommunicationCoverage {
  percentage: number;
  weightedPercentage: number;
  coveredEntities: string[];
  uncoveredEntities: string[];
  highImpactUncoveredEntities: string[];
}

export interface PolicyViolation {
  policy: string;
  violation: string;
}

export interface BreakdownItem {
  score: number;
  weight: number;
  reason: string;
}

export interface ScoringBreakdown {
  communicationCoverage: BreakdownItem;
  specificity: BreakdownItem;
  criticalPolicies: BreakdownItem;
  commitQuality: BreakdownItem;
  diffTextBalance: BreakdownItem;
}

export interface SquashAnalysis {
  squashRiskLevel: 'low' | 'medium' | 'high';
  squashNoiseScore: number;
  duplicateMessageCount: number;
  genericMessageCount: number;
  buriedSignalMessages: string[];
  noisyMessages: string[];
  recommendedFinalSummary: string;
  squashWarnings: string[];
}

export interface MainBranchSentry {
  isMainBranchSafe: boolean;
  memoryIntegrityScore: number;
  failedChecks: string[];
  passedChecks: string[];
  historyRiskExplanation: string;
}

export interface RepositoryMemoryIntegrity {
  score: number;
  riskLevel: 'low' | 'medium' | 'high';
  explanation: string;
  signals: string[];
}

export interface PRResponse {
  score: number;
  riskLevel: 'low' | 'medium' | 'high';
  summary: string;
  communicationCoverage: CommunicationCoverage;
  policyViolations: PolicyViolation[];
  scoringBreakdown: ScoringBreakdown;
  issues: Issue[];
  missingTokens: string[];
  genericPhrases: string[];
  commitWarnings: string[];
  duplicateCommitClusters: string[][];
  recommendations: string[];
  squashAnalysis: SquashAnalysis;
  mainBranchSentry: MainBranchSentry;
  repositoryMemoryIntegrity: RepositoryMemoryIntegrity;
}
