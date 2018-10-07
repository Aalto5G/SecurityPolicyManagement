import aiohttp
import asyncio, time
import json
import datetime

async def main(loop):
    async with aiohttp.ClientSession(loop=loop) as session:
        j = 0
        for i in range(6000, 8000):


            parameters = json.dumps({'fqdn': 'test'+str(i+j)+'.demo.', 'msisdn':'000000000'+str(i+j), 'ipv4':'192.168.4.'+str(i)})
            async with session.post('http://127.0.0.1/API/host_policy/ID', data=parameters) as resp:
                reply = await resp.text()
                print(reply)


            '''
            insert into host_cetp_negotiations (local_fqdn, remote_fqdn, reputation, direction, uid) values('*','*','*', 'EGRESS', '5849391047123800551');
            insert into host_cetp_negotiations (local_fqdn, remote_fqdn, reputation, direction, uid) values('*','*','*', 'INGRESS', '5849391047123800992');


            insert into host_cetp_policy_required (uid, type, parameter, constraints) values ('5849391047123800551', 'host_cetp_id', 'fqdn', NULL);
            insert into host_cetp_policy_required (uid, type, parameter, constraints) values ('5849391047123800551', 'host_cetp_payload', 'eth', NULL);
            insert into host_cetp_policy_required (uid, type, parameter, constraints) values ('5849391047123800551', 'host_cetp_control_params', 'caep', NULL);

            insert into host_cetp_policy_offered (uid, type, parameter) values ('5849391047123800551', 'host_cetp_id', 'fqdn');
            insert into host_cetp_policy_offered (uid, type, parameter) values ('5849391047123800551', 'host_cetp_payload', 'eth');
            insert into host_cetp_policy_offered (uid, type, parameter) values ('5849391047123800551', 'host_cetp_control_params', 'caep');

            insert into host_cetp_policy_available (uid, type, parameter) values ('5849391047123800551', 'host_cetp_id', 'fqdn');
            insert into host_cetp_policy_available (uid, type, parameter) values ('5849391047123800551', 'host_cetp_payload', 'eth');
            insert into host_cetp_policy_available (uid, type, parameter) values ('5849391047123800551', 'host_cetp_control_params', 'caep');




            insert into host_cetp_policy_required (uid, type, parameter, constraints) values ('5849391047123800992', 'host_cetp_id', 'fqdn', NULL);
            insert into host_cetp_policy_required (uid, type, parameter, constraints) values ('5849391047123800992', 'host_cetp_payload', 'eth', NULL);
            insert into host_cetp_policy_required (uid, type, parameter, constraints) values ('5849391047123800992', 'host_cetp_control_params', 'caep', NULL);

            insert into host_cetp_policy_available (uid, type, parameter) values ('5849391047123800992', 'host_cetp_id', 'fqdn');
            insert into host_cetp_policy_available (uid, type, parameter) values ('5849391047123800992', 'host_cetp_payload', 'eth');
            insert into host_cetp_policy_available (uid, type, parameter) values ('5849391047123800992', 'host_cetp_control_params', 'caep');

            '''

            parameters = json.dumps({'local_fqdn': 'test'+str(i+j)+'.demo.', 'remote_fqdn':'*', 'payload_type':'eth', 'value':1})
            async with session.post('http://127.0.0.1/API/host_cetp/cetp_payload', data=parameters) as resp:
                reply = await resp.text()
                print(reply)

                parameters = json.dumps({'local_fqdn': 'test' + str(i + j) + '.demo.', 'id_type': 'fqdn', 'value': 'test' + str(i + j) + '.demo.'})
            async with session.post('http://127.0.0.1/API/host_cetp/cetp_id', data=parameters) as resp:
                reply = await resp.text()
                print(reply)

            parameters = json.dumps({'local_fqdn': 'test' + str(i + j) + '.demo.', 'remote_fqdn': '*', 'direction': '*', 'parameters': 'caep', 'value':'["195.148.124.145"]'})
            async with session.post('http://127.0.0.1/API/host_cetp/cetp_control_params', data=parameters) as resp:
                reply = await resp.text()
                print(reply)

            parameters = json.dumps({'local_fqdn': 'test' + str(i + j) + '.demo.', 'remote_fqdn': '*', 'direction': '*',
                                     'parameters': 'ack', 'value': '["195.148.124.145"]'})
            async with session.post('http://127.0.0.1/API/host_cetp/cetp_control_params', data=parameters) as resp:
                reply = await resp.text()
                print(reply)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))



