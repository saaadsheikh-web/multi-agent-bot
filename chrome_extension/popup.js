const API = 'http://127.0.0.1:8787';

async function refresh() {
  const status = document.getElementById('status');
  status.textContent = '...';

  try {
    const r = await fetch(`${API}/health`);
    if (!r.ok) throw new Error('status ' + r.status);
    const data = await r.json();

    document.getElementById('equity').textContent = '$' + data.equity.toFixed(0);
    const pnl = document.getElementById('pnl');
    pnl.textContent = (data.today_pnl >= 0 ? '+' : '') + '$' + data.today_pnl.toFixed(2);
    pnl.className = 'v ' + (data.today_pnl >= 0 ? 'green' : 'red');
    document.getElementById('open').textContent = data.open_trades;
    document.getElementById('regime').textContent = data.regime;
    document.getElementById('keys').textContent = data.keys;

    status.textContent = 'Live · ' + new Date().toLocaleTimeString();
    status.className = 'green';
  } catch(e) {
    status.textContent = 'Bot offline';
    status.className = 'red';
  }
}

function sendCmd(cmd) {
  fetch(`${API}/tv`, { method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      secret: '178f9024586197ca101fac18fdb8796579165984f3e5058b',
      symbol: 'BTC-USDT', side: 'long', confidence: 1, strategy: cmd
    })
  }).then(r => r.text()).then(t => {
    document.getElementById('status').textContent = t;
  });
}

document.getElementById('refresh').onclick = refresh;
document.getElementById('pause').onclick = () => sendCmd('pause');
document.getElementById('resume').onclick = () => sendCmd('resume');
document.getElementById('flatten').onclick = () => { if(confirm('Close ALL?')) sendCmd('flatten_all'); };
document.getElementById('killAgent').onclick = () => {
  const a = document.getElementById('agentSelect').value;
  if(a && confirm('Kill '+a+'?')) sendCmd('kill_'+a);
};

['stoch_rsi','funding_extremes','macd_cross','fibonacci'].forEach(a => {
  const o = document.createElement('option'); o.value = a; o.textContent = a;
  document.getElementById('agentSelect').appendChild(o);
});

refresh();
setInterval(refresh, 30000);
