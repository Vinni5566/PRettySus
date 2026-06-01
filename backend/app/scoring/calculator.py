class ScoringCalculator:
    @staticmethod
    def calculate_score(parsed_diff, generic_phrases, unmentioned_files, commit_quality_score, description, policy_violations, coverage_data):
        score = 100
        issues = []
        
        # Communication Coverage (Weight: 35)
        cov_score = coverage_data["weightedPercentage"]
        cov_weight = 35
        cov_contribution = int(cov_score * (cov_weight / 100))
        score -= (cov_weight - cov_contribution)
        
        # Specificity (Weight: 20)
        spec_score = 100
        if generic_phrases:
            spec_score -= len(generic_phrases) * 15
            issues.append({"type": "generic_language", "description": f"Found {len(generic_phrases)} generic phrases."})
        if unmentioned_files:
            spec_score -= len(unmentioned_files) * 10
            issues.append({"type": "missing_context", "description": f"{len(unmentioned_files)} changed files not mentioned in description."})
        spec_score = max(0, spec_score)
        spec_contribution = int(spec_score * (20 / 100))
        score -= (20 - spec_contribution)
        
        # Critical Policies (Weight: 25)
        pol_score = 100
        if policy_violations:
            pol_score -= len(policy_violations) * 30
        pol_score = max(0, pol_score)
        pol_contribution = int(pol_score * (25 / 100))
        score -= (25 - pol_contribution)
        
        # Commit Quality (Weight: 10)
        cq_score = commit_quality_score
        cq_contribution = int(cq_score * (10 / 100))
        score -= (10 - cq_contribution)
        
        # Diff-Text Balance (Weight: 10)
        desc_word_count = len(description.split()) if description else 0
        bal_score = 100
        if parsed_diff["total_changes"] > 50 and desc_word_count < 20:
            bal_score -= 50
            issues.append({"type": "insufficient_detail", "description": "Large diff requires more detailed explanation."})
        if desc_word_count < 5:
            bal_score -= 50
            issues.append({"type": "missing_description", "description": "Description is missing or extremely short."})
        bal_contribution = int(bal_score * (10 / 100))
        score -= (10 - bal_contribution)
        
        score = max(0, min(100, score))
        
        if score >= 80:
            risk = "low"
        elif score >= 50:
            risk = "medium"
        else:
            risk = "high"
            
        breakdown = {
            "communicationCoverage": {"score": cov_score, "weight": 35, "reason": "Measures coverage of weighted tech entities"},
            "specificity": {"score": spec_score, "weight": 20, "reason": "Penalty for generic filler or omitted files"},
            "criticalPolicies": {"score": pol_score, "weight": 25, "reason": f"{len(policy_violations)} policy violations"},
            "commitQuality": {"score": cq_score, "weight": 10, "reason": "Commit message clarity and uniqueness"},
            "diffTextBalance": {"score": bal_score, "weight": 10, "reason": "Description size relative to diff size"}
        }
            
        return score, risk, issues, breakdown
