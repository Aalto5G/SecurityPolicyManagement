import aiohttp
import asyncio, time
import json
import datetime

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        for i in range(0, 1):
            if i == 0:
                x = datetime.datetime.now()
                print ('start time', x, '\n\n\n')
            if i == 9999:
                y = datetime.datetime.now()
                print('end time', y)
                print ('Total time taken final', y - x)
            parameters = json.dumps([{'fqdn':'nest0.gwa.demo.', 'cesapp_id':12,'type':'FIREWALL_ADMIN','active':'1','priority':'10',
                                     'direction':'EGRESS','src':'1.1.2.1','dst':'2.2.2.2','sport':'50','dport':'50',
                                     'protocol':'2012','target':'ACCEPT','comment':'{"comment":"Host DNS limit"}',
                                     'raw_data':'{"hashlimit":"1001"}'},{'fqdn':'nest0.gwa.demo.', 'cesapp_id':34,'type':'FIREWALL_ADMIN','active':'1','priority':'10',
                                     'direction':'EGRESS','src':'1.1.2.1','dst':'2.2.2.2','sport':'50','dport':'50',
                                     'protocol':'2034','target':'ACCEPT','comment':'{"comment":"Host DNS limit"}',
                                     'raw_data':'{"hashlimit":"1001"}'},{'fqdn':'nest0.gwa.demo.', 'cesapp_id':56,'type':'FIREWALL_ADMIN','active':'1','priority':'10',
                                     'direction':'EGRESS','src':'1.1.2.1','dst':'2.2.2.2','sport':'50','dport':'50',
                                     'protocol':'2056','target':'ACCEPT','comment':'{"comment":"Host DNS limit"}',
                                     'raw_data':'{"hashlimit":"1001"}'}])
            async with session.put('http://127.0.0.1:80/API/host_policy_cesapp', data=parameters) as resp:
            #async with session.post('http://127.0.0.1/testing', data=parameters) as resp:
                reply = await resp.text()
                print (reply)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))













