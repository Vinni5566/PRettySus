import { useState } from 'react';
import InputForm from '../components/InputForm';
import ScoreCard from '../components/ScoreCard';
import { analyzePR, getMarkdownReport } from '../services/api';
import { PRRequest, PRResponse } from '../types';
import { Download, Copy, Check } from 'lucide-react';

export default function Dashboard() {
  const [result, setResult] = useState<PRResponse | null>(null);
  const [lastRequest, setLastRequest] = useState<PRRequest | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  const handleAnalyze = async (data: PRRequest) => {
    setIsLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await analyzePR(data);
      setResult(res);
      setLastRequest(data);
    } catch (err: any) {
      setError(err.message || 'An error occurred during analysis.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDownloadJSON = () => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'prettysus-report.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleCopyMarkdown = async () => {
    if (!lastRequest) return;
    try {
      const res = await getMarkdownReport(lastRequest);
      await navigator.clipboard.writeText(res.markdown);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      alert("Failed to copy markdown report");
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div>
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-2">Analyze Pull Request</h2>
          <p className="text-[#8b949e]">
            Paste your PR details below. PRettySus will evaluate the communication quality deterministically against the provided Git diff.
          </p>
        </div>
        <InputForm onSubmit={handleAnalyze} isLoading={isLoading} />
        {error && (
          <div className="mt-4 p-4 bg-[#f85149] bg-opacity-10 border border-[#f85149] text-[#ff7b72] rounded-md">
            {error}
          </div>
        )}
      </div>

      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Analysis Results</h2>
          {result && (
            <div className="flex gap-2">
              <button 
                onClick={handleCopyMarkdown}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-[#21262d] hover:bg-[#30363d] border border-[#30363d] rounded text-sm text-[#c9d1d9] transition-colors"
              >
                {copied ? <Check size={14} className="text-[#3fb950]"/> : <Copy size={14} />}
                {copied ? 'Copied!' : 'Copy Markdown'}
              </button>
              <button 
                onClick={handleDownloadJSON}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-[#21262d] hover:bg-[#30363d] border border-[#30363d] rounded text-sm text-[#c9d1d9] transition-colors"
              >
                <Download size={14} /> JSON
              </button>
            </div>
          )}
        </div>
        
        {result ? (
          <ScoreCard result={result} />
        ) : (
          <div className="bg-[#0d1117] border border-[#30363d] border-dashed rounded-lg p-10 flex flex-col items-center justify-center text-[#8b949e] h-[400px]">
            <p>Run analysis to see detailed scoring and communication insights.</p>
          </div>
        )}
      </div>
    </div>
  );
}
