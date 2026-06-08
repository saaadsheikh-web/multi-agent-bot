# Loss Analysis & Permanent Fixes — 2026-06-07

## Root Causes Found
- 40% of losers: Trade had profit (+0.6-0.9%) but trail never activated (+1%)
- 33% of losers: Breakeven never triggered (+0.5% threshold too high)
- 27% of losers: Bad entry timing (immediate reversal)
- 5/7 big losers were SHORTS (now blocked unless trend <= -2)
- ALL losers were conf=3 signals

## Fixes Applied
| Fix | Before | After |
|-----|--------|-------|
| Breakeven ladder | +0.5% | +0.3% |
| Trail activate | +3.0% | +1.0% |
| Trail distance | 6% | 4% |
| Min confidence | 3 | 4 |
| Signal consensus | 3/6 | 4/6 |
| Bad hours | 6 hours | 9 hours |
| Volume filter | None | >80% avg |

## Signal Quality Gate
- Hard-blocked: bad hours (3-7, 18-19, 0, 2 UTC)
- Hard-blocked: volume < 80% average
- Hard-blocked: < 4/6 indicator agreement
- Hard-blocked: confidence < 4
- Hard-blocked: shorts unless trend <= -2
