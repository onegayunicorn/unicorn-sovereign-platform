export type CircuitFormat = 'openqasm2' | 'openqasm3' | 'qir' | 'quil' | 'cirq-json';

export interface QuantumCircuit {
  circuitId: string;
  name: string;
  version?: string;
  format: CircuitFormat;
  qubitCount?: number;
  depth?: number;
  content: string;
  hash: string;
  signature?: string;
  createdBy?: string;
  createdAt: string;
}
