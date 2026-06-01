import re

class TextUtils:
    @staticmethod
    def extract_tokens(text: str) -> set:
        """Extracts technical tokens (words > 4 chars containing alphanumeric and underscores)."""
        if not text:
            return set()
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text)
        return set([w for w in words if len(w) > 4])
