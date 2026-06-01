class GitParser:
    @staticmethod
    def parse_diff(diff_text: str) -> dict:
        """Parses a raw git diff to extract files changed, additions, and deletions."""
        changed_files = []
        additions = 0
        deletions = 0
        
        if not diff_text:
            return {"changed_files": [], "additions": 0, "deletions": 0, "total_changes": 0}

        for line in diff_text.splitlines():
            if line.startswith("+++ b/"):
                changed_files.append(line[6:])
            elif line.startswith("+") and not line.startswith("+++"):
                additions += 1
            elif line.startswith("-") and not line.startswith("---"):
                deletions += 1
                
        return {
            "changed_files": changed_files,
            "additions": additions,
            "deletions": deletions,
            "total_changes": additions + deletions
        }
