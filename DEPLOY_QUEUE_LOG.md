# DEPLOY QUEUE LOG

Audit log of deploy-approver scheduled task runs.

---

## 2026-04-30T03:39:57Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 1
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~9.5h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.

## 2026-04-30T05:01:56Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 1
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~10.8h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.

## 2026-04-30T07:01:59Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 3
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~12.8h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.
  - `daily_breakout` — queued 2026-04-30 (~3.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~3.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.

## 2026-04-30T09:18:52Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 3
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~15.1h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.
  - `daily_breakout` — queued 2026-04-30 (~5.4h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~5.4h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.

## 2026-04-30T11:02:00Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 3
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~16.8h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.
  - `daily_breakout` — queued 2026-04-30 (~7.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~7.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.

## 2026-04-30T13:02:01Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 3
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~18.8h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.
  - `daily_breakout` — queued 2026-04-30 (~9.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~9.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.

## 2026-04-30T15:01:59Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 3
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~20.8h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.
  - `daily_breakout` — queued 2026-04-30 (~11.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~11.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.

## 2026-04-30T17:02:05Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 3
- **Reminders sent:** 0
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~22.8h ago via source report timestamp 2026-04-29T18:12:14Z); under 24h threshold → silent.
  - `daily_breakout` — queued 2026-04-30 (~13.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~13.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.

## 2026-04-30T19:02:01Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 5
- **Reminders attempted:** 1
- **Reminders sent:** 0 (network egress blocked — see below)
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~24.83h ago via source report timestamp 2026-04-29T18:12:14Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: trend_pullback has been pending approval for 24h. Stats: ExpR +0.204R, DD 22.0%, n=2457. To deploy: tell Cowork 'deploy trend_pullback' / To reject: tell Cowork 'reject trend_pullback'".
    - **Send result:** FAILED. `api.telegram.org` is not on the cowork sandbox network allowlist (HTTP 403 from proxy via curl; web_fetch returned `cowork-egress-blocked`). Allowlist would need `api.telegram.org` added in Settings → Capabilities for this scheduled task to deliver Telegram nudges.
    - **Note:** trend_pullback also flagged in queue with re-validation note — ExpR slipped to +0.153R (n=649) on 2026-04-30 05:02 UTC fresh universe. Saad should review whether to deploy on the original PASS stats or re-queue.
  - `daily_breakout` — queued 2026-04-30 (~15.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~15.1h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_4h` — queued 2026-04-30 (~5.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.
  - `daily_breakout_7d` — queued 2026-04-30 (~5.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.

## 2026-04-30T21:59:39Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 5
- **Reminders attempted:** 1
- **Reminders sent:** 0 (network egress still blocked — see below)
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~27.79h ago via source report timestamp 2026-04-29T18:12:14Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: trend_pullback has been pending approval for 28h. Stats: ExpR +0.204R, DD 22.0%, n=2457. To deploy: tell Cowork 'deploy trend_pullback' / To reject: tell Cowork 'reject trend_pullback'".
    - **Send result:** FAILED again. `api.telegram.org` is still not on the cowork sandbox network allowlist (curl exit 56; web_fetch returned `cowork-egress-blocked`, current allowlist excludes telegram). Saad needs to add `api.telegram.org` in Settings → Capabilities (or ask workspace admin) for any deploy reminders to deliver.
    - **Note:** trend_pullback re-validation note still standing — ExpR slipped to +0.153R (n=649) on 2026-04-30 05:02 UTC fresh universe. Saad should review whether to deploy on the original PASS stats or re-queue. This is the 2nd consecutive run reminder has fired and not delivered.
  - `daily_breakout` — queued 2026-04-30 (~18.05h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~18.05h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_4h` — queued 2026-04-30 (~8.31h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.
  - `daily_breakout_7d` — queued 2026-04-30 (~8.31h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.

## 2026-05-01T01:02:00Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 5
- **Reminders attempted:** 1
- **Reminders sent:** 0 (network egress still blocked — see below)
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~30.83h ago via source report timestamp 2026-04-29T18:12:14Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: trend_pullback has been pending approval for 31h.\nStats: ExpR +0.204R, DD 22.0%, n=2457.\nTo deploy: tell Cowork 'deploy trend_pullback'\nTo reject: tell Cowork 'reject trend_pullback'".
    - **Send result:** FAILED again. `api.telegram.org` still not on the cowork sandbox network allowlist (curl exit 56, HTTP 403 from proxy after CONNECT). 3rd consecutive run the reminder has fired without delivery. Saad needs to add `api.telegram.org` in Settings → Capabilities (or ask workspace admin) for any deploy reminders to actually deliver.
    - **Note:** trend_pullback re-validation note still standing — ExpR slipped to +0.153R (n=649) on 2026-04-30 05:02 UTC fresh universe. Strategy now also has 4 stronger same-cohort peers in queue (daily_breakout_4h ExpR +0.501R / Sharpe 10.36 is the stand-out). Saad should review whether to deploy on the original PASS stats, re-queue, or reject in favor of the stronger candidates.
  - `daily_breakout` — queued 2026-04-30 (~21.09h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent.
  - `daily_breakout_24h` — queued 2026-04-30 (~21.09h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent. (Will cross 24h before next ~03:00Z run.)
  - `daily_breakout_4h` — queued 2026-04-30 (~11.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.
  - `daily_breakout_7d` — queued 2026-04-30 (~11.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.

## 2026-05-01T03:02:01Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 5
- **Reminders attempted:** 1
- **Reminders sent:** 0 (network egress still blocked — see below)
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~32.83h ago via source report timestamp 2026-04-29T18:12:14Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: trend_pullback has been pending approval for 33h.\nStats: ExpR +0.204R, DD 22.0%, n=2457.\nTo deploy: tell Cowork 'deploy trend_pullback'\nTo reject: tell Cowork 'reject trend_pullback'".
    - **Send result:** FAILED again. `api.telegram.org` still not on the cowork sandbox network allowlist (curl exit 56, HTTP 403 from proxy after CONNECT). 4th consecutive run the reminder has fired without delivery. Saad needs to add `api.telegram.org` in Settings → Capabilities (or ask workspace admin) for any deploy reminders to actually deliver.
    - **Note:** trend_pullback re-validation note still standing — ExpR slipped to +0.153R (n=649) on 2026-04-30 05:02 UTC fresh universe. Strategy now also has 4 stronger same-cohort peers in queue (daily_breakout_4h ExpR +0.501R / Sharpe 10.36 is the stand-out). Saad should review whether to deploy on the original PASS stats, re-queue, or reject in favor of the stronger candidates.
  - `daily_breakout` — queued 2026-04-30 (~23.09h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent. (Will cross 24h within the next hour; expect first reminder on next ~05:00Z run.)
  - `daily_breakout_24h` — queued 2026-04-30 (~23.09h ago via source report timestamp 2026-04-30T03:56:39Z); under 24h threshold → silent. (Will cross 24h within the next hour; expect first reminder on next ~05:00Z run.)
  - `daily_breakout_4h` — queued 2026-04-30 (~13.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.
  - `daily_breakout_7d` — queued 2026-04-30 (~13.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent.

## 2026-05-01T05:02:03Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 5
- **Reminders attempted:** 3
- **Reminders sent:** 0 (network egress still blocked — see below)
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~34.83h ago via source report timestamp 2026-04-29T18:12:14Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: trend_pullback has been pending approval for 35h.\nStats: ExpR +0.204R, DD 22.0%, n=2457.\nTo deploy: tell Cowork 'deploy trend_pullback'\nTo reject: tell Cowork 'reject trend_pullback'".
    - **Send result:** FAILED. `api.telegram.org` still not on the cowork sandbox network allowlist (curl exit 56, HTTP 403 from proxy after CONNECT). 5th consecutive run the trend_pullback reminder has fired without delivery.
    - **Note:** Re-validation note still standing — ExpR slipped to +0.153R (n=649) on 2026-04-30 05:02 UTC fresh universe. 4 stronger same-cohort peers now in queue (daily_breakout_4h ExpR +0.501R / Sharpe 10.36 stand-out). Saad should review whether to deploy on original PASS stats, re-queue, or reject in favor of stronger candidates.
  - `daily_breakout` — queued 2026-04-30 (~25.09h ago via source report timestamp 2026-04-30T03:56:39Z); **OVER 24h threshold** (just crossed) → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: daily_breakout has been pending approval for 25h.\nStats: ExpR +0.417R, DD 4.0%, n=290.\nTo deploy: tell Cowork 'deploy daily_breakout'\nTo reject: tell Cowork 'reject daily_breakout'".
    - **Send result:** FAILED. Same `api.telegram.org` allowlist block (curl exit 56, HTTP 403 from proxy after CONNECT). 1st reminder for this strategy.
  - `daily_breakout_24h` — queued 2026-04-30 (~25.09h ago via source report timestamp 2026-04-30T03:56:39Z); **OVER 24h threshold** (just crossed) → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: daily_breakout_24h has been pending approval for 25h.\nStats: ExpR +0.384R, DD 5.2%, n=1009.\nTo deploy: tell Cowork 'deploy daily_breakout_24h'\nTo reject: tell Cowork 'reject daily_breakout_24h'".
    - **Send result:** FAILED. Same `api.telegram.org` allowlist block (curl exit 56, HTTP 403 from proxy after CONNECT). 1st reminder for this strategy.
  - `daily_breakout_4h` — queued 2026-04-30 (~15.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent. (Will cross 24h before next ~15:00Z run.)
  - `daily_breakout_7d` — queued 2026-04-30 (~15.35h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent. (Will cross 24h before next ~15:00Z run.)
- **Action needed from Saad:** add `api.telegram.org` to the cowork sandbox network allowlist (Settings → Capabilities, or via workspace admin) — every reminder this task has produced has been blocked at the proxy. Until that's done, no deploy reminders will actually reach Telegram. Alternative: review the 5 pending strategies directly here and deploy/reject by replying in-session.

## 2026-05-01T09:06:05Z
- **Run:** mab-deploy-approver
- **Queue entries scanned:** 9
- **Reminders attempted:** 3
- **Reminders sent:** 0 (network egress still blocked — see below)
- **Details:**
  - `trend_pullback` — queued 2026-04-30 (~38.90h ago via source report timestamp 2026-04-29T18:12:14Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: trend_pullback has been pending approval for 39h.\nStats: ExpR +0.204R, DD 22.0%, n=2457.\nTo deploy: tell Cowork 'deploy trend_pullback'\nTo reject: tell Cowork 'reject trend_pullback'".
    - **Send result:** FAILED. `api.telegram.org` still not on cowork sandbox network allowlist (curl exit 56, HTTP 403 from proxy after CONNECT; web_fetch confirms cowork-egress-blocked). 6th consecutive run the trend_pullback reminder has fired without delivery.
    - **Note:** Re-validation note still standing — ExpR slipped to +0.153R (n=649) on 2026-04-30 05:02 UTC fresh universe. Same-cohort peers in queue now total 8 (daily_breakout_2h ExpR +0.466R / Sharpe 13.18 is the new stand-out, surpassing daily_breakout_4h). Saad should review whether to deploy on the original PASS stats, re-queue, or reject in favor of stronger candidates.
  - `daily_breakout` — queued 2026-04-30 (~29.16h ago via source report timestamp 2026-04-30T03:56:39Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: daily_breakout has been pending approval for 29h.\nStats: ExpR +0.417R, DD 4.0%, n=290.\nTo deploy: tell Cowork 'deploy daily_breakout'\nTo reject: tell Cowork 'reject daily_breakout'".
    - **Send result:** FAILED. Same `api.telegram.org` allowlist block (curl exit 56, HTTP 403 from proxy after CONNECT). 2nd consecutive reminder for this strategy.
  - `daily_breakout_24h` — queued 2026-04-30 (~29.16h ago via source report timestamp 2026-04-30T03:56:39Z); **OVER 24h threshold** → reminder Telegram attempted with payload: "⏰ DEPLOY REMINDER: daily_breakout_24h has been pending approval for 29h.\nStats: ExpR +0.384R, DD 5.2%, n=1009.\nTo deploy: tell Cowork 'deploy daily_breakout_24h'\nTo reject: tell Cowork 'reject daily_breakout_24h'".
    - **Send result:** FAILED. Same `api.telegram.org` allowlist block (curl exit 56, HTTP 403 from proxy after CONNECT). 2nd consecutive reminder for this strategy.
  - `daily_breakout_4h` — queued 2026-04-30 (~19.42h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent. (Will cross 24h before next ~11:00Z run; expect first reminder then.)
  - `daily_breakout_7d` — queued 2026-04-30 (~19.42h ago via source report timestamp 2026-04-30T13:40:52Z); under 24h threshold → silent. (Re-validation 2026-05-01 03:18 UTC reported n=0 on 6-symbol limited universe; queued pending re-test on full universe.)
  - `daily_breakout_2h` — queued 2026-05-01 (~5.79h ago via source report timestamp 2026-05-01T03:18:35Z); under 24h threshold → silent.
  - `daily_breakout_12h` — queued 2026-05-01 (~5.79h ago via source report timestamp 2026-05-01T03:18:35Z); under 24h threshold → silent.
  - `daily_breakout_8h` — queued 2026-05-01 (~5.79h ago via source report timestamp 2026-05-01T03:18:35Z); under 24h threshold → silent.
  - `daily_breakout_48h` — queued 2026-05-01 (~5.79h ago via source report timestamp 2026-05-01T03:18:35Z); under 24h threshold → silent. (Marginal PASS — ExpR exactly at +0.201R threshold; report verdict 🟡 KEEP rather than 🟢.)
- **Action needed from Saad:** add `api.telegram.org` to the cowork sandbox network allowlist (Settings → Capabilities, or via workspace admin). Every reminder this task has produced across 6+ runs has been blocked at the proxy. Until that's done, no deploy reminders will reach Telegram. Alternative: review the 9 pending strategies directly here and deploy/reject by replying in-session.
