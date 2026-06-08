# TradingView Webhook Setup

## Webhook URL

```
https://brigida-tristichic-janet.ngrok-free.dev/tv
```

> Note: this URL is stable as long as the ngrok LaunchAgent (`com.saad.ngrok.webhook`) is running.
> If your Mac reboots and ngrok reassigns a URL, run:
> `curl -s http://localhost:4040/api/tunnels | python3 -c "import sys,json; [print(t['public_url']) for t in json.load(sys.stdin)['tunnels']]"`

---

## Authentication Header

Add this header to every TradingView alert:

| Header name | Value |
|-------------|-------|
| `X-Secret`  | `178f9024586197ca101fac18fdb8796579165984f3e5058b` |

In TradingView → Alert → Notifications → Webhook URL, paste the URL above.
Under **Header**, add `X-Secret` with the value above.

---

## JSON Body Template

Paste this into the **Message** box of your TradingView alert:

```json
{
  "secret":     "178f9024586197ca101fac18fdb8796579165984f3e5058b",
  "symbol":     "{{ticker}}-USDT",
  "side":       "long",
  "confidence": 8,
  "strategy":   "my_strategy_name",
  "price":      {{close}}
}
```

- Change `"side"` to `"long"` or `"short"` per alert condition.
- Change `"confidence"` (1–10). Minimum to trade is **6**; AI arbiter kicks in at **8**.
- Change `"strategy"` to match the name in `TV_STRATEGY_PROFILES` in `bot.py` for a custom TP/SL profile, or leave any name to use the default `momentum` profile.
- `{{ticker}}` and `{{close}}` are TradingView template variables — leave them as-is.

---

## Profile Customisation

Edit `TV_STRATEGY_PROFILES` in `bot.py` to map your strategy names to risk profiles:

```python
TV_STRATEGY_PROFILES: Dict[str, str] = {
    "my_scalp_strategy": "scalp",    # 0.6% TP / 0.4% SL / 30-min max hold
    "my_swing_strategy": "swing",    # 4.5% TP / 2.0% SL / 24-hr max hold
    # default for anything not listed: "momentum" (3% TP / 1.2% SL)
}
```

Available profiles: `scalp`, `momentum`, `swing`, `meanrev`, `whale`, `news`

---

## Test Locally

```bash
curl -X POST http://localhost:8787/tv \
  -H "Content-Type: application/json" \
  -H "X-Secret: 178f9024586197ca101fac18fdb8796579165984f3e5058b" \
  -d '{"symbol":"BTC-USDT","side":"long","confidence":8,"strategy":"test","price":94000}'
```

## Test via ngrok (end-to-end)

```bash
curl -X POST https://brigida-tristichic-janet.ngrok-free.dev/tv \
  -H "Content-Type: application/json" \
  -H "X-Secret: 178f9024586197ca101fac18fdb8796579165984f3e5058b" \
  -d '{"symbol":"BTC-USDT","side":"long","confidence":3,"strategy":"test","price":94000}'
```

A confidence of 3 will be vetoed by the risk manager (below MIN_CONFIDENCE=6) so no real trade fires.
