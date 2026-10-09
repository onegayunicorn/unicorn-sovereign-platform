import React, { useState, useCallback } from 'react';
// Circuit workbench — builds circuit IR and dispatches to Web Worker simulation.
const Workbench: React.FC = () => {
  const [numQubits, setNumQubits] = useState(2);
  const [result, setResult] = useState<Record<string, number> | null>(null);
  const runSimulation = useCallback(() => {
    const worker = new Worker(new URL('../workers/quantumWorker.ts', import.meta.url), { type: 'module' });
    worker.postMessage({ type: 'bell_state', numQubits, shots: 1024 });
    worker.onmessage = (e) => setResult(e.data.counts);
  }, [numQubits]);
  return (
    <div className="workbench">
      <h2>Circuit Workbench</h2>
      <label>Qubits: <input type="number" value={numQubits} min={1} max={32}
        onChange={e => setNumQubits(Number(e.target.value))} /></label>
      <button onClick={runSimulation}>Run Bell State</button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
};
export default Workbench;
