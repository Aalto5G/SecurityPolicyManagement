import aiohttp
import asyncio, time
import json
import datetime
'''
async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        time_start=time.time()
        for i in range(0, 1000):
            async with session.get('http://127.0.0.1/API/host_policy_user/FQDN/nest0.gwa.demo.') as resp:
                await resp.text()
        time_end=time.time()
        print (time_end-time_start)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))

'''



import random
import asyncio
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        #delay = response.headers.get("DELAY")
        #date = response.headers.get("DATE")
        #print("{}:{} with delay {}".format(date, response.url, delay))
        #a = await response.read()
        #print (a)
        #return a
        return await response.read()


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(r):
    url = "http://127.0.0.1/API/host_policy_user/FQDN/nest0.gwa.demo."
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        start_time=time.time()
        for i in range(r):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        await responses
        end_time=time.time()
        #print ('Time Taken by', r, 'queries in seconds =', end_time-start_time, '\nAnd time taken per query in ms =',
        #       (end_time-start_time)*1000/r, '\nRequests Per second =', r/(end_time-start_time))
        print('And time taken per query in ms =',(end_time-start_time)*1000/r, '\nRequests Per second =', r/(end_time-start_time))

number = 20
loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(number))
loop.run_until_complete(future)









