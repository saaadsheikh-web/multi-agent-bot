# 🚨 AUDITOR ALERT — 2026-05-26T14:07Z

## Headline

**COMPANY_LOG says connors_rsi2/bb_bounce/daily_breakout_4h are "KILLED (perm in source)" — they are NOT. Bot has not been restarted. All three agents remain active as of 14:02 UTC.**

## Evidence

- **COMPANY_LOG** (generated 12:37 UTC by Claude/Cowork session): marks connors_rsi2 as `🔴 KILLED`, states "connors_rsi2 / bb_bounce / daily_breakout_4h KILLED (perm in source)"
- **bot.log at 13:33 UTC** (55 minutes AFTER COMPANY_LOG): `agents enabled: ['daily_breakout_2h', 'macd_cross', 'bb_bounce', 'zscore_reversion', 'stoch_rsi', 'connors_rsi2', 'hurst_regime', 'funding_extremes', 'fibonacci', 'fib_confluence']`
- **bot.log at 14:02 UTC**: `BAD_HOUR_SKIP connors_rsi2 XAG-USDT: 13:00 UTC in killer-hours window` — agent is alive and scanning, only blocked by time filter

## What this means right now

connors_rsi2 **will resume trading** when the killer-hours window (13:00 UTC) lifts — probably within the next 60–90 minutes. If you believe it's dead, it isn't.

## What Saad needs to do

1. **Verify:** Check if the kill was actually committed to bot.py source and restart the bot. `grep -n "connors_rsi2" ~/multi_agent_bot/bot.py | grep -i "disabled\|skip\|kill\|comment"`
2. **If kill is in source but bot hasn't restarted:** Restart bot to activate the kill.
3. **If kill was NOT committed to source:** The COMPANY_LOG is aspirationally wrong — CEO queued a size-down recommendation, not an actual kill.

## Secondary issues (from full audit — see AUDITOR_LOG.md)

- Kill-switch WR mechanism: no `KILL-SWITCH: dropping` log line found anywhere. hurst_regime has WR=25% by DB full count but bot scan shows 56% (non-zero trades only). Kill-switch is not firing as designed.
- hurst_regime undeploy: pending manual curl for 3rd+ consecutive audit window.
- connors_rsi2 WR has degraded -20pp (last10: 40% vs prior10: 60%). CEO has size-down queued.

