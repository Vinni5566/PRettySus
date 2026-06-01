from app.analyzers.rules import AnalyzerRules

class MainBranchSentry:
    INTENT_MARKERS = [
        "because", "to prevent", "to support", "due to", "fixes",
        "avoids", "enables", "required for", "so that", "in order to",
        "resolves", "addresses", "prevents", "ensures"
    ]

    @staticmethod
    def validate(squash_text: str, high_impact_entities: list,
                 policy_violations: list, generic_phrases: list,
                 noise_score: int, pr_full_text: str = "") -> dict:
        # Validate against the full PR context: squash message + title + description
        combined_text = f"{squash_text} {pr_full_text}".lower()
        text_lower = squash_text.lower() if squash_text else ""
        checks_passed = []
        checks_failed = []

        # Check 1: Not mostly duplicate/repetitive text
        lines = [l.strip() for l in squash_text.splitlines() if l.strip()] if squash_text else []
        unique_lines = set(lines)
        if len(lines) > 0 and len(unique_lines) / len(lines) < 0.5:
            checks_failed.append("Final message is mostly duplicate text.")
        else:
            checks_passed.append("Message text is not overly repetitive.")

        # Check 2: Mentions high-impact entities (checked against full PR context)
        mentioned = 0
        for e in high_impact_entities:
            e_lower = e.lower()
            e_clean = e_lower.replace('_', ' ')
            if e_lower in combined_text or e_clean in combined_text:
                mentioned += 1
        threshold = max(1, len(high_impact_entities) // 4)  # 25% threshold — squash messages summarize
        if high_impact_entities and mentioned < threshold:
            checks_failed.append(f"Only {mentioned}/{len(high_impact_entities)} high-impact entities referenced in PR text.")
        else:
            checks_passed.append("High-impact entities are referenced.")

        # Check 3: Contains at least one intent marker
        has_intent = any(m in text_lower for m in MainBranchSentry.INTENT_MARKERS)
        if not has_intent:
            checks_failed.append("No intent/reason markers found (because, fixes, to prevent, etc).")
        else:
            checks_passed.append("Contains intent/reason markers.")

        # Check 4: Not dominated by generic phrases
        generics = AnalyzerRules.find_generic_phrases(squash_text)
        words = squash_text.split() if squash_text else []
        generic_word_count = sum(len(g.split()) for g in generics)
        if words and generic_word_count / max(len(words), 1) > 0.4:
            checks_failed.append("Message is dominated by generic filler phrases.")
        else:
            checks_passed.append("Message is not dominated by generic filler.")

        # Check 5: Noise threshold
        if noise_score > 60:
            checks_failed.append(f"Squash noise score is {noise_score}/100 (threshold: 60).")
        else:
            checks_passed.append("Squash noise is within acceptable range.")

        # Check 6: Policy coverage
        if policy_violations:
            pv_types = [pv.get("policy", "") if isinstance(pv, dict) else pv.policy for pv in policy_violations]
            checks_failed.append(f"Unaddressed policy violations: {', '.join(pv_types)}")
        else:
            checks_passed.append("No critical policy violations.")

        is_safe = len(checks_failed) == 0
        integrity = max(0, 100 - len(checks_failed) * 20)

        if checks_failed:
            explanation = f"This merge message fails {len(checks_failed)} safety checks. Merging risks corrupting main branch history for future engineers and AI code search."
        else:
            explanation = "This merge message preserves engineering context and is safe for main branch history."

        return {
            "isMainBranchSafe": is_safe,
            "memoryIntegrityScore": integrity,
            "failedChecks": checks_failed,
            "passedChecks": checks_passed,
            "historyRiskExplanation": explanation
        }
