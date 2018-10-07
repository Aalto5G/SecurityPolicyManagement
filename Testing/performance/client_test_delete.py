import aiohttp
import asyncio, time
import json
import datetime

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        for i in range(0, 1):
            async with session.delete('http://127.0.0.1/API/host_policy/FIREWALL', data=parameters) as resp:
            #async with session.post('http://127.0.0.1/testing', data=parameters) as resp:
                reply = await resp.text()
                print (reply)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))













