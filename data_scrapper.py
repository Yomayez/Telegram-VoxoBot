import aiohttp
import asyncio

async def voxo_status():
    async with aiohttp.ClientSession() as session:
        async with session.get(url='https://api.vo-xo.com/status') as resp:
            data = await resp.json()

    if bool(data['online']):
        data_res = {
            'status' : bool(data['online']),
            'online': int(data['players']['online']),
            'uptime': int(data['uptime']['current_seconds']),
            'peak_online': int(data['peaks']['today'])
        }

    else:
        data_res = {
            'status' : False,
        }

    return data_res

async def voxo_stats():
    async with aiohttp.ClientSession() as session:
        async with session.get(url='https://api.vo-xo.com/community/stats',) as resp:
            data = await resp.json()

    data_res = {
        'users': int(data['players_confirmed']),
        'clans': int(data['clans']),
        'playtime': int(data['total_playtime_ms']),
    }

    return data_res