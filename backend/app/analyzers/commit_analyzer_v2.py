from app.analyzers.rules import AnalyzerRules

class CommitAnalyzerV2:
    @staticmethod
    def analyze(commits: list) -> dict:
        warnings = []
        clusters = []
        
        seen = {}
        for c in commits:
            if not c.strip(): continue
            ct = c.strip().lower()
            seen[ct] = seen.get(ct, 0) + 1
            
        for ct, count in seen.items():
            if count > 1:
                clusters.append([c for c in commits if c.strip().lower() == ct])
                
        for commit in commits:
            c_clean = commit.strip()
            if not c_clean: continue
            
            generic = AnalyzerRules.find_generic_phrases(c_clean)
            if generic:
                warnings.append(f"Commit '{c_clean[:30]}...' contains generic verbs: {', '.join(generic)}")
            elif len(c_clean.split()) < 3:
                warnings.append(f"Commit '{c_clean[:30]}...' is too short or likely squash-noise.")
                
        score = 100
        score -= len(warnings) * 10
        score -= len(clusters) * 15
        
        return {
            "score": max(0, score),
            "warnings": warnings,
            "clusters": clusters
        }
