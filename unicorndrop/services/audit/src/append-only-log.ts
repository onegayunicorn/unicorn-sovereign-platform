// Append-only immutable audit log — entries are hashed and chained.
import crypto from 'crypto';

export interface AuditEntry {
  seq: number;
  timestamp: number;
  actor: string;
  action: string;
  resource: string;
  prevHash: string | null;
  entryHash: string;
}

export class ImmutableAuditLog {
  private entries: AuditEntry[] = [];
  private lastHash: string | null = null;

  append(actor: string, action: string, resource: string): AuditEntry {
    const seq = this.entries.length;
    const timestamp = Date.now();
    const payload = `${seq}|${timestamp}|${actor}|${action}|${resource}|${this.lastHash}`;
    const entryHash = crypto.createHash('sha256').update(payload).digest('hex');
    const entry: AuditEntry = { seq, timestamp, actor, action, resource, prevHash: this.lastHash, entryHash };
    this.lastHash = entryHash;
    this.entries.push(entry);
    return entry;
  }

  verify(): boolean {
    let prev: string | null = null;
    for (const e of this.entries) {
      if (e.prevHash !== prev) return false;
      const payload = `${e.seq}|${e.timestamp}|${e.actor}|${e.action}|${e.resource}|${e.prevHash}`;
      if (crypto.createHash('sha256').update(payload).digest('hex') !== e.entryHash) return false;
      prev = e.entryHash;
    }
    return true;
  }
}
