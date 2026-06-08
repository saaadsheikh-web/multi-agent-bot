import sqlite3
con = sqlite3.connect('/sessions/relaxed-pensive-clarke/mnt/multi_agent_bot/bot.db')
cur = con.cursor()
# Last 5 connors_rsi2
cur.execute("SELECT pnl, closed_at FROM trades WHERE agent='connors_rsi2' AND status='closed' ORDER BY closed_at DESC LIMIT 5")
last5 = cur.fetchall()
print('Last 5 connors_rsi2:')
for r in last5: print(r)
pnls = [r[0] for r in last5]
gw = sum(p for p in pnls if p>0)
gl = sum(p for p in pnls if p<0)
print(f'NET: {sum(pnls):.4f}, PF: {gw/abs(gl) if gl else float("inf"):.2f}')
# Open trades
cur.execute("SELECT id, agent, symbol, side, entry_price, qty, notional, opened_at FROM trades WHERE status!='closed'")
print('\nOPEN TRADES:')
for r in cur.fetchall(): print(r)
# Last 10 connors_rsi2 WR
cur.execute("SELECT pnl FROM trades WHERE agent='connors_rsi2' AND status='closed' ORDER BY closed_at DESC LIMIT 10")
l10 = [r[0] for r in cur.fetchall()]
wins10 = sum(1 for p in l10 if p>0)
gw = sum(p for p in l10 if p>0); gl = sum(p for p in l10 if p<0)
pf10 = gw/abs(gl) if gl else float('inf')
print(f'\nLast 10 connors_rsi2: WR={wins10/10*100:.0f}%, NET=${sum(l10):.4f}, PF={pf10:.2f}')
# Last 20 connors_rsi2 WR/PF
cur.execute("SELECT pnl FROM trades WHERE agent='connors_rsi2' AND status='closed' ORDER BY closed_at DESC LIMIT 20")
l20 = [r[0] for r in cur.fetchall()]
wins20 = sum(1 for p in l20 if p>0)
gw20 = sum(p for p in l20 if p>0); gl20 = sum(p for p in l20 if p<0)
pf20 = gw20/abs(gl20) if gl20 else float('inf')
print(f'Last 20 connors_rsi2: WR={wins20/20*100:.0f}%, NET=${sum(l20):.4f}, PF={pf20:.2f}')
# funding_extremes
cur.execute("SELECT pnl, closed_at FROM trades WHERE agent='funding_extremes' AND status='closed' ORDER BY closed_at DESC")
fe = cur.fetchall()
print(f'\nfunding_extremes (all {len(fe)}):')
for r in fe: print(r)
