#!/opt/homebrew/Caskroom/miniconda/base/bin/python3.13
"""Test the AI arbiter chain."""
import os, sys, asyncio, aiohttp
sys.path.insert(0, '/Users/saad/multi_agent_bot')
import bot

async def test():
    async with aiohttp.ClientSession() as session:
        print(f"DEEPSEEK key: {bot.DEEPSEEK_API_KEY[:8]}..." if bot.DEEPSEEK_API_KEY else "NO DEEPSEEK KEY")
        print(f"DEEPSEEK model: {bot.DEEPSEEK_MODEL}")
        print(f"OPENROUTER key: {bot.OPENROUTER_API_KEY[:8]}..." if bot.OPENROUTER_API_KEY else "NO OR KEY")
        print(f"OPENROUTER model: {bot.OPENROUTER_MODEL}")
        print(f"OPENROUTER_FREE_ONLY: {bot.OPENROUTER_FREE_ONLY}")
        
        # Test DeepSeek
        print("\n--- Testing DeepSeek ---")
        try:
            async with session.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {bot.DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
                json={"model": bot.DEEPSEEK_MODEL, "messages": [{"role": "user", "content": '{"approve": true}'}], "max_tokens": 10},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                text = await r.text()
                print(f"Status: {r.status}")
                print(f"Response: {text[:300]}")
        except Exception as e:
            print(f"DeepSeek error: {e}")
        
        # Test OpenRouter
        print("\n--- Testing OpenRouter ---")
        try:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {bot.OPENROUTER_API_KEY}", "Content-Type": "application/json",
                         "HTTP-Referer": "https://infinitylux.co.uk", "X-Title": "MAB"},
                json={"model": bot.OPENROUTER_MODEL, "messages": [{"role": "user", "content": '{"approve": true}'}], "max_tokens": 10},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as r:
                text = await r.text()
                print(f"Status: {r.status}")
                print(f"Response: {text[:300]}")
        except Exception as e:
            print(f"OpenRouter error: {e}")

asyncio.run(test())
