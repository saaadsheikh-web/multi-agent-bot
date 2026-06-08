# Session handoff — read me first

Last touched: 2026-05-16.

## What's wired

- **OpenRouter**: rotation across multiple keys, free-tier only.
  - `.env` → `OPENROUTER_API_KEYS=key1,key2` (comma-separated, add more anytime).
  - `OPENROUTER_MODEL=openrouter/owl-alpha` (free 1M-context stealth model).
  - `OPENROUTER_FREE_ONLY=1` (refuses paid slugs).
- **`openrouter_client.py`** — thread-safe `KeyRotator` + `chat()`. Round-robin, 60s cooldown on 429/5xx/401/403, free-only guard.
- **`hermes_bridge.py`** — file-based bus between Hermes and the crypto bot.
  - `state.json`, `events.jsonl`, `commands.jsonl`, `ack.jsonl` under `./hermes_bridge/`.
  - Commands: `pause`, `resume`, `flatten`, `flatten_all`, `set_leverage`, `set_risk`, `reload_strategies`, `ping`, `say`.
- **`hermes.py`** — observer/controller. Uses the rotator. CLI:
  - `python3 hermes.py state | tail | ask "…" | auto "…" | exec pause | exec set_leverage --arg value=3 | ping`
- **`bot.py`** — runs `hermes_loop` alongside the other supervised loops. Publishes a snapshot every 5s, drains+acks Hermes commands. Arbiter routes through the rotator.
- **Chart**: `equity_curve_compact.png` (910×455, ~94 KB) saved alongside the original.

## Verify locally

```bash
cd ~/multi_agent_bot
./hermes_smoketest.sh
```

Confirms rotation, makes a real Owl Alpha call, runs a bridge round-trip.

## Open todos / next moves

- Add more OpenRouter free keys to `OPENROUTER_API_KEYS` to widen rate-limit headroom.
- (Optional) Wire Hermes into Telegram so commands can be issued from your phone.
- (Optional) Have Hermes auto-act on regime changes (e.g., `flatten_all` if BTC vol > N%).
