---
name: backtest-statistical-findings
description: "Statistical patterns from comprehensive 44-agent backtest — TF analysis, WR correlation, trade count sweet spot, native vs non-native"
metadata: 
  node_type: memory
  type: project
  originSessionId: 08d28190-52b4-461f-893a-bbbffc7549aa
---

Key statistical findings from the comprehensive 2026-06-03 backtest (44 agents × 4 TFs × 20 symbols):

**Timeframes**:
- 1H is the only profitable TF on average (+81.3% avg return, 41% profitable)
- 5m, 15m, 30m all average -19.8% return
- 30m has lowest avg DD (29%) — best for conservative strategies

**Win Rate**:
- WR > 65% = 74% chance of profitability, +113.3% avg return
- WR < 45% = 7% chance of profitability, -25.0% avg return
- WR is the strongest single predictor of strategy success

**Trade Count**:
- 500-1999 trades/year = sweet spot (+19.2% avg return)
- <100 trades = break-even (-0.8% avg)
- 2000+ = diminishing returns (+14.5% avg)

**Native vs Non-Native**:
- Non-native TFs outperform native by 40 percentage points (+10.8% vs -28.8%)
- Only 25% of native-TF results are profitable vs 29% for non-native
- Hardcoded TFs are likely wrong — always test all TFs

**Confirmation**:
- Improves 76% of strategies, avg +6.9%
- Most effective: 1H→15m, 15m→5m
- Works by filtering bad signals, not improving win rate

**Best profiles**: daily_breakout (+518%), zscore_reversion (+154%), daily_breakout_24h (+153%)
**Worst profiles**: hurst_regime (-84%), momentum (-63%), golden_cross (-62%)

**Why**: To guide strategy development and deployment decisions
**How to apply**: Default new strategies to 1H, target 65%+ WR, aim for 500-2000 trades/yr, always test non-native TFs, use confirmation for high-signal strategies
