# Infinity Lux Concierge — OpenClaw + Website Chat Widget

Two pieces. Set up Part 1 first (OpenClaw side), then Part 2 (website side).

---

## Part 1 — Set up the Concierge agent in OpenClaw

```bash
# Create a dedicated Infinity Lux agent in OpenClaw
openclaw agents create infinity_lux_concierge --description "Infinity Lux website concierge — handles customer enquiries"

# Set the system prompt for this agent (paste the full prompt below)
openclaw config set agents.infinity_lux_concierge.systemPrompt "$(cat <<'EOF'
You are the Infinity Lux Concierge — a polished, warm, professional assistant for a London-based luxury chauffeur and events company.

Your role:
- Answer questions about services (chauffeur, airport transfers, weddings, corporate events, daily rentals)
- Qualify leads by gathering: full name, email, phone, service type, date, pickup location
- Quote indicative prices when asked (e.g., London airport transfer £150-300, hourly chauffeur £80-120/hr)
- Escalate complex requests by emailing saaadsheikh@gmail.com with the conversation summary
- Be warm but efficient — luxury without pretension

Rules:
- Never promise availability without checking with Saad first
- Always collect contact details before quoting
- Keep responses to 2-3 sentences unless explaining a service in detail
- Use British English (favour, colour)
- Never discuss competitors

If a customer wants to book, respond with: "I'll have Saad confirm and email you within 2 hours. Could I have your name, email, phone, date, and pickup address?"

After collecting details, send to Saad via email and reply: "Thank you, [Name]. Saad will be in touch within 2 hours."
EOF
)"

# Restart gateway to apply
launchctl kickstart -k gui/$(id -u)/openclaw.gateway 2>/dev/null
```

## Part 2 — Drop-in chat widget for your website

Save this as `concierge-widget.html` and paste the contents into your website's HTML (just before `</body>`):

```html
<!-- Infinity Lux Concierge Widget — start -->
<style>
  #ilux-chat { position:fixed; bottom:20px; right:20px; width:60px; height:60px; border-radius:50%;
    background:#0a0a0a; color:#d4af37; border:none; cursor:pointer; font-size:28px; z-index:9999;
    box-shadow:0 4px 24px rgba(0,0,0,0.3); }
  #ilux-chat-window { position:fixed; bottom:90px; right:20px; width:360px; height:500px;
    background:white; border-radius:12px; box-shadow:0 8px 32px rgba(0,0,0,0.2); display:none;
    flex-direction:column; z-index:9999; font-family:-apple-system, sans-serif; }
  #ilux-chat-header { background:#0a0a0a; color:#d4af37; padding:14px 18px; border-radius:12px 12px 0 0;
    font-weight:600; }
  #ilux-chat-messages { flex:1; padding:14px; overflow-y:auto; }
  #ilux-chat-msg { margin-bottom:10px; padding:8px 12px; border-radius:10px; max-width:80%; line-height:1.4; }
  .ilux-bot { background:#f3f3f3; align-self:flex-start; }
  .ilux-user { background:#0a0a0a; color:white; align-self:flex-end; margin-left:auto; }
  #ilux-chat-input { display:flex; border-top:1px solid #eee; padding:8px; }
  #ilux-chat-input input { flex:1; padding:8px 12px; border:1px solid #ddd; border-radius:20px; }
  #ilux-chat-input button { margin-left:6px; background:#d4af37; color:#0a0a0a; border:none;
    border-radius:20px; padding:8px 18px; cursor:pointer; font-weight:600; }
</style>

<button id="ilux-chat" onclick="iluxToggle()">💬</button>
<div id="ilux-chat-window">
  <div id="ilux-chat-header">Infinity Lux Concierge</div>
  <div id="ilux-chat-messages">
    <div id="ilux-chat-msg" class="ilux-bot">Welcome to Infinity Lux. How may I help you today?</div>
  </div>
  <div id="ilux-chat-input">
    <input id="ilux-input-field" type="text" placeholder="Type a message…" onkeydown="if(event.key==='Enter')iluxSend()">
    <button onclick="iluxSend()">Send</button>
  </div>
</div>

<script>
  // CHANGE THIS to your OpenClaw webhook URL once exposed via ngrok or a public domain.
  const ILUX_WEBHOOK = 'https://YOUR-NGROK-URL.ngrok-free.app/webhook/infinity_lux';

  function iluxToggle() {
    const w = document.getElementById('ilux-chat-window');
    w.style.display = w.style.display === 'flex' ? 'none' : 'flex';
  }

  async function iluxSend() {
    const input = document.getElementById('ilux-input-field');
    const text = input.value.trim();
    if (!text) return;
    iluxAddMsg(text, 'user');
    input.value = '';

    try {
      const res = await fetch(ILUX_WEBHOOK, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: text, sessionId: iluxSessionId()})
      });
      const data = await res.json();
      iluxAddMsg(data.reply || 'Apologies — please email us at info@infinitylux.co.uk', 'bot');
    } catch(e) {
      iluxAddMsg('Apologies — connection issue. Email us at info@infinitylux.co.uk', 'bot');
    }
  }

  function iluxAddMsg(text, kind) {
    const msgs = document.getElementById('ilux-chat-messages');
    const div = document.createElement('div');
    div.className = 'ilux-bot ' + (kind === 'user' ? 'ilux-user' : 'ilux-bot');
    div.style.cssText = 'margin-bottom:10px;padding:8px 12px;border-radius:10px;max-width:80%;line-height:1.4;' +
      (kind === 'user' ? 'background:#0a0a0a;color:white;margin-left:auto;text-align:right;' : 'background:#f3f3f3;');
    div.textContent = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function iluxSessionId() {
    let id = localStorage.getItem('ilux_sid');
    if (!id) { id = 'sess_' + Math.random().toString(36).slice(2); localStorage.setItem('ilux_sid', id); }
    return id;
  }
</script>
<!-- Infinity Lux Concierge Widget — end -->
```

## Part 3 — Expose OpenClaw via ngrok (so the widget can reach it)

```bash
# Install ngrok if not already
brew install ngrok

# Expose OpenClaw's gateway port to a public URL
ngrok http 18789
```

ngrok will print a URL like `https://abc123.ngrok-free.app`. **Copy that URL** and paste it in the widget's `ILUX_WEBHOOK` line, replacing `YOUR-NGROK-URL`.

## Part 4 — Add the widget to your website

- WordPress: paste into theme's footer.php, or use "Insert Headers and Footers" plugin
- Squarespace: Settings → Advanced → Code Injection → Footer
- Webflow: Project Settings → Custom Code → Footer Code
- Custom HTML: paste before `</body>` in your site

That's it. Customer types message → goes to OpenClaw via ngrok → Kimi K2 generates reply via OpenClaw's Concierge agent prompt → reply shown in chat widget.

---

## Maintenance

- Update the agent prompt: `openclaw config set agents.infinity_lux_concierge.systemPrompt "..."`
- See conversations: `openclaw sessions list | grep infinity_lux`
- Restart after changes: `launchctl kickstart -k gui/$(id -u)/openclaw.gateway`
