import aiohttp
import asyncio, time
import json
import datetime

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        for i in range(0, 10000):
            if i == 0:
                x = datetime.datetime.now()
                print ('start time', x, '\n\n\n')
            if i == 9999:
                y = datetime.datetime.now()
                print('end time', y)
                print ('Total time taken final', y - x)
            #async with session.get('http://127.0.0.1/API/host_policy_user/FQDN/nest0.gwa.demo.') as resp:
            async with session.get('http://127.0.0.1/testing') as resp:
                #print (await resp.text())
                await resp.text()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))











