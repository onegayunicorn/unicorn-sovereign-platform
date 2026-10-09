import { describe, it, expect } from 'vitest';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import jobSchema from '../job.schema.json';
import circuitSchema from '../circuit.schema.json';
import artifactSchema from '../artifact.schema.json';
import auditEventSchema from '../audit-event.schema.json';

const ajv = new Ajv({ strict: false, allErrors: true });
addFormats(ajv);

describe('JSON Schema Validation', () => {
  it('job.schema.json is valid JSON Schema 2020-12', () => {
    const validate = ajv.compile(jobSchema);
    expect(validate.errors).toBeNull();
  });

  it('circuit.schema.json is valid JSON Schema 2020-12', () => {
    const validate = ajv.compile(circuitSchema);
    expect(validate.errors).toBeNull();
  });

  it('artifact.schema.json is valid JSON Schema 2020-12', () => {
    const validate = ajv.compile(artifactSchema);
    expect(validate.errors).toBeNull();
  });

  it('audit-event.schema.json is valid JSON Schema 2020-12', () => {
    const validate = ajv.compile(auditEventSchema);
    expect(validate.errors).toBeNull();
  });
});
