export type EventType =
  | 'job-submitted'
  | 'policy-evaluated'
  | 'job-approved'
  | 'job-rejected'
  | 'job-queued'
  | 'execution-started'
  | 'execution-completed'
  | 'execution-failed'
  | 'artifact-created'
  | 'attestation-verified'
  | 'result-delivered';

export type EventSource = 'unicorndrop' | 'qps' | 'scheduler' | 'gateway' | 'kms' | 'operator';
export type EventSeverity = 'info' | 'warning' | 'error' | 'critical';

export interface AuditEvent {
  eventId: string;
  correlationId: string;
  jobId: string;
  tenantId?: string;
  timestamp: string;
  eventType: EventType;
  source: EventSource;
  severity: EventSeverity;
  details?: Record<string, unknown>;
  signature?: string;
}
