import re

class CoverageAnalyzer:
    HIGH_IMPACT_CATEGORIES = {
        "auth": ["auth", "security", "session", "token", "jwt", "login", "logout", "redis"],
        "database": ["migration", "schema", "sql", "cache", "flyway", "liquibase"],
        "api": ["api", "route", "controller", "handler", "endpoint"],
        "config": ["config", "docker", "requirements", "package"],
        "payment": ["payment", "billing", "invoice", "checkout"]
    }

    # Low-signal tokens that appear in almost any diff and should not count against coverage
    _NOISE_TOKENS = {
        "pass", "return", "self", "none", "true", "false", "import",
        "from", "class", "function", "const", "async", "await",
        "raise", "except", "elif", "else", "with", "yield"
    }
    
    @staticmethod
    def extract_entities(diff_text: str) -> list:
        entities = set()
        if not diff_text:
            return []

        for line in diff_text.splitlines():
            if line.startswith("+++ b/"):
                file_path = line[6:]
                # Add each directory component and the base filename (without extension)
                parts = [p for p in file_path.split("/") if p]
                entities.update(parts)
                base_stem = parts[-1].rsplit('.', 1)[0] if parts else ""
                if base_stem:
                    entities.add(base_stem)
            elif line.startswith("+") and not line.startswith("+++"):
                words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', line)
                # Only keep meaningful tokens: length > 5, not pure noise, not all lowercase single-word noise
                for w in words:
                    if len(w) > 5 and w.lower() not in CoverageAnalyzer._NOISE_TOKENS:
                        entities.add(w)
        return list(entities)
        
    @staticmethod
    def calculate_coverage(entities: list, text: str) -> dict:
        text_lower = text.lower()
        covered = []
        uncovered = []
        high_impact_uncovered = []
        
        total_weight = 0
        covered_weight = 0
        
        for entity in set(entities):
            if not entity: continue
            
            ent_lower = entity.lower()
            is_high_impact = False
            for cat, keywords in CoverageAnalyzer.HIGH_IMPACT_CATEGORIES.items():
                if any(kw == ent_lower or f"{kw}_" in ent_lower or f"_{kw}" in ent_lower for kw in keywords):
                    is_high_impact = True
                    break
                    
            weight = 5 if is_high_impact else 1
            total_weight += weight
            
            clean_ent = ent_lower.replace('_', ' ')
            if ent_lower in text_lower or clean_ent in text_lower:
                covered.append(entity)
                covered_weight += weight
            else:
                uncovered.append(entity)
                if is_high_impact:
                    high_impact_uncovered.append(entity)
                    
        perc = int((len(covered) / len(entities) * 100)) if entities else 100
        w_perc = int((covered_weight / total_weight * 100)) if total_weight > 0 else 100
        
        return {
            "percentage": perc,
            "weightedPercentage": w_perc,
            "coveredEntities": covered,
            "uncoveredEntities": uncovered,
            "highImpactUncoveredEntities": high_impact_uncovered
        }
