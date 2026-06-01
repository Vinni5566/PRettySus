from app.models.schemas import (
    PRRequest, PRResponse, Issue, CommunicationCoverage, PolicyViolation,
    ScoringBreakdown, BreakdownItem, SquashAnalysis, MainBranchSentry as MainBranchSentryModel,
    RepositoryMemoryIntegrity
)
from app.parsers.git_parser import GitParser
from app.analyzers.rules import AnalyzerRules
from app.analyzers.coverage_analyzer import CoverageAnalyzer
from app.analyzers.policy_checker import PolicyChecker
from app.analyzers.commit_analyzer_v2 import CommitAnalyzerV2
from app.analyzers.squash_analyzer import SquashMergeAnalyzer
from app.services.sentry_service import MainBranchSentry
from app.scoring.calculator import ScoringCalculator
from app.utils.text_utils import TextUtils

class AnalyzerService:
    @staticmethod
    def analyze_pr(pr: PRRequest) -> PRResponse:
        parsed_diff = GitParser.parse_diff(pr.diff)
        full_text = f"{pr.title} {pr.description} {' '.join(pr.commits)}"

        entities = CoverageAnalyzer.extract_entities(pr.diff)
        coverage_data = CoverageAnalyzer.calculate_coverage(entities, full_text)

        policy_violations_raw = PolicyChecker.check_policies(pr.diff, pr.description, pr.title)
        commit_analysis = CommitAnalyzerV2.analyze(pr.commits)

        generic_phrases = AnalyzerRules.find_generic_phrases(f"{pr.title} {pr.description}")
        unmentioned_files = AnalyzerRules.check_unmentioned_files(
            pr.description, pr.title, parsed_diff["changed_files"]
        )

        diff_tokens = TextUtils.extract_tokens(pr.diff)
        desc_tokens = TextUtils.extract_tokens(f"{pr.title} {pr.description}")
        missing_tokens = list(diff_tokens - desc_tokens)[:10]

        # Phase 3: Squash analysis
        squash_data = SquashMergeAnalyzer.analyze(
            commits=pr.commits,
            proposed_squash=pr.proposedSquashMessage or "",
            pr_title=pr.title,
            pr_description=pr.description,
            covered_entities=coverage_data["coveredEntities"],
            high_impact_uncovered=coverage_data["highImpactUncoveredEntities"],
            policy_violations=policy_violations_raw,
            changed_files=parsed_diff["changed_files"]
        )

        # Phase 3: Main Branch Sentry
        squash_text = pr.proposedSquashMessage or f"{pr.title}\n\n" + "\n".join(
            [f"* {c.strip()}" for c in pr.commits if c.strip()])
        sentry_data = MainBranchSentry.validate(
            squash_text=squash_text,
            high_impact_entities=coverage_data["highImpactUncoveredEntities"] + coverage_data["coveredEntities"],
            policy_violations=policy_violations_raw,
            generic_phrases=generic_phrases,
            noise_score=squash_data["squashNoiseScore"],
            pr_full_text=full_text
        )

        # Phase 2: Scoring
        score, risk, raw_issues, breakdown = ScoringCalculator.calculate_score(
            parsed_diff, generic_phrases, unmentioned_files,
            commit_analysis["score"], pr.description, policy_violations_raw, coverage_data
        )

        issues = [Issue(**issue) for issue in raw_issues]
        p_violations = [PolicyViolation(**pv) for pv in policy_violations_raw]

        s_breakdown = ScoringBreakdown(
            communicationCoverage=BreakdownItem(**breakdown["communicationCoverage"]),
            specificity=BreakdownItem(**breakdown["specificity"]),
            criticalPolicies=BreakdownItem(**breakdown["criticalPolicies"]),
            commitQuality=BreakdownItem(**breakdown["commitQuality"]),
            diffTextBalance=BreakdownItem(**breakdown["diffTextBalance"])
        )

        # Phase 3: Repository Memory Integrity
        rmi_score = int(
            (coverage_data["weightedPercentage"] * 0.3) +
            ((100 - squash_data["squashNoiseScore"]) * 0.25) +
            (commit_analysis["score"] * 0.15) +
            (sentry_data["memoryIntegrityScore"] * 0.2) +
            ((100 - len(generic_phrases) * 10) * 0.1)
        )
        rmi_score = max(0, min(100, rmi_score))

        if rmi_score >= 80:
            rmi_risk = "low"
        elif rmi_score >= 50:
            rmi_risk = "medium"
        else:
            rmi_risk = "high"

        rmi_signals = []
        if squash_data["squashNoiseScore"] > 40:
            rmi_signals.append(f"High squash noise ({squash_data['squashNoiseScore']}%)")
        if not sentry_data["isMainBranchSafe"]:
            rmi_signals.append("Main branch sentry: UNSAFE")
        if coverage_data["weightedPercentage"] < 50:
            rmi_signals.append(f"Low communication coverage ({coverage_data['weightedPercentage']}%)")
        if p_violations:
            rmi_signals.append(f"{len(p_violations)} policy violations")

        rmi_explanation = (
            f"Repository memory integrity is {rmi_risk}. "
            f"Coverage: {coverage_data['weightedPercentage']}%, "
            f"Squash noise: {squash_data['squashNoiseScore']}%, "
            f"Sentry: {'SAFE' if sentry_data['isMainBranchSafe'] else 'UNSAFE'}."
        )

        recommendations = []
        if generic_phrases:
            recommendations.append("Avoid generic phrases. Describe 'what' and 'why' specifically.")
        if p_violations:
            recommendations.append("Address critical policy violations by explaining impact.")
        if commit_analysis["warnings"]:
            recommendations.append("Provide meaningful commit messages without duplication.")
        if squash_data["squashRiskLevel"] == "high":
            recommendations.append("Write a dedicated squash summary before merging to preserve history.")
        if not sentry_data["isMainBranchSafe"]:
            recommendations.append("Fix sentry failures before merging to main branch.")
        if score < 50:
            recommendations.append("Consider breaking down this PR or adding a comprehensive technical summary.")

        summary = f"PR contains {parsed_diff['total_changes']} line changes across {len(parsed_diff['changed_files'])} files."

        return PRResponse(
            score=score,
            riskLevel=risk,
            summary=summary,
            communicationCoverage=CommunicationCoverage(**coverage_data),
            policyViolations=p_violations,
            scoringBreakdown=s_breakdown,
            issues=issues,
            genericPhrases=generic_phrases,
            commitWarnings=commit_analysis["warnings"],
            duplicateCommitClusters=commit_analysis["clusters"],
            recommendations=recommendations,
            squashAnalysis=SquashAnalysis(**squash_data),
            mainBranchSentry=MainBranchSentryModel(**sentry_data),
            repositoryMemoryIntegrity=RepositoryMemoryIntegrity(
                score=rmi_score, riskLevel=rmi_risk,
                explanation=rmi_explanation, signals=rmi_signals
            )
        )
