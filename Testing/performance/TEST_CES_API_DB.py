#!/usr/bin/env python3

#import mysql.connector
import asyncio
import json

from src.REST_server.CES_API_DB import CesApiDatabase

error_list = ['Successful', 'No data exists with these Parameters.', 'Error Executing Statement', 'Error Reading Data', 'Unknown error occurred.']





async def test1(mysql_obj):
    '''
    Policy Retrival for a user. Either comma separated tables, or one table name or no table name for all policies
    '''
    id_type = 'fqdn'
    id_value = 'nest0.gwa.demo.'
    policy_name = ['Firewall']
    data = await mysql_obj.host_policy_user_get(id_type, id_value)
    #print('test1() host_policy_get({}, {}, {})\n{}'.format(id_type, id_value, policy_name, data))
    print('-----------------------------')
    print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test2(mysql_obj):
    '''
    Retrieve all policies of a table or use ID for any specific row of a table
    '''
    data = await mysql_obj.host_policy_get('Firewall', 5)
    print('-----------------------------')
    print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test3(mysql_obj):
    '''
    Insert test in host_id table
    '''
    data = await mysql_obj.host_policy_insert('ID', msisdn='123123123123', fqdn='test.aalto.com', ipv4='10.10.10.10')
    print('test3() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test4(mysql_obj):
    '''
    test insert query creation function for insert in host_group
    '''
    data = await mysql_obj.host_policy_insert('GROUP', fqdn='test.aalto.com', group='prepaid1')
    print('test4() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')

async def test5(mysql_obj):
    '''
    test insert query creation function for insert in host_circularpool
    '''
    data = await mysql_obj.host_policy_insert('CIRCULARPOOL', fqdn='test.aalto.com', raw_data='{"test":"test"}')
    print('test5() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test6(mysql_obj):
    '''
    test insert query creation function for insert in host_carriergrade
    '''
    data = await mysql_obj.host_policy_insert('CARRIERGRADE', fqdn='test.aalto.com', raw_data='{"test":"test"}')
    print('test6() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')

async def test7(mysql_obj):
    '''
    test insert query creation function for insert in host_sfqdn
    '''
    data = await mysql_obj.host_policy_insert('SFQDN', fqdn='test.aalto.com', sfqdn='http.hassaan.aalto.fi', proxy_required=1, carriergrade=0, protocol='5', port='10', loose_packet=3)
    print('test7() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test8(mysql_obj):
    '''
    test insert query creation function for insert in host_ucop
    '''
    data = await mysql_obj.host_policy_insert('Firewall', type='firewall_admin', fqdn='test.aalto.com', reputation=0.5, active=1, network_support='http', direction='EGRESS', src='1.1.1.1', dst='1.1.1.1', sport='50', dport='1,2,3', protocol=17, target='ACCEPT', comment='{"test":"test"}')
    print('test8() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')




async def test9(mysql_obj):
    '''
    Update test in host_id table
    '''
    data = await mysql_obj.host_policy_update('ID', id=1, msisdn='321321321', fqdn='test.aalto.com', ipv4='11.11.11.11')
    print('test9() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test10(mysql_obj):
    '''
    test Update query creation function for insert in host_group
    '''
    data = await mysql_obj.host_policy_update('GROUP', id=1, fqdn='test.aalto.com', group='httpprepaid1')
    print('test10() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')

async def test11(mysql_obj):
    '''
    test Update query creation function for insert in host_circularpool
    '''
    data = await mysql_obj.host_policy_update('CIRCULARPOOL', id=1, fqdn='test.aalto.com', raw_data='{"httptest":"test"}')
    print('test11() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test12(mysql_obj):
    '''
    test Update query creation function for insert in host_carriergrade
    '''
    data = await mysql_obj.host_policy_update('CARRIERGRADE', id=1, fqdn='test.aalto.com', raw_data='{"httptest":"test"}')
    print('test12() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')

async def test13(mysql_obj):
    '''
    test Update query creation function for insert in host_sfqdn
    '''
    data = await mysql_obj.host_policy_update('SFQDN', id=1, fqdn='test.aalto.com', sfqdn='httptest.hassaan.aalto.fi', proxy_required=1, carriergrade=0, protocol='5', port='10', loose_packet=3)
    print('test13() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')

async def test14(mysql_obj):
    '''
    test Update query creation function for insert in host_ucop
    '''
    data = await mysql_obj.host_policy_update('Firewall', id=1, type='firewall_admin', reputation=0.5, active=1, direction='EGRESS', src='1.1.1.1', dst='12.12.12.12', sport='50', dport='1,2,3', protocol=17, target='ACCEPT', comment='{"test":"test"}')
    print('test14() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test15(mysql_obj):
    '''
    test retrieve bootstrap policies
    '''
    data = await mysql_obj.host_policy_delete('ID', '1')
    #print('test() reply= {}'.format(data))
    print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test16(mysql_obj):
    '''
    test retrieve bootstrap policies
    '''
    data = await mysql_obj.host_bootstrap_get(['IPSET','Circularpool'])
    #print('test() reply= {}'.format(data))
    print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test27(mysql_obj):
    '''
    test for retrieving required policies
    '''
    data = await mysql_obj.host_cetp_user_get('hosta1.cesa.lte.', '*', 'EGRESS')
    #print('test() reply= {}'.format(data))
    print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test28(mysql_obj):
    '''
    test for retrieving required policies
    '''
    data = await mysql_obj.host_cetp_get('cetp_control_params')
    print('test() reply= {}'.format(data))
    #print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test29(mysql_obj):
    '''
    test insert query creation function for insert in host_cept_policy_required
    '''
    data = await mysql_obj.host_cetp_insert('request', uid='abcababc', type='host_cetp_id', parameter='yuyuyuy',
                                            constraint='')
    print('test29() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test30(mysql_obj):
    '''
    test insert query creation function for insert in host_cept_policy_available
    '''
    data = await mysql_obj.host_cetp_insert('available', uid='abcababc', type='host_cetp_id', parameter='yuyuyuy',
                                            constraint='')
    print('test30() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def test31(mysql_obj):
    '''
    test insert query creation function for insert in host_cept_policy_available
    '''
    data = await mysql_obj.host_cetp_insert('offer', uid='abcababc', type='host_cetp_id', parameter='yuyuyuy',
                                            constraint='')
    print('test31() reply= {}'.format(data))
    # print(json.dumps(data, indent=4))
    print('-----------------------------')


async def run_tests():
    mysql_obj = CesApiDatabase()
    await mysql_obj.connect()

    #loop.create_task(test1(mysql_obj))
    #loop.create_task(test2(mysql_obj))

    #loop.create_task(test3(mysql_obj))
    #await asyncio.sleep(1)
    #loop.create_task(test4(mysql_obj))
    #loop.create_task(test5(mysql_obj))
    #loop.create_task(test6(mysql_obj))
    #loop.create_task(test7(mysql_obj))
    #loop.create_task(test8(mysql_obj))

    #loop.create_task(test9(mysql_obj))

    #loop.create_task(test10(mysql_obj))
    #loop.create_task(test11(mysql_obj))
    #loop.create_task(test12(mysql_obj))
    #loop.create_task(test13(mysql_obj))
    #loop.create_task(test14(mysql_obj))

    #loop.create_task(test15(mysql_obj))
    #loop.create_task(test16(mysql_obj))

    #loop.create_task(test17(mysql_obj))
    #loop.create_task(test18(mysql_obj))
    #loop.create_task(test19(mysql_obj))
    #loop.create_task(test20(mysql_obj))
    #loop.create_task(test21(mysql_obj))
    #loop.create_task(test22(mysql_obj))
    #loop.create_task(test23(mysql_obj))
    #loop.create_task(test24(mysql_obj))
    #loop.create_task(test25(mysql_obj))
    #loop.create_task(test26(mysql_obj))

    #loop.create_task(test27(mysql_obj))
    #loop.create_task(test28(mysql_obj))
    #loop.create_task(test29(mysql_obj))
    loop.create_task(test30(mysql_obj))
    #loop.create_task(test31(mysql_obj))

    await asyncio.sleep(1)
    await mysql_obj.disconnect()


loop = asyncio.get_event_loop()

if __name__ == '__main__':
    try:
        loop.set_debug(True)
        loop.create_task(run_tests())
        loop.run_forever()
    except KeyboardInterrupt:
        print('\nInterrupted\n')
    finally:
        # next two lines are required for actual aiohttp resource cleanup
        loop.stop()
        #loop.run_forever()
        loop.close()



#pymysql.err.IntegrityError:   for duplicate entries

