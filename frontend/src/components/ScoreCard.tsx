import { PRResponse } from '../types';
import { AlertCircle, ShieldAlert, GitCommit, Target, AlertTriangle, Layers, GitMerge, FileText, Database } from 'lucide-react';

interface Props {
  result: PRResponse;
}

export default function ScoreCard({ result }: Props) {
  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'low': return 'text-[#3fb950] border-[#3fb950]';
      case 'medium': return 'text-[#d29922] border-[#d29922]';
      case 'high': return 'text-[#f85149] border-[#f85149]';
      default: return 'text-white border-white';
    }
  };

  const getCoverageColor = (cov: number) => {
    if (cov >= 80) return 'text-[#3fb950]';
    if (cov >= 50) return 'text-[#d29922]';
    return 'text-[#f85149]';
  };

  return (
    <div className="flex flex-col gap-6">
      
      {/* 0. Repository Memory Integrity */}
      {result.repositoryMemoryIntegrity && (
        <div className={`border rounded-lg p-6 bg-[#010409] ${getRiskColor(result.repositoryMemoryIntegrity.riskLevel)} border-l-4`}>
           <div className="flex items-center gap-3 mb-2">
             <Database size={24} />
             <h2 className="text-2xl font-bold uppercase tracking-wide">Repository Memory Integrity Score: {result.repositoryMemoryIntegrity.score}</h2>
           </div>
           <p className="text-sm text-[#8b949e] mb-3">{result.repositoryMemoryIntegrity.explanation}</p>
           <div className="flex flex-wrap gap-2 mt-2">
             {result.repositoryMemoryIntegrity.signals.map((sig, i) => (
                <span key={i} className="px-2 py-1 bg-[#21262d] text-[#c9d1d9] border border-[#30363d] rounded text-xs">
                  {sig}
                </span>
             ))}
           </div>
        </div>
      )}

      {/* 1. Main Branch Sentry */}
      {result.mainBranchSentry && (
        <div className={`border rounded-lg p-5 flex flex-col gap-3 ${result.mainBranchSentry.isMainBranchSafe ? 'border-[#3fb950] bg-[#3fb950] bg-opacity-10' : 'border-[#f85149] bg-[#f85149] bg-opacity-10'}`}>
          <h3 className={`font-semibold flex items-center gap-2 ${result.mainBranchSentry.isMainBranchSafe ? 'text-[#3fb950]' : 'text-[#ff7b72]'}`}>
            <ShieldAlert size={18} /> Main Branch Sentry: {result.mainBranchSentry.isMainBranchSafe ? 'SAFE TO MERGE' : 'UNSAFE FOR MAIN BRANCH'}
          </h3>
          <p className="text-sm text-[#c9d1d9]">{result.mainBranchSentry.historyRiskExplanation}</p>
          {result.mainBranchSentry.failedChecks.length > 0 && (
            <ul className="flex flex-col gap-1 mt-2">
              {result.mainBranchSentry.failedChecks.map((fail, i) => (
                 <li key={i} className="text-sm text-[#ff7b72] flex items-center gap-2">
                   <AlertTriangle size={14} /> {fail}
                 </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {/* 2. Main Score and Coverage Map */}
      <div className="grid grid-cols-2 gap-4">
        <div className={`border rounded-lg p-6 flex flex-col items-center justify-center bg-[#161b22] ${getRiskColor(result.riskLevel)}`}>
          <div className="text-5xl font-bold mb-1">{result.score}</div>
          <div className="text-sm font-medium uppercase tracking-wider">Base PR Score ({result.riskLevel})</div>
        </div>
        
        <div className="border border-[#30363d] rounded-lg p-6 flex flex-col items-center justify-center bg-[#161b22]">
          <div className={`text-5xl font-bold mb-1 flex items-center gap-2 ${getCoverageColor(result.communicationCoverage.weightedPercentage)}`}>
            {result.communicationCoverage.weightedPercentage}%
          </div>
          <div className="text-sm font-medium text-[#8b949e] uppercase tracking-wider flex items-center gap-1">
            <Target size={14}/> Communication Coverage
          </div>
        </div>
      </div>

      {/* 3. Squash Risk Visualization */}
      {result.squashAnalysis && (
        <div className="bg-[#0d1117] border border-[#30363d] rounded-lg p-5 flex flex-col gap-4">
           <h3 className="text-white font-semibold flex items-center gap-2">
             <GitMerge size={18} className="text-[#a371f7]" /> Squash Merge Risk
           </h3>
           <div className="grid grid-cols-3 gap-4 mb-2">
              <div className="bg-[#161b22] border border-[#30363d] p-3 rounded">
                <div className="text-xs text-[#8b949e] uppercase">Squash Noise</div>
                <div className="text-lg font-bold text-[#f85149]">{result.squashAnalysis.squashNoiseScore}%</div>
              </div>
              <div className="bg-[#161b22] border border-[#30363d] p-3 rounded">
                <div className="text-xs text-[#8b949e] uppercase">Duplicate Commits</div>
                <div className="text-lg font-bold text-[#d29922]">{result.squashAnalysis.duplicateMessageCount}</div>
              </div>
              <div className="bg-[#161b22] border border-[#30363d] p-3 rounded">
                <div className="text-xs text-[#8b949e] uppercase">Generic Commits</div>
                <div className="text-lg font-bold text-[#d29922]">{result.squashAnalysis.genericMessageCount}</div>
              </div>
           </div>
           
           {result.squashAnalysis.buriedSignalMessages.length > 0 && (
             <div className="mt-2">
                <h4 className="text-xs font-bold text-[#58a6ff] uppercase mb-2">💎 Buried Signal Detected</h4>
                <p className="text-xs text-[#c9d1d9] mb-2">These high-value commits will be lost in squash noise:</p>
                <ul className="flex flex-col gap-1">
                  {result.squashAnalysis.buriedSignalMessages.map((msg, i) => (
                    <li key={i} className="text-sm text-[#58a6ff] bg-[#161b22] p-2 rounded font-mono border border-[#58a6ff] border-opacity-30">
                      {msg}
                    </li>
                  ))}
                </ul>
             </div>
           )}

           {/* Deterministic Suggested Summary */}
           <div className="mt-4 pt-4 border-t border-[#30363d]">
             <h4 className="text-xs font-bold text-[#3fb950] uppercase mb-2 flex items-center gap-1">
               <FileText size={14} /> Deterministic Suggested Summary
             </h4>
             <p className="text-xs text-[#8b949e] mb-2 italic">Generated entirely without AI using diff analysis and high-impact coverage maps.</p>
             <pre className="bg-[#010409] border border-[#30363d] text-[#c9d1d9] text-xs p-3 rounded whitespace-pre-wrap font-mono">
               {result.squashAnalysis.recommendedFinalSummary}
             </pre>
           </div>
        </div>
      )}

      {/* 4. Critical Policy Violations */}
      {result.policyViolations.length > 0 && (
        <div className="bg-[#f85149] bg-opacity-10 border border-[#f85149] rounded-lg p-5">
          <h3 className="text-[#ff7b72] font-semibold flex items-center gap-2 mb-4">
            <ShieldAlert size={18} /> Critical Policy Violations
          </h3>
          <ul className="flex flex-col gap-3">
            {result.policyViolations.map((pv, idx) => (
              <li key={idx} className="flex gap-3 text-sm text-[#ff7b72] items-start bg-[#161b22] p-3 rounded">
                <AlertTriangle size={16} className="mt-0.5 shrink-0" />
                <div>
                  <span className="font-semibold capitalize mr-2">{pv.policy}:</span>
                  {pv.violation}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 5. Coverage Entities List */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-lg p-5 flex flex-col gap-4">
        <h3 className="text-white font-semibold flex items-center gap-2">
          <Layers size={18} className="text-[#58a6ff]" /> Code Entities Coverage Map
        </h3>
        
        {result.communicationCoverage.highImpactUncoveredEntities.length > 0 && (
          <div>
            <h4 className="text-xs font-bold text-[#ff7b72] uppercase mb-2">🚨 High-Impact Missing Explanations</h4>
            <div className="flex flex-wrap gap-2">
              {result.communicationCoverage.highImpactUncoveredEntities.map((ent, i) => (
                <span key={i} className="px-2 py-1 bg-[#f85149] bg-opacity-20 text-[#ff7b72] border border-[#f85149] rounded text-xs font-mono font-bold">{ent}</span>
              ))}
            </div>
          </div>
        )}
        
        {result.communicationCoverage.uncoveredEntities.length > 0 && (
          <div>
            <h4 className="text-xs font-medium text-[#8b949e] uppercase mb-2">Uncovered Code Entities</h4>
            <div className="flex flex-wrap gap-2">
              {result.communicationCoverage.uncoveredEntities.filter(e => !result.communicationCoverage.highImpactUncoveredEntities.includes(e)).map((ent, i) => (
                <span key={i} className="px-2 py-1 bg-[#21262d] text-[#d29922] border border-[#30363d] rounded text-xs font-mono">{ent}</span>
              ))}
            </div>
          </div>
        )}

        {result.communicationCoverage.coveredEntities.length > 0 && (
          <div>
            <h4 className="text-xs font-medium text-[#8b949e] uppercase mb-2">Covered Entities</h4>
            <div className="flex flex-wrap gap-2">
              {result.communicationCoverage.coveredEntities.map((ent, i) => (
                <span key={i} className="px-2 py-1 bg-[#21262d] text-[#3fb950] border border-[#30363d] rounded text-xs font-mono">{ent}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 6. Commit Quality */}
      {(result.commitWarnings.length > 0 || result.duplicateCommitClusters.length > 0) && (
        <div className="bg-[#0d1117] border border-[#30363d] rounded-lg p-5">
          <h3 className="text-white font-semibold flex items-center gap-2 mb-4">
            <GitCommit size={18} className="text-[#a371f7]" /> Commit Quality
          </h3>
          <ul className="flex flex-col gap-2">
            {result.commitWarnings.map((warn, i) => (
              <li key={i} className="text-sm text-[#c9d1d9] flex gap-2"><AlertCircle size={14} className="text-[#d29922] mt-1 shrink-0"/>{warn}</li>
            ))}
            {result.duplicateCommitClusters.map((cluster, i) => (
              <li key={`dup-${i}`} className="text-sm text-[#c9d1d9] flex gap-2"><AlertTriangle size={14} className="text-[#f85149] mt-1 shrink-0"/>Duplicate cluster detected: {cluster.length} commits identical to "{cluster[0]}"</li>
            ))}
          </ul>
        </div>
      )}

      {/* 7. Scoring Breakdown */}
      <div className="bg-[#0d1117] border border-[#30363d] rounded-lg p-5">
        <h3 className="text-white font-semibold flex items-center gap-2 mb-4">
          📊 Base Scoring Breakdown
        </h3>
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-[#8b949e] uppercase border-b border-[#30363d]">
            <tr>
              <th className="py-2">Metric</th>
              <th className="py-2">Score</th>
              <th className="py-2">Weight</th>
              <th className="py-2">Reason</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#30363d] text-[#c9d1d9]">
            {Object.entries(result.scoringBreakdown).map(([key, item]) => (
              <tr key={key}>
                <td className="py-2 capitalize font-medium">{key.replace(/([A-Z])/g, ' $1').trim()}</td>
                <td className="py-2 font-mono">{item.score} / 100</td>
                <td className="py-2">{item.weight}%</td>
                <td className="py-2 text-[#8b949e]">{item.reason}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}
