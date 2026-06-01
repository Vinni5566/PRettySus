from app.analyzers.rules import AnalyzerRules

class SquashMergeAnalyzer:
    INTENT_MARKERS = [
        "because", "to prevent", "to support", "due to", "fixes",
        "avoids", "enables", "required for", "so that", "in order to"
    ]

    @staticmethod
    def _near_duplicate(a: str, b: str) -> bool:
        wa = set(a.lower().split())
        wb = set(b.lower().split())
        if not wa or not wb:
            return False
        overlap = len(wa & wb) / max(len(wa), len(wb))
        return overlap > 0.7

    @staticmethod
    def analyze(commits: list, proposed_squash: str, pr_title: str,
                pr_description: str, covered_entities: list,
                high_impact_uncovered: list, policy_violations: list,
                changed_files: list) -> dict:

        if not commits:
            return {
                "squashRiskLevel": "low", "squashNoiseScore": 0,
                "duplicateMessageCount": 0, "genericMessageCount": 0,
                "buriedSignalMessages": [], "noisyMessages": [],
                "recommendedFinalSummary": pr_title, "squashWarnings": []
            }

        # Duplicate detection
        seen = {}
        for c in commits:
            ct = c.strip().lower()
            if ct:
                seen[ct] = seen.get(ct, 0) + 1
        dup_count = sum(1 for v in seen.values() if v > 1)

        # Near-duplicate detection
        unique_msgs = list(seen.keys())
        near_dup_pairs = 0
        for i in range(len(unique_msgs)):
            for j in range(i + 1, len(unique_msgs)):
                if SquashMergeAnalyzer._near_duplicate(unique_msgs[i], unique_msgs[j]):
                    near_dup_pairs += 1

        # Generic message detection
        generic_count = 0
        noisy = []
        signal = []
        for c in commits:
            ct = c.strip()
            if not ct:
                continue
            generics = AnalyzerRules.find_generic_phrases(ct)
            if generics or len(ct.split()) < 4:
                generic_count += 1
                noisy.append(ct)
            else:
                signal.append(ct)

        # Buried signal: meaningful commits among mostly noisy ones
        buried = []
        if noisy and signal and len(noisy) > len(signal) * 2:
            buried = signal

        # Squash noise score
        total = max(len(commits), 1)
        noise_ratio = (generic_count + dup_count + near_dup_pairs) / total
        noise_score = min(100, int(noise_ratio * 100))

        # Build squash text for sentry validation
        squash_text = proposed_squash or f"{pr_title}\n\n" + "\n".join(
            [f"* {c.strip()}" for c in commits if c.strip()])

        # Warnings
        warnings = []
        if dup_count > 0:
            warnings.append(f"{dup_count} duplicate commit messages detected.")
        if near_dup_pairs > 0:
            warnings.append(f"{near_dup_pairs} near-duplicate commit pairs found.")
        if generic_count > len(commits) * 0.5:
            warnings.append(f"{generic_count}/{len(commits)} commits are generic or too short.")
        if buried:
            warnings.append(f"{len(buried)} high-signal commits buried under {len(noisy)} noisy messages.")
        if len(commits) > 10 and not proposed_squash:
            warnings.append("10+ commits without a proposed squash summary risks history corruption.")

        # Risk level
        if noise_score >= 60 or (buried and dup_count > 2):
            risk = "high"
        elif noise_score >= 30 or dup_count > 0:
            risk = "medium"
        else:
            risk = "low"

        # Deterministic recommended summary
        summary_parts = [pr_title]
        if high_impact_uncovered:
            summary_parts.append(f"Changes: {', '.join(high_impact_uncovered[:5])}")
        if covered_entities:
            summary_parts.append(f"Covers: {', '.join(covered_entities[:5])}")
        if policy_violations:
            summary_parts.append(f"Policy notes: {'; '.join([pv.get('violation', pv.get('policy', ''))[:60] for pv in policy_violations[:3]])}")
        if buried:
            summary_parts.append(f"Key commits: {'; '.join(buried[:3])}")
        if changed_files:
            summary_parts.append(f"Files: {', '.join(changed_files[:5])}")

        recommended = "\n".join(summary_parts)

        return {
            "squashRiskLevel": risk,
            "squashNoiseScore": noise_score,
            "duplicateMessageCount": dup_count,
            "genericMessageCount": generic_count,
            "buriedSignalMessages": buried,
            "noisyMessages": noisy[:10],
            "recommendedFinalSummary": recommended,
            "squashWarnings": warnings
        }
