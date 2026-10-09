export interface QuantumJob {
  jobId: string;
  correlationId: string;
  tenantId: string;
  workspaceId?: string;
  circuitId: string;
  status:
    | 'submitted'
    | 'validated'
    | 'approved'
    | 'queued'
    | 'executing'
    | 'completed'
    | 'failed'
    | 'cancelled'
    | 'rejected';
  backend: {
    provider: string;
    target: string;
    region?: string;
  };
  policy: {
    jurisdiction: string;
    dataClassification: 'public' | 'internal' | 'confidential' | 'regulated';
    approved: boolean;
    decisionReason?: string;
  };
  execution?: {
    shots: number;
    priority?: number;
  };
  submittedAt: string;
  startedAt?: string;
  completedAt?: string;
  createdBy?: string;
}
