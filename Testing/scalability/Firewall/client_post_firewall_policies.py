import aiohttp
import asyncio, time
import json
import datetime

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        j = 0
        for i in range(6000,8000):
            #x = datetime.datetime.now()
            #y = datetime.datetime.now()
            #print ('Total time taken final', y - x)

            parameters = json.dumps({'fqdn': 'test'+str(i+j)+'.demo.', 'msisdn':'000000000'+str(i+j), 'ipv4':'192.168.4.'+str(i)})
            async with session.post('http://127.0.0.1/API/host_policy/ID', data=parameters) as resp:
                reply = await resp.text()
                print(reply)
            parameters = json.dumps({'fqdn': 'test'+str(i+j)+'.demo.', 'group':'Prepaid'})
            async with session.post('http://127.0.0.1/API/host_policy/GROUP', data=parameters) as resp:
                reply = await resp.text()
                print(reply)
            parameters = json.dumps({'fqdn': 'test'+str(i+j)+'.demo.', 'type':'FIREWALL_ADMIN', 'priority':0, 'direction':'EGRESS', 'protocol':'17', 'dport':'53',
                                              'target':'REJECT'})
            async with session.post('http://127.0.0.1/API/host_policy/FIREWALL', data=parameters) as resp:
                reply = await resp.text()
                print(reply)
            parameters = json.dumps({'fqdn': 'test'+str(i+j)+'.demo.', 'type': 'FIREWALL_USER', 'priority': 100, 'direction': 'EGRESS',
                                     'target': 'ACCEPT'})
            async with session.post('http://127.0.0.1/API/host_policy/FIREWALL', data=parameters) as resp:
                reply = await resp.text()
                print(reply)

            parameters = json.dumps({'fqdn': 'test' + str(i + j) + '.demo.', 'type': 'FIREWALL_USER', 'priority': 100,
                                     'direction': 'INGRESS','target': 'ACCEPT'})
            async with session.post('http://127.0.0.1/API/host_policy/FIREWALL', data=parameters) as resp:
                reply = await resp.text()
                print(reply)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))













