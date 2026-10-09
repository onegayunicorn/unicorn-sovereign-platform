// Shared Zod types for transfer records.
import { z } from 'zod';

export const TransferSchema = z.object({
  id: z.string().uuid(),
  idempotencyKey: z.string().min(1),
  contentHash: z.string().regex(/^[a-f0-9]{64}$/, 'Must be SHA-256 hex'),
  state: z.enum(['CREATED','ACCEPTING','RECEIVED','SCANNING','APPROVED','DELIVERING','DELIVERED','REJECTED','QUARANTINED','DEAD_LETTERED']),
  sizeBytes: z.number().int().nonnegative(),
  tenantId: z.string(),
});
export type Transfer = z.infer<typeof TransferSchema>;
