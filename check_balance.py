#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""Check BloFin account balance."""
import sys; sys.path.insert(0, '/Users/saad/multi_agent_bot')
import bot
bf = bot.BloFin()

# Try multiple account endpoint names
endpoints = [
    ('mix_account', 'get_account'),
    ('account', 'get_account'),
    ('mix_account', 'get_accounts'),
    ('account', 'get_balance'),  # needs account_type
    ('wallet', 'get_all_balance'),
    ('asset', 'get_balances'),
]

for mod, method_name in endpoints:
    try:
        cl = getattr(bf.client, mod, None)
        if cl:
            fn = getattr(cl, method_name, None)
            if fn:
                r = fn()
                print(f'--- {mod}.{method_name} ---')
                import json
                print(json.dumps(r, indent=2, default=str)[:1000])
    except Exception as e:
        print(f'{mod}.{method_name}: {type(e).__name__}: {e}')

# Also check what methods exist on bf.client
print('\n--- Available methods on bf.client ---')
for attr in dir(bf.client):
    if not attr.startswith('_'):
        print(f'  {attr}')
