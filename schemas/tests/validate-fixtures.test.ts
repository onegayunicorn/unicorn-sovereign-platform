import { describe, it, expect } from 'vitest';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import jobSchema from '../job.schema.json';
import circuitSchema from '../circuit.schema.json';
import artifactSchema from '../artifact.schema.json';
import auditEventSchema from '../audit-event.schema.json';
import bellJob from '../fixtures/job.bell-state.json';
import bellCircuit from '../fixtures/circuit.bell-state.json';
import resultArtifact from '../fixtures/artifact.result.json';
import lifecycleEvents from '../fixtures/audit-event.lifecycle.json';

const ajv = new Ajv({ strict: false, allErrors: true });
addFormats(ajv);

describe('Fixture Validation — Bell State MVP', () => {
  it('✅ Bell-state job passes validation', () => {
    const validate = ajv.compile(jobSchema);
    const valid = validate(bellJob);
    if (!valid) console.error('Job errors:', validate.errors);
    expect(valid).toBe(true);
  });

  it('✅ Bell-state circuit passes validation', () => {
    const validate = ajv.compile(circuitSchema);
    const valid = validate(bellCircuit);
    if (!valid) console.error('Circuit errors:', validate.errors);
    expect(valid).toBe(true);
  });

  it('✅ Result artifact passes validation', () => {
    const validate = ajv.compile(artifactSchema);
    const valid = validate(resultArtifact);
    if (!valid) console.error('Artifact errors:', validate.errors);
    expect(valid).toBe(true);
  });

  it('✅ All 7 lifecycle audit events pass validation', () => {
    const validate = ajv.compile(auditEventSchema);
    for (const event of lifecycleEvents) {
      const valid = validate(event);
      if (!valid) console.error('Audit event errors:', validate.errors, event.eventType);
      expect(valid).toBe(true);
    }
  });

  it('✅ All audit events share the same correlationId + jobId', () => {
    const correlationIds = new Set(lifecycleEvents.map(e => e.correlationId));
    const jobIds = new Set(lifecycleEvents.map(e => e.jobId));
    expect(correlationIds.size).toBe(1);
    expect(jobIds.size).toBe(1);
    expect([...correlationIds][0]).toBe('sovereign-bell-0001');
  });
});
