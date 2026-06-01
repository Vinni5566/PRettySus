class AnalyzerRules:
    GENERIC_PHRASES = [
        "fix logic", "improve code", "refined internal structure", "minor changes", 
        "update things", "refactor", "bug fix", "fixes", "updates", "optimizations",
        "optimized performance", "clean up", "tweaks", "various changes"
    ]
    
    @staticmethod
    def find_generic_phrases(text: str) -> list:
        if not text:
            return []
        text_lower = text.lower()
        found = []
        for phrase in AnalyzerRules.GENERIC_PHRASES:
            if phrase in text_lower:
                found.append(phrase)
        return found
        
    @staticmethod
    def check_unmentioned_files(description: str, title: str, files: list) -> list:
        text = f"{description} {title}".lower()
        unmentioned = []
        for file in files:
            base_name = file.split('/')[-1].split('.')[0].lower()
            base_name_clean = base_name.replace('_', ' ').replace('-', ' ')
            if base_name and base_name not in text and base_name_clean not in text:
                unmentioned.append(file)
        return unmentioned

    @staticmethod
    def analyze_commit_quality(commits: list) -> list:
        warnings = []
        for commit in commits:
            if not commit.strip():
                continue
            generic = AnalyzerRules.find_generic_phrases(commit)
            if generic:
                warnings.append(f"Commit '{commit[:30]}...' contains generic phrases: {', '.join(generic)}")
            elif len(commit.split()) < 3:
                warnings.append(f"Commit '{commit[:30]}...' is too short.")
        return warnings
