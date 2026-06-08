# Fix the broker_id error — 2 minutes, then trades will fire

## What's actually wrong

Your current API key (named "hyperbot") is a **Broker API Key**, not a regular retail key.
BloFin has two types:

| Key type            | Needs brokerId? | Use case                       |
|---------------------|-----------------|--------------------------------|
| Transaction API Key | NO              | Normal retail trading          |
| Broker API Key      | YES (specific)  | 3rd-party bots like Hyperbot   |

The diagnostic dump (`broker_diag.json`) shows your key is type 2 = Broker. That's why:
- No brokerId   → 152012 "brokerId is required"
- brokerId=MAB  → 152013 "Unmatched brokerId" (MAB isn't bound to this key)

We don't know the right brokerId because Hyperbot keeps it private.

## The 2-minute fix

1. Open https://blofin.com/account/apiManagement
2. **Create a new API key** — pick the DEFAULT type (Transaction API Key, NOT Broker)
   - Give it any name like `mab-bot`
   - Permissions: **Read + Trade** (no Withdraw)
   - No IP whitelist (or add your home IP)
3. Copy the 3 values it shows you ONCE: `API Key`, `Secret`, `Passphrase`
4. Paste them to me in the chat. I'll update `.env`, the bot will auto-restart, and the next signal will fire a real order.

That's it. You don't need to delete the old hyperbot key — just leave it; we'll switch the bot to the new key.

## Why I can't do this for you

Anthropic safety rule: I cannot create accounts or API credentials on your behalf. You have to be the one clicking the "Create API Key" button. After that, hand me the values and I do the rest.
