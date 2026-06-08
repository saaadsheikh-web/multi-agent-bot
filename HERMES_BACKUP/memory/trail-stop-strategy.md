---
name: trail-stop-strategy
description: "Trail stop findings from comprehensive backtest — tight trails kill profits, use dynamic fib-based trailing"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

**Backtest finding**: Tight trailing stops are the #1 profitability killer. High WR strategies fail because trail exits are too small relative to SL.

**Evidence from comprehensive backtest**:
- trend_pullback: 63.3% WR but -21.5% (5m), -46.9% (15m) — trail captures ~1.5%, SL is 2.5%
- daily_breakout: 73.9% WR, +1,992% — trail is 2%, SL is 4% (wider ratio)
- wide_scalp: 63.2% WR, +113% — trail is 0.4%, but SL is only 0.6% (better ratio)

**The math**: 
- 1.5% trail with 2.5% SL at 63% WR: EV = 0.63×1.5 - 0.37×2.5 = -0.02% (BREAKEVEN)
- 2% trail with 4% SL at 74% WR: EV = 0.74×2 - 0.26×4 = +0.44% (PROFITABLE)

**User directive**:
- Don't trail too tight — let positions breathe
- Use fib levels, EMA structure, and market context to dynamically set trail distance
- Active trail management beats fixed percentages

**Implementation approach**:
- Use Fibonacci retracement levels for trail activation points
- Wider trail in trending markets (stay in the move)
- Tighter trail only when price approaches key fib resistance
- Trail distance should be at least 50% of SL distance (not 25-50% like trend_pullback)

**Why**: Fixed tight trails destroy edge. Dynamic fib-based trails preserve edge.
**How to apply**: Increase trail distance to ≥50% of SL, use fib levels for activation, wider trails in trends. See also [[comprehensive-backtest-20260603]], [[backtest-statistical-findings]].
