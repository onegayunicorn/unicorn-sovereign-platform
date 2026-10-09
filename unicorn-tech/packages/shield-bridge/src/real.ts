// N01 Shield Hub real API bridge — requires UNICORN_USE_REAL=true + credentials.
export async function fetchShieldTelemetry(endpoint: string, apiKey: string): Promise<unknown> {
  const res = await fetch(`${endpoint}/telemetry`, { headers: { Authorization: `Bearer ${apiKey}` } });
  if (!res.ok) throw new Error(`Shield Hub API error: ${res.status}`);
  return res.json();
}
