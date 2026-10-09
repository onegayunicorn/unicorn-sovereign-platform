// N03 Emu-Verse mock — runtime metrics.
export interface RuntimeMetrics {
  cpuPct: number;
  memoryPct: number;
  activeEmulations: number;
  fps: number;
}

export function mockRuntimeMetrics(): RuntimeMetrics {
  return { cpuPct: 42.5, memoryPct: 67.2, activeEmulations: 3, fps: 60.0 };
}
