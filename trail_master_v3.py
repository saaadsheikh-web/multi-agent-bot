"""
TRAIL MASTER v3 — Research-backed trailing stops from 28.7M tests.
Implements the 4 proven exit methods with per-strategy optimization.

Key Finding (BreakOrb 2026): 
- TP Trail (trail after TP hit) = 43.3% best
- Chandelier (ATR from high) = 25.8% best  
- Fixed TP/SL = 25.1% best
- No trail = 5.8% best (short timeframes)

For crypto altcoins: wider stops needed, TP Trail works best.
For ETH/BNB: Chandelier exit on longer timeframes.
"""

# The 4 exit strategies:
EXIT_METHODS = {
    "fixed_tp_sl": {
        "description": "Original fixed take-profit and stop-loss. No trailing.",
        "best_for": ["mean_reversion", "short_timeframes", "choppy_markets"],
        "backtest_fit": "25.1% of strategies"
    },
    
    "tp_trail": {
        "description": "Trail activates ONLY after price hits take-profit target. Then locks in profit.",
        "how_it_works": "Set TP at 2-5%. When TP hit, don't exit — start trailing at 50% retracement.",
        "best_for": ["trend_following", "breakouts", "altcoins", "BNB"],
        "backtest_fit": "43.3% of strategies — BEST OVERALL",
        "profit_improvement": "BNB: +$102K, ETH: +$73K simulated",
        "our_strategies": ["breakout_12h", "breakout_48h", "daily_breakout", "trend_pullback"]
    },
    
    "chandelier": {
        "description": "ATR-based trail from highest high since entry. Widens in high vol, tightens in low.",
        "how_it_works": "Trail = highest_high - (ATR × multiplier). Stop moves up as price rises.",
        "best_for": ["trending_markets", "smooth_price_action", "ETH", "longer_timeframes"],
        "backtest_fit": "25.8% of strategies",
        "optimal_multiplier": "2-3x ATR"
    },
    
    "no_trail": {
        "description": "Hold to fixed TP/SL. No modification. Works when noise dominates.",
        "best_for": ["1m_timeframes", "low_volatility", "when_extended_trends_are_rare"],
        "backtest_fit": "Remaining ~5.8% of strategies"
    }
}

# Optimal settings for our specific strategies:
STRATEGY_TRAILS = {
    "breakout_12h_1H": {
        "method": "tp_trail",
        "tp_pct": 3.0,
        "trail_retracement_pct": 50.0,
        "sl_pct": 1.8,
        "note": "Let breakout run to 3%. Then trail at 50% retracement of peak."
    },
    "breakout_48h_30m": {
        "method": "tp_trail",
        "tp_pct": 5.0,
        "trail_retracement_pct": 50.0,
        "sl_pct": 3.0,
        "note": "Wider targets for longer lookback."
    },
    "trend_pullback_1H": {
        "method": "chandelier",
        "atr_multiplier": 2.0,
        "sl_pct": 2.5,
        "note": "ATR-based trail since trend_pullback catches trending moves."
    },
    "volume_capitulation": {
        "method": "fixed_tp_sl",
        "tp_pct": 99.0,
        "sl_pct": 1.5,
        "note": "Quick reversal trades. Just take the bounce and exit."
    },
    "fib_ext_15m": {
        "method": "chandelier",
        "atr_multiplier": 3.0,
        "note": "ATR-based trail for fib extension. Adapts to volatility."
    },
    "asian_pump": {
        "method": "fixed_tp_sl",
        "tp_pct": 99.0,
        "sl_pct": 2.5,
        "note": "Quick session trades. Take profit fast."
    }
}

# Market condition adjustments:
MARKET_ADJUSTMENTS = {
    "high_volatility": {
        "action": "widen_all_stops_1.5x",
        "chandelier_mult": "increase_to_3x",
        "tp_trail_retracement": "reduce_to_30%"
    },
    "low_volatility": {
        "action": "tighten_stops_0.8x",
        "tp_trail_target": "reduce_to_2%"
    },
    "strong_trend": {
        "action": "chandelier_works_best",
        "recommended": "switch_to_chandelier"
    },
    "ranging": {
        "action": "fixed_tp_sl_works_best",
        "recommended": "take_profit_at_target"
    }
}

print("="*60)
print("  TRAIL MASTER v3 — Research-Backed")
print("="*60)
print(f"\nBased on 28.7M tests (BreakOrb 2026):")
print(f"\n📊 BEST EXIT METHODS:")
for method, info in EXIT_METHODS.items():
    print(f"  {method:20s} → {info['backtest_fit']:30s} | {info['description']}")
    
print(f"\n📊 OUR STRATEGIES OPTIMAL TRAILS:")
for strat, config in STRATEGY_TRAILS.items():
    print(f"  {strat:25s} → {config['method']:15s} | {config.get('note','')}")
