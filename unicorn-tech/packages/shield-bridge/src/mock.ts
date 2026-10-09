// N01 Shield Hub mock bridge — deterministic responses for CI/testing.
export interface ShieldTelemetry {
  topology: Record<string, string>;
  uptimeSeconds: number;
  safetyGateOpen: boolean;
}

export function mockShieldTelemetry(): ShieldTelemetry {
  return {
    topology: { 'node-01': 'online', 'node-02': 'online', 'node-03': 'maintenance' },
    uptimeSeconds: 86400 * 7,
    safetyGateOpen: true,
  };
}
