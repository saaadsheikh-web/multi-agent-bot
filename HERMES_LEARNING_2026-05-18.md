# HERMES LEARNING FILE — 2026-05-18

Purpose: Trading rules and strategy upgrades for Hermes to internalize.
Owner: Saad
Mission: Make money. Kill what doesn't work. Make winners bigger.

---

## CORE PRINCIPLE

Most bots die from **small wins + big losses**.
Flip it: **big wins + small losses**. That's the entire game.

---

## KILL RULES (cut bleeders fast)

- Negative expectancy over 50+ trades → KILL. No revival.
- Win rate < 40% AND R:R < 2:1 → KILL.
- Max drawdown > 2x average win → KILL or shrink size by 75%.
- Strategy correlated to other losers (loses when they lose) → not diversification, it's hidden leverage. KILL.

**Why:** Bad strategies don't "come back." They compound losses while you wait.

---

## TURN LOSSES INTO PROFITS (the 3 that matter)

### 1. Re-entry after stop-out
- If price moves in your original direction within **5 bars** of getting stopped → re-enter at **50% size**.
- **Why:** Most losses are right idea, wrong timing. Tight stops + re-entry beats wide stops.

### 2. Fade failed breakouts
- Breakout fails inside **3 bars** → trade the reversal.
- **Why:** Failed breakouts trap traders. Their forced exits fuel your move.

### 3. Pause after 3 consecutive losses
- Hit 3 losses in a row on a strategy → **pause for the session**.
- Resume next session OR after a volatility reset.
- **Why:** Regime shifted. Continuing = paying tuition you already paid.

---

## MAKE WINNERS BIGGER (where the real money is)

### 1. Pyramid winners
- At **+1R**: add 50% of original size. Move stop to breakeven on original.
- At **+2R**: add 25% more. Trail stop to +1R.
- **Why:** Turns 2R winners into 5R+ winners. Same win rate, 2-3x the P&L.

### 2. ATR trailing stops instead of fixed TPs
- Replace fixed take-profits with ATR-based or swing-structure trailing stops.
- **Why:** Fixed TPs cap upside. Trailing stops let runners run. The 10R trade pays for 10 losers.

### 3. Partial exit at +1R, runner on the rest
- Take **50% off at +1R**. Move stop to breakeven on remainder.
- Let the rest ride with trailing stop.
- **Why:** Worst case = breakeven. Best case = 10R. Asymmetric by design.

---

## LOSS TAGGING (every loser is data)

Tag every losing trade with one of:
- **Wrong direction** → strategy may be broken, watch closely
- **Right direction, wrong timing** → tighten entry filter or add re-entry
- **Stopped then reversed** → stop too tight, widen or use structure-based
- **Regime mismatch** → add regime filter (trend vs chop vs crisis)

**Why:** Untagged losses teach nothing. Tagged losses become the next edge.

---

## NEW STRATEGIES TO BOLT ON (crypto-specific)

1. **Funding-rate arbitrage** — perp vs spot when funding extreme
2. **Liquidation-cascade fades** — mean reversion after large liq events
3. **Volume-weighted breakout filter** — kills 70% of false breakouts
4. **Cross-exchange lead-lag** — Binance leads Coinbase by seconds
5. **Regime classifier (meta-layer)** — routes capital only to strategies that win in current regime

---

## POSITION SIZING RULE

- Recent expectancy positive + volatility favorable → **increase size on next signal**.
- Recent expectancy negative OR volatility hostile → **shrink size**.
- **Why:** Press edge when hot. Protect capital when cold. Don't size flat.

---

## DAILY HERMES CHECKLIST

1. Any strategy hit kill criteria today? → Kill it.
2. Any losses tagged? → Tag them now.
3. Any winner still open? → Is it pyramided? Trailing stop set?
4. Any 3-loss streak? → Pause that strategy.
5. Regime check: trend, chop, or crisis? → Route capital accordingly.

---

## NORTH STAR

> Small wins die slow. Big wins compound fast.
> Cut losers in 1 bar. Ride winners for 100.

End of learning file.
