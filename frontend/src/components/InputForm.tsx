import { useState, FormEvent } from 'react';
import { PRRequest } from '../types';
import { Play, CheckCircle, DatabaseZap, BugOff, GitMerge, FileCheck } from 'lucide-react';

interface Props {
  onSubmit: (data: PRRequest) => void;
  isLoading: boolean;
}

export default function InputForm({ onSubmit, isLoading }: Props) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [commits, setCommits] = useState('');
  const [diff, setDiff] = useState('');
  const [proposedSquashMessage, setProposedSquashMessage] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit({
      title,
      description,
      commits: commits.split('\n').filter(c => c.trim()),
      diff,
      proposedSquashMessage: proposedSquashMessage.trim() || undefined
    });
  };

  const loadGoodSample = () => {
    setTitle("Implement JWT authentication flow and Redis session caching");
    setDescription("This PR implements the new authentication flow using secure JWT tokens. It also connects our session storage to Redis to improve cache latency and reduce database lookups.");
    setCommits("feat: add jwt token validation\nfeat: implement redis caching layer");
    setDiff("+++ b/src/auth/jwt_manager.py\n+def validate_session():\n+    redis_client.get('session')\n+++ b/src/auth/redis_cache.py\n+def connect():\n+    pass\n");
    setProposedSquashMessage("");
  };

  const loadRiskyMigration = () => {
    setTitle("Update user table");
    setDescription("minor fixes and schema tweaks.");
    setCommits("update things\nupdate things");
    setDiff("+++ b/src/db/migration_005.sql\n+ALTER TABLE users DROP COLUMN email;\n+++ b/src/db/cache_layer.py\n+def flush(): pass");
    setProposedSquashMessage("");
  };

  const loadBadSample = () => {
    setTitle("Auth updates");
    setDescription("Improved authentication flow and optimized performance.");
    setCommits("fix logic\nimprove code\nrefined internal structure");
    setDiff("+++ b/src/auth/jwt_manager.py\n+def validate_session():\n+    redis_client.get('session')\n+++ b/src/auth/redis_cache.py\n+def connect():\n+    pass\n");
    setProposedSquashMessage("");
  };

  const loadNoisySquash = () => {
    setTitle("Auth updates");
    setDescription("Improved authentication flow and optimized performance.");
    setCommits("fix logic\nimprove code\nrefined internal structure\nupdated auth flow\nfix logic\nminor changes\nimprove code\ntweaks\nupdate things\nclean up\nfix logic\noptimizations\nvarious changes\nfix logic\nFix Redis session invalidation race during JWT refresh");
    setDiff("+++ b/src/auth/session.py\n+def invalidate_session(): pass\n+++ b/src/cache/redis_store.py\n+class RedisStore: pass\n");
    setProposedSquashMessage("");
  };

  const loadCleanSquash = () => {
    setTitle("Implement JWT session validation with Redis caching");
    setDescription("This PR adds secure JWT session validation to prevent unauthorized access. Redis caching reduces database lookups for session tokens.");
    setCommits("feat: add JWT session validation to prevent expired token reuse\nfeat: integrate Redis caching for session lookups");
    setDiff("+++ b/src/auth/jwt_manager.py\n+def validate_session(): pass\n+++ b/src/cache/redis_store.py\n+class RedisStore: pass\n");
    setProposedSquashMessage("Implement JWT session validation with Redis caching to prevent unauthorized access and reduce DB lookups.");
  };

  return (
    <form onSubmit={handleSubmit} className="bg-[#0d1117] border border-[#30363d] rounded-lg p-6 flex flex-col gap-4">
      <div className="flex flex-col mb-2 gap-2">
        <h2 className="text-lg font-semibold text-white">Analysis Input</h2>
        <div className="flex flex-wrap gap-3">
          <button type="button" onClick={loadGoodSample} className="text-xs text-[#3fb950] hover:underline flex items-center gap-1">
            <CheckCircle size={14} /> Good PR
          </button>
          <button type="button" onClick={loadBadSample} className="text-xs text-[#58a6ff] hover:underline flex items-center gap-1">
            <BugOff size={14} /> Bad Filler PR
          </button>
          <button type="button" onClick={loadRiskyMigration} className="text-xs text-[#f85149] hover:underline flex items-center gap-1">
            <DatabaseZap size={14} /> Risky Migration PR
          </button>
          <div className="w-full h-px bg-[#30363d] my-1"></div>
          <button type="button" onClick={loadNoisySquash} className="text-xs text-[#a371f7] hover:underline flex items-center gap-1">
            <GitMerge size={14} /> Noisy Squash Merge
          </button>
          <button type="button" onClick={loadCleanSquash} className="text-xs text-[#3fb950] hover:underline flex items-center gap-1">
            <FileCheck size={14} /> Clean Squash Merge
          </button>
        </div>
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-[#c9d1d9]">PR Title</label>
        <input 
          type="text" 
          value={title} 
          onChange={e => setTitle(e.target.value)} 
          className="bg-[#010409] border border-[#30363d] rounded-md p-2 text-sm text-white focus:border-[#58a6ff] focus:outline-none"
          required
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-[#c9d1d9]">PR Description</label>
        <textarea 
          value={description} 
          onChange={e => setDescription(e.target.value)} 
          className="bg-[#010409] border border-[#30363d] rounded-md p-2 text-sm text-white focus:border-[#58a6ff] focus:outline-none min-h-[100px]"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-[#c9d1d9]">Commit Messages (one per line)</label>
        <textarea 
          value={commits} 
          onChange={e => setCommits(e.target.value)} 
          className="bg-[#010409] border border-[#30363d] rounded-md p-2 text-sm text-white focus:border-[#58a6ff] focus:outline-none min-h-[80px]"
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-[#c9d1d9]">Raw Git Diff</label>
        <textarea 
          value={diff} 
          onChange={e => setDiff(e.target.value)} 
          className="bg-[#010409] border border-[#30363d] rounded-md p-2 text-sm text-[#8b949e] font-mono focus:border-[#58a6ff] focus:outline-none min-h-[150px]"
          required
        />
      </div>

      <div className="flex flex-col gap-1">
        <label className="text-sm font-medium text-[#c9d1d9]">Proposed Squash Commit Message (Optional)</label>
        <textarea 
          value={proposedSquashMessage} 
          onChange={e => setProposedSquashMessage(e.target.value)} 
          placeholder="Leave blank to simulate default squash message from PR title + commits"
          className="bg-[#010409] border border-[#30363d] rounded-md p-2 text-sm text-[#8b949e] font-mono focus:border-[#58a6ff] focus:outline-none min-h-[60px]"
        />
      </div>

      <button 
        type="submit" 
        disabled={isLoading}
        className="mt-4 bg-[#238636] hover:bg-[#2ea043] text-white font-medium py-2 px-4 rounded-md flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
      >
        <Play size={18} /> {isLoading ? 'Analyzing...' : 'Analyze PR'}
      </button>
    </form>
  );
}
