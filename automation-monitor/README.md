# Automation Monitor Suite

Capability: IMPLEMENTED. Python 3.12+.

## Triggers
- GitHub Monitor: cron '0 * * * *' (hourly) + push/release events
- HF Tracker: cron '0 12 * * *' (daily 12:00 UTC)
- Vercel Summary: cron '0 13 * * *' (daily 13:00 UTC) + Vercel webhook dispatch
