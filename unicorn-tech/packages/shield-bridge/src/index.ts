// Env-gated mock/real switch. Defaults to mock — real requires explicit opt-in.
import { mockShieldTelemetry } from './mock';
import { fetchShieldTelemetry } from './real';

export async function getShieldTelemetry(): Promise<unknown> {
  const useReal = process.env.UNICORN_USE_REAL === 'true';
  if (useReal) {
    const endpoint = process.env.SHIELD_HUB_ENDPOINT;
    const apiKey = process.env.SHIELD_HUB_API_KEY;
    if (!endpoint || !apiKey) throw new Error('Real Shield Hub requested but credentials missing');
    return fetchShieldTelemetry(endpoint, apiKey);
  }
  return mockShieldTelemetry();
}
