# Plan B — if BloFin Transaction API never arrives

If Saad's BloFin Transaction API Key application is denied or stalls indefinitely, here are concrete fallback paths ranked by effort vs payoff.

## Option 1: Bybit (RECOMMENDED Plan B) — ALREADY 80% BUILT

**Status:** `bybit_wrapper.py` is complete. `bot.py` has an `EXCHANGE=bybit` env switch.
**Remaining effort:** ~30 min (write Bybit credentials to .env + retest backtest with Bybit data fetcher).
**Payoff:** full bot working without BloFin.

- Bybit perpetual futures has retail API keys with no broker binding
- Sign up: bybit.com → Account → API Management → Create API Key
- Same instrument symbols mostly (BTC-USDT, ETH-USDT, etc.)
- Python SDK: `pip install pybit` — official Bybit SDK
- Fee: 0.055% taker (slightly better than BloFin's 0.06%)

**What's already done:**
- `bybit_wrapper.py` mirrors BloFin's interface exactly (tickers, candles, place_market, balance, positions, etc.)
- Symbol translation BTC-USDT ↔ BTCUSDT handled
- Bar code translation (1H → 60, 5m → 5, etc.) handled
- bot.py has `EXCHANGE=bybit` env switch that swaps wrapper at runtime
- All strategies + backtest simulator are exchange-agnostic — they read OHLCV and fire signals. They keep working.

**What remains:**
1. You create Bybit account + Read/Trade API key
2. Add to `.env`: `BYBIT_API_KEY=`, `BYBIT_API_SECRET=`, `EXCHANGE=bybit`
3. Withdraw USDT from BloFin → deposit to Bybit (~10-30 min TRC20)
4. Re-fetch 365d cache from Bybit (one-shot 5 min run; their API: 1000 candles per request, paginate)
5. Run live backtest to confirm same edge holds on Bybit's data
6. Bot auto-restarts, fires real trades

**Fund transfer:** withdraw USDT from BloFin → deposit to Bybit. ~10-30 min on TRC20 network.

## Option 2: OKX

**Effort:** ~3-4 hours. **Payoff:** working bot.

- Larger exchange, also has retail API keys without broker binding
- Sign up: okx.com → API Management
- Python SDK: `pip install python-okx`
- Fee: 0.05% taker
- Note: OKX has stricter KYC for high volumes; fine for $2k account

## Option 3: Hyperliquid (DEX, no KYC)

**Effort:** ~6-8 hours. **Payoff:** non-custodial, but different paradigm.

- Decentralized exchange, no centralized API key — uses wallet signatures
- Python SDK: `pip install hyperliquid-python-sdk`
- Hyperliquid is what the original "hyperbot" service is built for — ironic
- Fee: 0.035% taker (cheapest of any option)
- Liquidation/margin model differs from BloFin's
- Funds need to be on Arbitrum or via their bridge

## Option 4: Continue manual trading w/ Telegram signals

**Effort:** zero (already built). **Payoff:** lower since Saad has to click each trade.

- Bot already emits Telegram alerts when signals fire
- Saad clicks trade manually on BloFin web UI
- Loses the autonomous-execution edge, but strategies still profit from being right about direction
- Maybe 30-50% slippage vs auto-execution because of human reaction time

## Option 5: Wait for BloFin Transaction API approval

**Effort:** zero. **Payoff:** unknown (BloFin may never approve).

- Submit the application form (https://forms.gle/mNAXgrSbcpwAPrbr5)
- Approval times reported online: hours to weeks
- If approved, plug in the new key, drop brokerId, bot fires immediately

## My recommendation

If you give BloFin **24-48 hours** to respond after submitting the application and they don't approve, **switch to Bybit (Option 1)**. The retargeting work is mechanical — replace ~150 lines of broker layer in bot.py and re-fetch backtest data. All your strategy work transfers cleanly.

I can start prepping the Bybit retarget proactively (separate `bybit.py` module that mirrors `BloFin`'s interface) so when you say "go", we flip the import and run.

## File map for retargeting

The pieces that touch BloFin specifically (need rewriting per exchange):

- `bot.py` lines ~415-660 — `BloFin` class (instrument, ticker, candle, orderbook, place_market, close_position fetch)
- `bot.py` line ~3082 — instantiation: `bf = BloFin()`
- `backtest.py` lines ~107-170 — data fetching
- `.env` — credential variable names

The strategy code (Agent classes, signal fns, profiles, regime classifier, backtest simulator) is all exchange-agnostic. ~95% of the codebase is portable.
