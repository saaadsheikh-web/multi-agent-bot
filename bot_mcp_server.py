#!/usr/bin/env python3
"""Hermes MCP Server — BloFin trading bot monitor.
Provides tools for Hermes to check bot health, agent PnL, open positions, and more.

Run: python3 bot_mcp_server.py
Connects via stdio MCP protocol to Hermes."""

import sqlite3, os, json, asyncio, subprocess
from datetime import datetime, timezone

# --- MCP Protocol Helpers ---
async def handle_request(request):
    """Handle a single MCP JSON-RPC request."""
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}}
        }}
    elif method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "tools": [
                {
                    "name": "check_bot_health",
                    "description": "Check bot status: running, equity, open positions, latest PnL",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "get_agent_pnl",
                    "description": "Get per-agent PnL from the database",
                    "inputSchema": {"type": "object", "properties": {
                        "agent": {"type": "string", "description": "Agent name (optional — all agents if omitted)"}
                    }}
                },
                {
                    "name": "get_open_positions",
                    "description": "Get all currently open positions from the bot DB",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "run_monitor",
                    "description": "Run the agent_monitor.py and return full report",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "get_bot_log",
                    "description": "Get last N lines of the bot log",
                    "inputSchema": {"type": "object", "properties": {
                        "lines": {"type": "integer", "description": "Number of lines (default 20)"}
                    }}
                },
                {
                    "name": "tv_alert_processed",
                    "description": "Log that a TV webhook signal was received and processed",
                    "inputSchema": {"type": "object", "properties": {
                        "symbol": {"type": "string"},
                        "side": {"type": "string"},
                        "confidence": {"type": "integer"},
                        "reason": {"type": "string"}
                    }}
                }
            ]
        }}
    elif method == "tools/call":
        tool = params.get("name")
        args = params.get("arguments", {})
        
        if tool == "check_bot_health":
            result = await check_bot_health()
        elif tool == "get_agent_pnl":
            result = get_agent_pnl(args.get("agent"))
        elif tool == "get_open_positions":
            result = get_open_positions()
        elif tool == "run_monitor":
            result = run_monitor()
        elif tool == "get_bot_log":
            result = get_bot_log(args.get("lines", 20))
        elif tool == "tv_alert_processed":
            result = tv_alert_processed(args.get("symbol"), args.get("side"), 
                                        args.get("confidence"), args.get("reason"))
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool not found: {tool}"}}
        
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
    
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}

BOT_DIR = os.path.expanduser("~/multi_agent_bot")
DB_PATH = os.path.join(BOT_DIR, "bot.db")
LOG_PATH = os.path.join(BOT_DIR, "bot.log")

async def check_bot_health():
    result = {}
    # Check if bot process is running
    try:
        r = subprocess.run(["pgrep", "-f", "python.*bot.py"], capture_output=True, text=True, timeout=5)
        pids = [p for p in r.stdout.strip().split('\n') if p]
        pids = [p for p in pids if int(p) != os.getpid() and int(p) != os.getppid()]
        result["bot_running"] = len(pids) > 0
        result["pids"] = pids
    except:
        result["bot_running"] = False
        result["pids"] = []
    
    # Last log lines
    result["last_log"] = get_bot_log(5)
    
    # Open positions
    result["open_positions"] = get_open_positions()
    
    # Agent PnL summary
    pnl = get_agent_pnl(None)
    result["agents"] = pnl
    
    return result

def get_agent_pnl(agent_filter=None):
    if not os.path.exists(DB_PATH):
        return {"error": "No DB found"}
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        if agent_filter:
            c.execute("SELECT agent, COUNT(*) as trades, COALESCE(SUM(pnl),0) as total_pnl, COALESCE(SUM(CASE WHEN pnl>0 THEN 1 ELSE 0 END),0) as wins, COALESCE(MAX(closed_at),'never') as last_closed FROM trades WHERE status='closed' AND pnl IS NOT NULL AND agent=? GROUP BY agent", (agent_filter,))
        else:
            c.execute("SELECT agent, COUNT(*) as trades, COALESCE(SUM(pnl),0) as total_pnl, COALESCE(SUM(CASE WHEN pnl>0 THEN 1 ELSE 0 END),0) as wins, COALESCE(MAX(closed_at),'never') as last_closed FROM trades WHERE status='closed' AND pnl IS NOT NULL GROUP BY agent ORDER BY total_pnl DESC")
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows
    except Exception as e:
        return {"error": str(e)}

def get_open_positions():
    if not os.path.exists(DB_PATH):
        return []
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT agent, symbol, side, entry_price, qty, notional, opened_at, pnl FROM trades WHERE status='open' ORDER BY opened_at DESC")
        rows = [dict(r) for r in c.fetchall()]
        conn.close()
        return rows
    except:
        return []

def run_monitor():
    script = os.path.join(BOT_DIR, "agent_monitor.py")
    if not os.path.exists(script):
        return {"error": "agent_monitor.py not found"}
    try:
        r = subprocess.run(["python3", script], capture_output=True, text=True, timeout=15, cwd=BOT_DIR)
        return {"output": r.stdout, "error": r.stderr if r.stderr else None}
    except Exception as e:
        return {"error": str(e)}

def get_bot_log(n=20):
    if not os.path.exists(LOG_PATH):
        return {"error": "No log found"}
    try:
        with open(LOG_PATH) as f:
            lines = f.readlines()
        last = [l.strip() for l in lines[-n:]]
        return {"lines": last}
    except Exception as e:
        return {"error": str(e)}

def tv_alert_processed(symbol, side, confidence, reason):
    entry = f"[{datetime.now(timezone.utc).isoformat()}] TV_ALERT {symbol} {side} conf={confidence} reason={reason}"
    log_file = os.path.join(BOT_DIR, "tv_webhook_log.txt")
    with open(log_file, "a") as f:
        f.write(entry + "\n")
    return {"logged": True, "entry": entry}

async def main():
    """MCP stdio server — reads JSON-RPC from stdin, writes to stdout."""
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    
    while True:
        try:
            line = await reader.readline()
            if not line:
                break
            request = json.loads(line.decode().strip())
            response = await handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            continue
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    import sys
    asyncio.run(main())
