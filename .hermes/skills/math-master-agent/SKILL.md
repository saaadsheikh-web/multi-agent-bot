---
name: math-master-agent
description: Build and deploy the MathMaster agent — a 4-layer math fusion agent using entropy, Bayesian probability, Monte Carlo simulation, and maximum entropy distributions.
---

# MathMaster Agent

Build when Saad says "teach complex maths", "learn maths", or wants advanced math in the trading bot.

## The 4 layers

1. **Shannon Entropy** — `H = -sum(p * log2(p))`. Low entropy (< 3.5 bits) = predictable market = edge exists.

2. **Bayesian Probability Fusion** — `P(win | signals) = odds * LR_rsi * LR_vol * LR_trend * LR_volatility`. Updates prior (0.55) with evidence from RSI, volume, EMA position, and ATR.

3. **Monte Carlo** — Generates 200 random walks from log-normal distribution. Counts fraction ending positive. Need 55%+ paths going your way.

4. **Maximum Entropy** — Under max entropy (principle of indifference), the least-biased distribution given mean and variance is N(mu, sigma^2). Uses normal CDF to find direction probability.

## Voting system

Each layer casts 1 vote. Need 3/4 votes to fire a signal.

## Location

Insert in bot.py right after `utbot_signal` function (around line 3446), before `_realized_vol_annualized` function.

## Deployment

```bash
cd /Users/saad/multi_agent_bot
git add -A && git commit -m "description" && git push origin main
# Kill and restart bot
```

## Troubleshooting

- If bot won't start: check for `from scipy.stats import norm` — scipy must be installed
- If scipy not available: replace with manual normal CDF approximation (error function)
- The agent uses `pd.Series` inside the analyze method — ensure pandas is imported at module level
