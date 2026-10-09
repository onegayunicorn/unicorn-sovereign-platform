// Transfer state machine with idempotency + audit trail.
export type TransferState =
  | 'CREATED' | 'ACCEPTING' | 'RECEIVED' | 'SCANNING'
  | 'APPROVED' | 'DELIVERING' | 'DELIVERED'
  | 'REJECTED' | 'QUARANTINED' | 'DEAD_LETTERED';

export type RetryClass = 'transient' | 'auth' | 'policy' | 'permanent';

const TRANSITIONS: Record<TransferState, TransferState[]> = {
  CREATED: ['ACCEPTING', 'REJECTED'],
  ACCEPTING: ['RECEIVED', 'REJECTED', 'DEAD_LETTERED'],
  RECEIVED: ['SCANNING', 'REJECTED'],
  SCANNING: ['APPROVED', 'QUARANTINED', 'REJECTED'],
  APPROVED: ['DELIVERING', 'REJECTED'],
  DELIVERING: ['DELIVERED', 'DEAD_LETTERED', 'QUARANTINED'],
  DELIVERED: [],
  REJECTED: [], QUARANTINED: [], DEAD_LETTERED: [],
};

export function canTransition(from: TransferState, to: TransferState): boolean {
  return TRANSITIONS[from]?.includes(to) ?? false;
}

export interface TransferRecord {
  id: string;
  idempotencyKey: string;
  contentHash: string; // SHA-256
  state: TransferState;
  retryClass?: RetryClass;
  auditTrail: Array<{ state: TransferState; timestamp: number; actor: string }>;
}
