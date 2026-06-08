# CEO brief precompute

`ceo_brief.py` does the deterministic part of the hourly CEO meeting so the LLM
doesn't burn tokens re-deriving things SQL/regex can do in 60ms.

## What it computes

- **Per-agent stats**: n (total closed trades), n_real (excluding pnl=0 phantom
  init rows), wins, losses, WR, PF, ExpR/trade (with maker-fee 0.0008
  adjustment), annualized Sharpe, last5 / last10 / last20 windows.
- **Pre-evaluated gates** from SKILL.md:
  - `undeploy_candidates` — n_real>=5 AND (WR<30% OR last5 PF<0.5 OR cum_pnl<-$10)
  - `scale_up_candidates` — n_real>=10 AND PF>1.5 AND WR>55%, OR last20 WR>60% AND PF>1.7
  - `scale_down_candidates` — lifetime PF<0.8, OR last10 WR<45%
  - `insufficient_data` — n_real<5 (the hard floor — never act)
- **Today's PnL** and **last 7 days bucketed**.
- **Open positions** (agent, symbol, side, entry, opened_at, notional).
- **Liveness** from bot.log — last `scan:`, `signals:`, `regime:` line ages,
  current regime/ADX/ATR, last 5 ERROR rows. Liveness uses the most-recent log
  line as the time reference so it's correct regardless of the bot host's
  timezone (DB writes ISO+00:00, bot.log writes naive local time).
- **Liveness flags** — surfaces "SCANNER DEAD" if `scan:` is >10min stale while
  `regime:` is fresh (the exact failure mode from 2026-05-16 16:56Z).

## Output

Single JSON blob (~8 KB) to stdout. `--human` prints indented JSON.

```
python3 ceo_brief.py > /tmp/ceo_brief.json    # for the LLM run
python3 ceo_brief.py --human                  # for ad-hoc inspection
```

## How the hourly LLM run uses it

1. Run `python3 /Users/saad/multi_agent_bot/ceo_brief.py > /tmp/ceo_brief.json`
   (one bash call, ~60ms).
2. Read `/tmp/ceo_brief.json` (one tool call).
3. Reason over the precomputed gates, write devil's-advocate, queue actions,
   append the CEO_LOG entry, decide on Telegram. That's it.

This replaces the prior pattern of multiple inline SQL queries, log greps, and
stats math in the LLM context, which was the bulk of the per-hour token spend.

## Update / re-test

The script is self-contained. Just edit and rerun. Paths resolve from the
script's own directory, so it works in the sandbox and on the Mac without
config.
