import Dashboard from './pages/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-[#0d1117] text-[#c9d1d9] font-sans">
      <header className="border-b border-[#30363d] bg-[#161b22] px-6 py-4">
        <h1 className="text-xl font-semibold text-white tracking-tight">
          <span className="text-[#58a6ff]">PR</span>ettySus
        </h1>
        <p className="text-sm text-[#8b949e]">Deterministic PR Communication Quality Analyzer</p>
      </header>
      <main className="p-6 max-w-7xl mx-auto">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
