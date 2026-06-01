import re

class PolicyChecker:
    @staticmethod
    def _has_word(text: str, word: str) -> bool:
        return bool(re.search(rf'\b{re.escape(word)}\b', text))

    @staticmethod
    def check_policies(diff_text: str, description: str, title: str) -> list:
        text = f"{description} {title}".lower()
        diff_lower = diff_text.lower()
        violations = []
        
        # Security Auth check
        if any(kw in diff_lower for kw in ["auth", "security", "session", "jwt", "token"]):
            if not any(PolicyChecker._has_word(text, kw) for kw in ["security", "auth", "session", "token"]):
                violations.append({
                    "policy": "Security Coverage",
                    "violation": "Auth/security files changed, but PR text does not mention security/auth/session/token impact."
                })

        # Database check — match as substrings so migration_001.sql, schema_v2.sql all trigger
        if any(kw in diff_lower for kw in ["migration", "schema", "alter table", ".sql", "liquibase", "flyway"]):
            if not any(PolicyChecker._has_word(text, kw) for kw in ["migration", "rollback", "schema", "data risk", "database change"]):
                violations.append({
                    "policy": "Database Risk",
                    "violation": "Migration/schema files changed, but PR text does not contain migration/rollback/data-risk note."
                })
                
        # Dependency check
        if any(kw in diff_lower for kw in ["package.json", "requirements.txt", "go.mod"]):
            if not any(kw in text for kw in ["dependency", "package", "bump", "reason", "upgrade"]):
                violations.append({
                    "policy": "Dependency Management", 
                    "violation": "Dependency files changed, but PR text does not mention dependency reason."
                })
                
        # Config check
        if any(kw in diff_lower for kw in ["config", "env", "yaml"]):
            if not any(kw in text for kw in ["config", "deployment", "env"]):
                violations.append({
                    "policy": "Configuration Risk", 
                    "violation": "Config/env files changed, but PR text does not mention deployment/config impact."
                })
                
        # API check
        if any(kw in diff_lower for kw in ["api", "route", "controller"]):
            if not any(kw in text for kw in ["api", "contract", "endpoint", "behavior"]):
                violations.append({
                    "policy": "API Contract", 
                    "violation": "API route/controller changed, but PR text does not mention API behavior or contract impact."
                })

        return violations
