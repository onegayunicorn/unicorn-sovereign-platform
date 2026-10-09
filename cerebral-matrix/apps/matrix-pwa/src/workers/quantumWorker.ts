// Web Worker for circuit simulation — keeps UI thread free.
// Local WASM circuit simulator interface (placeholder — loads WASM module when available).
self.onmessage = (e: MessageEvent) => {
  const { type, numQubits, shots } = e.data;
  if (type === 'bell_state') {
    // Simulated Bell state — clearly labeled Simulated
    const counts: Record<string, number> = {};
    for (let i = 0; i < shots; i++) {
      const outcome = Math.random() < 0.5 ? '0'.repeat(numQubits) : '1'.repeat(numQubits);
      counts[outcome] = (counts[outcome] || 0) + 1;
    }
    (self as any).postMessage({ counts, classification: 'Simulated' });
  }
};
export {};
