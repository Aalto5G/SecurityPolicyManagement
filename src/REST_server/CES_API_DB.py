"""
BSD 3-Clause License
Copyright (c) 2018, Muhammad Hassaan Bin Mohsin, Aalto University, Finland
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

#!/usr/bin/env python3


import json
import socket, uuid
import uuid, dns, dns.message, dns.query

from errorsfile import API_ERROR
from Validator import Validator
from aiomysql_client import MySQLClient



table_mapping = {'ID':'host_ids', 'FIREWALL':'firewall_policies', 'HOST_POLICY_IDENTITY':'host_policy_identity',
                 'HOST_POLICIES':'host_policies', 'CES_POLICIES':'ces_policies', 'CES_POLICY_IDENTITY':'ces_policy_identity'}

dns_ip = '8.8.8.8'
dns_port = 53
soa = 'CES_AALTO.Testnetwork.'
dns_address = (dns_ip,dns_port)


class CesApiDatabase():

    def __init__(self, **kwargs):
        self.db_bootstrap = kwargs.setdefault('db_bootstrap', None)
        self.db_host = kwargs.setdefault('db_host', None)
        # Register function pointers in a dictionary
        self._register_function_pointers()


    async def dns_connection(self):
        '''
        Creating a socket for dns connection
        :return: Socket object
        '''
        # Create a socket (SOCK_DGRAM created UDP socket)
        sock = await socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return sock


    async def connect(self):
        '''
        Create connection to the two different databases which would be used in relevant functions
        '''
        if not isinstance(self.db_host, MySQLClient):
            self.db_host = MySQLClient(host='localhost', port=3306, user='root', password='take5',
                                       database='Session_Policies')
            await self.db_host.connect()


        if not isinstance(self.db_bootstrap, MySQLClient):
            self.db_bootstrap = MySQLClient(host='localhost', port=3306, user='root', password='take5',
                                            database='Bootstrap_Policies')
            await self.db_bootstrap.connect()


    async def disconnect(self):
        '''
        Close all the connections to all the databases
        '''
        await self.db_host.close()
        await self.db_bootstrap.close()


    def _register_function_pointers(self):
        # Initialize dictionary of function pointers
        self._host_policy_functions = {'ID':{'insert':self._host_policy_insert_id,
                                               'update':self._host_policy_update_id,
                                               'postprocess':self._host_policy_insert_id},
                                       'FIREWALL':{'insert':self._host_policy_insert_firewall,
                                                   'update':self._host_policy_update_firewall,
                                                   'postprocess':self._host_policy_insert_firewall},
                                       'HOST_POLICY_IDENTITY': {'insert':self._host_policy_insert_cetp_policy_identity,
                                                    'update':self._host_policy_update_cetp_policy_identity,
                                                    'postprocess':self._host_policy_insert_cetp_policy_identity},
                                       'HOST_POLICIES': {'insert': self._host_policy_insert_cetp_policies,
                                                    'update':self._host_policy_update_cetp_policies,
                                                    'postprocess':self._host_policy_insert_cetp_policies},
                                       'CES_POLICY_IDENTITY': {'insert': self._host_policy_insert_ces_policy_identity,
                                                         'update': self._host_policy_update_ces_policy_identity,
                                                         'postprocess': self._host_policy_insert_cetp_policies},
                                       'CES_POLICIES': {'insert': self._host_policy_insert_ces_policies,
                                                         'update': self._host_policy_update_ces_policies,
                                                         'postprocess': self._host_policy_insert_cetp_policies}
                                       }


    #####################################################################
    #####################################################################
    #####################################################################
    # Testing Functions:


    async def _host_get_user_ids(self, id_type, id_value):
        '''
        Get all IDs of user and raise error if no user exists with provided credentials
        :param id_type: Type of query. can be FQDN, IP, MSISDN or Username
        :param id_value:User identity for the relevant ID-Type
        :return:Raise error in case of no user existance or return user details
        '''
        if id_type not in ['fqdn', 'msisdn', 'ipv4', 'username']:
            error = "idtype not supported {}".format(id_type)
            raise API_ERROR(1001, error)
        # Get ids for the user based on given id
        query = "select uuid,fqdn,msisdn,ipv4 from host_ids where {} = '{}'".format(id_type, id_value)
        data = await self.db_host.fetchone(query)
        if not data:
            error = "No user found for id_type={} and id_value={}".format(id_type, id_value)
            raise API_ERROR(1002, error)
        return data


    async def _host_check_exist_uuid(self, uuid):
        '''
        Check if provided UUID already exists in database. If not then None is returned or if it does then True is returned
        :param uuid: UUID value to be searched in database table
        :return: Return True if UUID exists and if not then it returns None
        '''
        try:
            # Get uuid for the user based on given id
            query = "select * from host_ids where uuid = '{}'".format(uuid)
            data = await self.db_host.fetchone(query)
            if not data:
                return False
            return True
        except:
            return False


    async def _cetp_identity_check_exist_uuid(self, uuid):
        '''
        Check if provided UUID already exists in database. If not then None is returned or if it does then True is returned
        :param uuid: UUID value to be searched in database table
        :return: Return True if UUID exists and if not then it returns None
        '''
        try:
            # Get uuid for the user based on given id
            query = "select * from host_policy_identity where uuid = '{}'".format(uuid)
            data = await self.db_host.fetchone(query)
            if not data:
                return False
            return True
        except:
            return False

    async def _ces_identity_check_exist_uuid(self, uuid):
        '''
        Check if provided UUID already exists in database. If not then None is returned or if it does then True is returned
        :param uuid: UUID value to be searched in database table
        :return: Return True if UUID exists and if not then it returns None
        '''
        try:
            # Get uuid for the user based on given id
            query = "select * from ces_policy_identity where uuid = '{}'".format(uuid)
            data = await self.db_host.fetchone(query)
            if not data:
                return False
            return True
        except:
            return False

    ############################################################
    ############################################################
    ############################################################
    # Get Functions

    def _firewall_policy_sql_query_get(self, kwargs):
        '''
        Create SQL query according to the provided parameters or exclude them from statement
        :param kwargs: id_type, id_value, policy_name
        :return: SQL query
        '''
        kwargs = Validator.firewall_get_policies(**kwargs)
        query = "select id, types,sub_type,policy_element from firewall_policies where uuid=(select uuid from host_ids where {}='{}'){}".\
            format(kwargs['id_type'], kwargs['id_value'], kwargs['policy_name'])
        return query


    def _host_policy_get(self, table_name,query_parameters, id_instance):
        '''
        Create SQL statement to retrieve all policies from TABLENAME or only one row if ID is provided
        :param table_name: Mapped to actual table name using dictionary, Values= ID, FIREWALL_POLICIES, CETP_POLICY_IDENTITY, CETP_POLICIES
        :param id_instance: Optional parameter if only one instance needs to be retrieved from database
        :return: SQL statement
        '''
        p=''
        if id_instance or query_parameters:
            p = ' where'
            if id_instance:
                p += ' id={} and'.format(id_instance)
            for key in query_parameters:
                p += " {}='{}' and".format(key, query_parameters[key])
        return "select * from {}{}".format(table_mapping[table_name],p[:-4])


    def _cetp_sql_query_get(self, kwargs):
        '''
        Create SQL query according to the provided parameters or exclude them from statement
        :param kwargs: local_fqdn, remote_fqdn, direction, policy_name
        :return: SQL query
        '''
        kwargs = Validator.cetp_get_policies(**kwargs)
        query = "select types,policy_element from host_policies where uuid=(select uuid from host_policy_identity where local_fqdn='{}'{}{}){}".\
            format(kwargs['local_fqdn'], kwargs['remote_fqdn'], kwargs['direction'], kwargs['policy_name'])
        return query

    def _ces_sql_query_get(self, kwargs):
        '''
        Create SQL query according to the provided parameters or exclude them from statement
        :param kwargs: host_ces_id and protocol
        :return: SQL query
        '''
        kwargs = Validator.ces_get_policies(**kwargs)
        query = "select types,policy_element from ces_policies where uuid=(select uuid from ces_policy_identity where host_ces_id={} and protocol={})".\
            format(kwargs['host_ces_id'], kwargs['protocol'])
        return query


    ############################################################
    ############################################################
    ############################################################
    # Insert Functions

    async def _host_policy_insert_id(self, data):
        '''
        create sql statement to insert in host_ids according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, msisdn, ipv4
        :return: sql insert statement or raise exception in case of validation error
        '''
        parameters=''
        for kwargs in data:
            kwargs = Validator._ids_validator(kwargs)
            while (True):
                unique_id= uuid.uuid1().int >> 64
                exists_check = await self._host_check_exist_uuid(unique_id)
                if not exists_check:
                    break
            parameters += "('{}',{},{},{},{}),".format(unique_id, kwargs['fqdn'], kwargs['msisdn'], kwargs['ipv4'], kwargs['username'])
        return "insert into host_ids (uuid, fqdn, msisdn, ipv4, username) values " + parameters[:-1]


    def _host_policy_insert_firewall(self, data):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        parameters = ''
        for policy in data:
            #await self._host_check_exist_user(policy['fqdn'])
            policy = Validator._firewall_policy_validator_filter(policy)
            parameters += "((select uuid from host_ids where fqdn={}),{},{},{}),".format(
            policy['fqdn'], policy['types'], policy['sub_type'], policy['policy_element'])
        return "insert into firewall_policies (uuid, types, sub_type, policy_element) values " + parameters[:-1]


    async def _host_policy_insert_cetp_policy_identity(self, data):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        parameters = ''
        for policy in data:
            while (True):
                unique_id= uuid.uuid1().int >> 64
                exists_check = await self._cetp_identity_check_exist_uuid(unique_id)
                if not exists_check:
                    break
            policy = Validator._cetp_policy_identity_validator(policy)
            parameters += "({},{},{},{},'{}'),".format(policy['local_fqdn'], policy['remote_fqdn'], policy['reputation'],
                                                     policy['direction'], unique_id)
        return "insert into host_policy_identity (local_fqdn, remote_fqdn, reputation, direction, uuid) values " + parameters[:-1]


    async def _host_policy_insert_cetp_policies(self, data):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        parameters = ''
        for policy in data:
            exists_check = await self._cetp_identity_check_exist_uuid(policy['uuid'])
            if not exists_check:
                raise API_ERROR(1005, 'Unique ID does not exists = {}'.format(policy['uuid']))
            policy = Validator._cetp_policies_validator(policy)
            parameters += "({},{},{}),".format(policy['uuid'], policy['types'], policy['policy_element'])
        return "insert into host_policies (uuid, types, policy_element) values " + parameters[:-1]


    async def _host_policy_insert_ces_policy_identity(self, data):
        '''
        create sql statement to insert in ces_policy_identity table according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => protocol, host_ces_id
        :return:sql insert statement or raise exception in case of validation error
        '''
        parameters = ''
        for policy in data:
            while (True):
                unique_id= uuid.uuid1().int >> 64
                exists_check = await self._ces_identity_check_exist_uuid(unique_id)
                if not exists_check:
                    break
            policy = Validator._ces_policy_identity_validator(policy)
            parameters += "({},{},'{}'),".format(policy['host_ces_id'], policy['protocol'], unique_id)
        return "insert into ces_policy_identity (host_ces_id, protocol, uuid) values " + parameters[:-1]


    async def _host_policy_insert_ces_policies(self, data):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        parameters = ''
        for policy in data:
            exists_check = await self._ces_identity_check_exist_uuid(policy['uuid'])
            if not exists_check:
                raise API_ERROR(1005, 'Unique ID does not exists = {}'.format(policy['uuid']))
            policy = Validator._cetp_policies_validator(policy)
            parameters += "({},{},{}),".format(policy['uuid'], policy['types'], policy['policy_element'])
        return "insert into ces_policies (uuid, types, policy_element) values " + parameters[:-1]

    def _insert_bootstrap(self, data):
        '''
        create sql statement to insert in bootstrap table according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => name, types, subtype, data
        :return: sql insert statement or raise exception in case of validation error
        '''
        parameters=''
        for kwargs in data:
            kwargs = Validator._bootstrap_validator(kwargs)
            parameters += '({}, {}, {}, {}),'.format(kwargs['name'], kwargs['types'], kwargs['sub_type'], kwargs['data'])
        return "insert into bootstrap (name, types, subtype, data) values " + parameters[:-1]


    ############################################################
    ############################################################
    ############################################################
    # update Functions

    def _host_policy_update_id(self, data, id):
        '''
        create sql statement to insert in host_ids according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, msisdn, ipv4
        :return: sql insert statement or raise exception in case of validation error
        '''
        #if 'id' not in kwargs or not kwargs['id'].isdigit():
        #    raise API_ERROR(1005, 'Only Accepted parameter for ID is integer. ID received = {}'.format(kwargs['id']))
        data = Validator._ids_validator(data)
        return "update host_ids set fqdn={}, msisdn={}, ipv4={}, username={} where id={}".format(data['fqdn'], data['msisdn'], data['ipv4'], data['username'], id)


    def _host_policy_update_firewall(self, data, id):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        #await self._host_check_exist_user(policy['fqdn'])
        data = Validator._firewall_policy_validator_filter(data)
        return "update firewall_policies set uuid=(select uuid from host_ids where fqdn={}),types={}, sub_type={}," \
               "policy_element={} where id={}".format(data['fqdn'],data['types'],data['sub_type'], data['policy_element'], id)


    def _host_policy_update_cetp_policy_identity(self, data, id):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        data = Validator._cetp_policy_identity_validator(data)
        return "update host_policy_identity set local_fqdn={}, remote_fqdn={}, reputation={}, direction={} where " \
               "id={}".format(data['local_fqdn'], data['remote_fqdn'], data['reputation'],data['direction'], id)


    def _host_policy_update_cetp_policies(self, data, id):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        data = Validator._cetp_policies_validator(data)
        return "update host_policies set uuid={},types={}, policy_element={} where id={}".format(data['uuid'], data['types'], data['policy_element'], id)


    def _host_policy_update_ces_policy_identity(self, data, id):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        data = Validator._ces_policy_identity_validator(data)
        return "update ces_policy_identity set host_ces_id={}, protocol={} where id={}".format(data['host_ces_id'], data['protocol'], id)


    def _host_policy_update_ces_policies(self, data, id):
        '''
        create sql statement to insert in host_firewall according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => fqdn, types, active, priority, direction, src, dst, sport, dport, protocol, target, comment, raw_data, schedule_start, schedule_end
        :return:sql insert statement or raise exception in case of validation error
        '''
        data = Validator._cetp_policies_validator(data)
        return "update ces_policies set types={}, policy_element={} where id={}".format(data['types'], data['policy_element'], id)


    def _update_bootstrap(self, data, id_instance):
        '''
        create sql statement to edit in bootstrap table according to given parameters. Also calls relevant validation function for fields
        :param kwargs:Dictionary of parameters => name, types, subtype, data
        :return: sql update statement or raise exception in case of validation error
        '''
        kwargs = Validator._bootstrap_validator(data)
        return "update bootstrap set name={}, types={}, subtype={}, data={} where id={}".format(kwargs['name'],kwargs['types'],kwargs['sub_type'],kwargs['data'], id_instance)


    ############################################################
    ############################################################
    ############################################################
    # Formatting Functions

    def formatting_get_firewall_policies(self, policies, ids):
        '''
        Conver policies to the acceptable format for CES Node
        :param policies: It is tuple of tuple retrieved from database
        :param ids: It is tuple of ids of user
        :return: Need to make it json
        Sample:
        (('GROUP', '', 'IPS_GROUP_POSTPAID'), ('CIRCULARPOOL', '', '{"max": "100" }'), ('CARRIERGRADE', '', '{"ipv4": "192.168.0.10"}'), ('SFQDN', '', '{"fqdn":"nest0.gwa.demo.",  "proxy_required":false, "carriergrade": true}'), ('FIREWALL', 'FIREWALL_ADMIN', '{"priority": 0,   "direction": "EGRESS", "protocol": "17", "udp":{"dport": "53"}, "target": "REJECT", "hashlimit": {"hashlimit-above":"5/sec", "hashlimit-burst":"50", "hashlimit-name":"DnsLanHosts", "hashlimit-mode":"srcip", "hashlimit-htable-expire":"1001"}, "comment":{"comment":"Host DNS limit"}}'), ('FIREWALL', 'FIREWALL_USER', '{"priority": 100, "direction": "INGRESS","target": "ACCEPT", "comment":{"comment":"Allow incoming"}}'))
        '''
        result={}
        result['ID']={}
        result['ID']['fqdn']=ids[1]
        result['ID']['msisdn'] = ids[2]
        result['ID']['ipv4'] = ids[3]
        for p in policies:
            try:
                if p[1]=='FIREWALL':
                    try:
                        result['FIREWALL'][p[2]].append(json.loads(p[3]))
                    except:
                        if 'FIREWALL' not in result:
                            result['FIREWALL']={}
                        result['FIREWALL'][p[2]]=[]
                        result['FIREWALL'][p[2]].append(json.loads(p[3]))
                else:
                    result[p[1]].append(json.loads(p[3]))
            except:
                result[p[1]]=[]
                try:
                    result[p[1]].append(json.loads(p[3]))
                except:
                    result[p[1]].append(p[3])
        return result


    def formatting_get_cetp_policies(self, policies):
        result={}
        for p in policies:
            try:
                result[p[0]].append(json.loads(p[1]))
            except:
                result[p[0]]=[]
                result[p[0]].append(json.loads(p[1]))
        return result


    def _host_bootstrap_postprocess(self, data):
        '''
        Format bootstrap policies in order they are required.
        :param data: tuple or list
        :return: Formatted data
        id, name, types, subtype, data
        '''
        result = {}
        for d in data:
            while (True):
                if d[1] in result:
                    if d[2] in result[d[1]]:
                        if d[3] in result[d[1]][d[2]]:
                            result[d[1]][d[2]][d[3]].append(json.loads(d[4].replace("'", '"')))
                            break
                        else:
                            result[d[1]][d[2]][d[3]] = []
                    else:
                        result[d[1]][d[2]] = {}
                else:
                    result[d[1]] = {}
        return result



    ############################################################
    ############################################################
    ############################################################
    # Delete SQL statements


    def _host_policy_delete(self, table_name, parameter=None):
        '''
        create sql statement to delete policy from tables.
        :param table_name: Table name from which it is required to delete the policy
        :param parameter:it contains the value = 'where id = 5' id can be integer or tuple to delete multiple policies or empty to delete all policies
        :return:sql statement
        '''
        if not parameter:
            parameter=''
        return "delete from {} {}".format(table_name, parameter)



    def _delete_bootstrap(self, parameter=None):
        '''
        create sql statement to delete policy from bootstrap.
        :param parameter:it contains the value = 'where id = 5' id can be integer or tuple to delete multiple policies or empty to delete all policies
        :return:sql statement
        '''
        if not parameter:
            parameter=''
        return "delete from bootstrap {}".format(parameter)

    ############################################################
    ############################################################
    ############################################################
    # Policy Retrieval By CES

    async def firewall_policy_user_get(self, id_type, id_value, policy_name=None, format=False):
        '''
        Return specific user policy or all of them
        :param id_type: FQDN or MSISDN or other id types
        :param id_value: something@aalto.fi or +358441414141
        :param policy_name: All or FIREWAL,CARRIERGRADE,CIRCULARPOOL,ID,GROUP or SFQDN
        :return:
        '''

        # Get uuid for the host as key to other tables and to check if the user exists with the credentials
        # retrieves = uuid,fqdn,msisdn,ipv4
        host_ids = await self._host_get_user_ids(id_type, id_value)

        if policy_name and str(policy_name) not in ['ID', 'GROUP', 'CARRIERGRADE', 'CIRCULARPOOL', 'SFQDN', 'FIREWALL']:
            error = "Policy Name not supported = {}".format(policy_name)
            raise API_ERROR(1001, error)
        kwargs = locals()
        # Calling function to create SQL query to retrieve Policies. Then executing that query in SQL-Client and formatting returned policies
        query = self._firewall_policy_sql_query_get(kwargs)
        #print (query)
        result = await self.db_host.fetchall(query)
        if not format:
            result = self.formatting_get_firewall_policies(result,host_ids)
        return result


    async def host_cetp_policy_get(self, local_fqdn, remote_fqdn, direction, policy_name):
        '''
        Retrieving Host policies of a user
        :param local_fqdn: Local Fqdn (Value is compulsory)
        :param remote_fqdn: Remote FQDN (Optional Parameter)
        :param direction: EGRESS or INGRESS (Optional Parameter)
        :param policy_name: Available or Request or Offer or None. In case of None all parameters are considered(Optional Parameter)
        :return: Formatted Policies
        '''
        if not direction or not local_fqdn:
            raise API_ERROR(1001, 'Local FQDN and Direction are compulsory parameters for CETP policy Retrieval')
        kwargs=locals()
        query= self._cetp_sql_query_get(kwargs)
        #print (query)
        data = await self.db_host.fetchall(query)
        result = self.formatting_get_cetp_policies(data)
        return result


    async def ces_policy_get(self, ces_id, protocol):
        '''
        Retrieving Host policies of a user
        :param local_fqdn: Local Fqdn (Value is compulsory)
        :param remote_fqdn: Remote FQDN (Optional Parameter)
        :param direction: EGRESS or INGRESS (Optional Parameter)
        :param policy_name: Available or Request or Offer or None. In case of None all parameters are considered(Optional Parameter)
        :return: Formatted Policies
        '''
        if not ces_id or not protocol:
            raise API_ERROR(1001, 'CES ID and Protocol are compulsory parameters for CES policy Retrieval')
        kwargs=locals()
        query= self._ces_sql_query_get(kwargs)
        #print(query)
        data = await self.db_host.fetchall(query)
        result = self.formatting_get_cetp_policies(data)
        return result


    def _bootstrap_get(self, query=None):
        """ Return MySQL statement to retrieve bootstrap policies """
        return "select id, name, types, subtype, data from bootstrap {}".format(query)


    ############################################################
    ############################################################
    ############################################################
    # Policy Retrieval for Management Purpose


    async def host_policy_get(self, table_name, query_parameters, id_instance=None):
        """ Return a list of All policies in one table or return specific row of one table if ID is provided """
        if not table_name or str(table_name) not in ['CES_POLICIES', 'CES_POLICY_IDENTITY', 'HOST_POLICIES', 'HOST_POLICY_IDENTITY', 'FIREWALL', 'ID']:
            error = "Table Type not supported = {}".format(table_name)
            raise API_ERROR(1001, error)
        query = self._host_policy_get(table_name, query_parameters, id_instance)
        #print (query)
        data = await self.db_host.fetchall(query)
        data=[list(x) for x in data]
        for i in range (0,len(data)):
            for j in range (0,len(data[i])):
                if type(data[i][j]) is bytes:
                    data[i][j] = ord(data[i][j])
        return data



    async def host_policy_insert(self, table_name, data):
        """ Insert User Policy in table or return exception in case of validation error or other errors """
        # Check if table name is provided under label of policy_name
        if str(table_name) not in ['CES_POLICIES', 'CES_POLICY_IDENTITY', 'HOST_POLICIES', 'HOST_POLICY_IDENTITY', 'FIREWALL', 'ID']:
            error = "Table Type not supported = {}".format(table_name)
            raise API_ERROR(1001, error)

        get_function = self._host_policy_functions[table_name]['insert']
        if table_name == 'FIREWALL':
            query = get_function(data)
        else:
            query = await get_function(data)
        #print (query)
        data = await self.db_host.execute(query)
        #await self._update_timestamp(data['fqdn'], policy_name.upper())
        return data




    async def host_policy_update(self, table_name, data, id_instance):
        """ Insert User Policy in table or return exception in case of validation error or other errors """
        # Check if table name is provided under label of policy_name
        if str(table_name) not in ['CES_POLICIES', 'CES_POLICY_IDENTITY', 'HOST_POLICIES', 'HOST_POLICY_IDENTITY', 'FIREWALL', 'ID']:
            error = "Table Type not supported = {}".format(table_name)
            raise API_ERROR(1001, error)

        get_function = self._host_policy_functions[table_name]['update']
        query = get_function(data, id_instance)
        #print (query)
        data = await self.db_host.execute(query)
        #await self._update_timestamp(data['fqdn'], policy_name.upper())
        return data



    ############################################################
    ############################################################
    ############################################################
    # Bootstrap Policy Functions


    async def bootstrap_get_policies_ces(self, policy_type):
        # Fetch the bootstrap policies and format them to use for CES

        # Use dictionary for returning policies
        result_d = {}

        # Get all policies
        if policy_type and policy_type.upper() not in ['IPSET', 'IPTABLES', 'CIRCULARPOOL']:
            raise API_ERROR(1001, 'Incorrect Policy Type. Only accepted valued are IPSET, IPTABLES and CIRCULARPOOL. Provided = {}'.format(policy_type))
        # Get policies included in the iterable

        # Obtain SQL statement for execution
        if policy_type:
            query = self._bootstrap_get("where name='{}'".format(policy_type))
        else:
            query = self._bootstrap_get()
        #print(query)
        data = await self.db_bootstrap.fetchall(query)
        processed_data = self._host_bootstrap_postprocess(data)
        # Add process data to results
        result_d.update(processed_data)
        return result_d



    async def bootstrap_get_policies(self, policy_type, id=None):
        # Fetch the bootstrap policies
        if id:
            query = self._bootstrap_get("where id={}".format(id))
        elif policy_type:
            if policy_type and policy_type.upper() not in ['IPSET', 'IPTABLES', 'CIRCULARPOOL']:
                raise API_ERROR(1001,'Incorrect Policy Type. Only accepted valued are IPSET, IPTABLES and CIRCULARPOOL. Provided = {}'.format(policy_type))
            query = self._bootstrap_get("where name='{}'".format(policy_type))
        else:
            #print('*******2222****')
            query = self._bootstrap_get(' ')
        #print(query)
        data = await self.db_bootstrap.fetchall(query)
        return data


    async def bootstrap_insert(self, data):
        """ Insert Policy in bootstrap table or return exception in case of validation error or other errors """

        statement = self._insert_bootstrap(data)
        data = await self.db_bootstrap.execute(statement)
        return data


    async def bootstrap_update(self, data, id_instance):
        """ edit Policy in bootstrap table or return exception in case of validation error or other errors """

        statement = self._update_bootstrap(data, id_instance)
        data = await self.db_bootstrap.execute(statement)
        return data


    ############################################################
    ############################################################
    ############################################################
    # Delete Policies from Host Policies database


    async def policy_delete(self, policy_name, query_parameters, id_instance=None):
        """ Insert User Policy in table or return exception in case of validation error or other errors """

        # Check if table name is provided under label of policy_name
        if str(policy_name) not in ['CES_POLICIES', 'CES_POLICY_IDENTITY', 'HOST_POLICIES', 'HOST_POLICY_IDENTITY', 'FIREWALL', 'ID']:
            error = "Table Type not supported = {}".format(policy_name)
            raise API_ERROR(1001, error)
        parameters = ''
        if id_instance:
            if type(id_instance) is list or type(id_instance) is tuple:
                parameters="where id in {}".format(tuple(id_instance))
            elif type(id_instance) is str or type(id_instance) is int:
                parameters="where id = {}".format(int(id_instance))
            else:
                error = "ID = {} or Query Parameters = {} not support.".format(policy_name, query_parameters)
                raise API_ERROR(1001, error)
        elif query_parameters:
            parameters = ' where'
            for key in query_parameters:
                parameters += " {}='{}' and".format(key, query_parameters[key])
            parameters = parameters[:-4]
        query = self._host_policy_delete(table_mapping[policy_name], parameters)
        #print (query)
        data = await self.db_host.execute(query)
        return data



    async def host_bootstrap_delete(self, id=None):
        """ Delete single or multiple policies or complete table or return exception in case of validation error or other errors """
        if id:
            if type(id) is list or type(id) is tuple:
                id="where id in {}".format(tuple(id))
            elif type(id) is str or type(id) is int:
                id="where id = {}".format(int(id))
            else:
                error = "ID = {} not support.".format(id)
                raise API_ERROR(1001, error)
            query = self._delete_bootstrap(id)
        else:
            query = self._delete_bootstrap()
        #print (query)
        data = await self.db_bootstrap.execute(query)
        return data



    ############################################################
    ############################################################
    ############################################################
    # Extra Functionalities


    async def host_column_names(self, tablename):
        '''
        Get the column names of table for GUI
        :param database :database to retrieve tables from
        :param tablename:table name for which columns are required
        :return: Column names or raise an error incase of exception
        '''
        if str(tablename) not in ['CES_POLICIES', 'CES_POLICY_IDENTITY', 'HOST_POLICIES', 'HOST_POLICY_IDENTITY', 'FIREWALL', 'ID']:
            error = "Table Type not supported = {}".format(tablename)
            raise API_ERROR(1001, error)
        statement = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = n'{}'".format(table_mapping[tablename])
        data = await self.db_host.fetchall(statement)
        return data


    async def user_registration(self, username, password, ip_address, ttl):
        #Get uuid for the user based on given id
        fqdn = self.fqdn_formation(ip_address, soa)
        message = self.ddns_update(fqdn, soa, ip_address, ttl)
        dns_socket = await self.dns_connection()
        '''Need to send update message to Server here'''
        dns_socket.sendto(message.to_wire(), dns_address)
        dns_socket.recv(1024)
        #query = "update host_ids set ipv4='{}' where fqdn='{}'".format(ip,fqdn)
        #data = await self.db_host.execute(query)
        return 'nothing'


    def ddns_update(self, fqdn, soa, ipaddr, ttl):
        #print('Message sent to DNS = IP Address :', ipaddr, ' and FQDN:', fqdn)
        msg = dns.message.Message()
        msg.set_opcode(dns.opcode.UPDATE)
        msg.set_rcode(dns.rcode.NOERROR)
        # Zone
        rrset = dns.rrset.from_text(soa, ttl, dns.rdataclass.IN, dns.rdatatype.SOA)
        msg.question.append(rrset)
        # Record
        rrset = dns.rrset.from_text(fqdn, ttl, dns.rdataclass.IN, dns.rdatatype.A, ipaddr)
        msg.authority.append(rrset)
        return msg


    def fqdn_formation(self, ip_address, soa):
        ip_address=ip_address.replace('.','_')
        fqdn = ip_address + '.' + str(soa)
        return fqdn
