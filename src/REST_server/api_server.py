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

import ssl

from aiohttp import web
import json,asyncio
import pymysql, logging

from CES_API_DB import CesApiDatabase
from errorsfile import API_ERROR




logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

error_codes = {1001 : "Query Parameters not supported",
               1002 : "No record found",
               1003 : "Missing Information for query",
               1004 : "Statement Execution Error",
               1005 : "Data Validation Error",
               1006 : "Query Parameters Format not correct",
               1007 : "Forbidden Character found in Parameters",
               1010 : "User Does not exists"}

# HTTP codes. For now just assumed
http_codes =  {1001 : 601,      #"Query Parameters not supported",
               1002 : 602 ,     #"No record found",
               1003 : 603,      #"Missing Information for query",
               1004 : 604,      #"Statement Execution Error",
               1005 : 605,      #"Data Validation Error",
               1006 : 606,      #"Query Parameters Format not correct"}
               1007 : 607,      #"Query Parameters Format not correct"}
               1008 : 608,      #"Duplication Error"}
               1009 : 609,      #"Data Validation Error in Database",
               1010 : 610}      # User does not exists

class CES_API:

    #Connectiong to the database
    async def connect(self):
        self.api_db = CesApiDatabase()
        await self.api_db.connect()


    def encoding_data(self, data):
        try:
            Data = json.dumps(data)
        except Exception as e:
            Data = json.dumps(str(e) + ' --- Error Occured while json dumps for data --- ' + str(data))
        Data = Data.encode('utf-8')
        return Data


    def exception_handler(self,e):
        try:
            print ('\n\n\n' , type(e), e.code, '\n\n\n')
        except:
            print ('\n\n\n' , e, '\n\n\n')
        logger.warning('Exception Occured Printing Exception ={}\n'.format(str(e)))
        if type(e) is pymysql.err.ProgrammingError:
            http_code = e.args[0]
            http_reason = e.args[1]
        elif type(e) is pymysql.err.InternalError:
            #(1054, "Unknown column 'a' in 'where clause'")
            http_code = 500
            http_reason = e.args[1]
        elif type(e) is pymysql.err.IntegrityError:
            #(1062, "Duplicate entry 'test1.aalto.fi' for key 'PRIMARY'")
            http_code = 515#e.args[0]
            http_reason = e.args[1]
        elif type(e) is AttributeError:
            #AttributeError: 'CesApiDatabase' object has no attribute '_host_policy_functions'
            http_code = 515  # e.args[0]
            http_reason = e.args[0]
        elif type(e) is NameError:
            #NameError: name '_host_policy_functions' is not defined
            #(1048, "Column 'uuid' cannot be null")
            http_code = 515  # e.args[0]
            http_reason = e.args[0]
        elif type(e) is TypeError:
            #TypeError: argument of type 'coroutine' is not iterable
            http_code = 515  # e.args[0]
            http_reason = e.args[0]
        elif type(e) is KeyError:
            #TypeError: argument of type 'coroutine' is not iterable
            http_code = 515  # e.args[0]
            http_reason = 'The necessary element was missing in query - {}'.format(e.args[0])
        elif type(e) is UnboundLocalError:
            #UnboundLocalError: local variable 'p' referenced before assignment
            http_code = 515  # e.args[0]
            http_reason = 'Following error Occured - {}'.format(e)
        elif e.code:
            if e.code==1001:
                #Table Type not supported = {}
                http_reason = e.message
                http_code=http_codes[e.code]
            elif e.code == 1002:
                #No user found for id_type={} and id_value={}"
                http_reason = e.message
                http_code = http_codes[e.code]
            elif e.code==1003:
                http_reason = 'Missing data while inserting policy : Missing Parameter = ' + repr(e.message)
                http_code=http_codes[e.code]
            elif e.code == 1005:
                #a is not an integer
                #Only accepted data format is list of dict
                http_reason = 'Missing data while inserting policy : Missing Parameter = ' + repr(e.message)
                http_code = http_codes[e.code]
            elif e.code==1007:
                http_reason = e.message
                http_code=http_codes[e.code]
            elif e.code==1009:
                http_reason = 'Field Validation Error in DB Occured while inserting policy : ' + repr(e.message)
                http_code=http_codes[e.code]
            elif e.code == 1146:
                http_reason = e.message
                http_code = http_codes[e.code]
            else:
                raise (e)
        else:
            logger.error('Error Occured' + str(e))
            raise e
        return http_code,http_reason


    async def response_creater(self, request, http_code, reason, data, caller):
        data = json.dumps(data).encode('utf-8')
        resp = web.StreamResponse(status=http_code, reason=reason, headers={'Content-Type': 'application/json'})
        await resp.prepare(request)
        resp.write(data)
        if caller==True:
            logger.info('\nReturned Data: {}'.format(data))
            pass
        else:
            logger.info('Error Occured. Details = {}{}'.format(http_code, data))
            pass
        return resp


    def fetch_parameters(self, request):
        '''
        Function to fetch parameters from query so that database data can be fintered on the base of provided parameters
        :param request: request (http object from aiohttp)
        :return: returning dictionary of all not null parameters
        '''
        parameters = {}
        parameters['uuid'] = request.GET.get('uuid')
        parameters['types'] = request.GET.get('types')
        parameters['sub_type'] = request.GET.get('sub_type')
        parameters['policy_element'] = request.GET.get('policy_element')
        parameters['host_ces_id'] = request.GET.get('host_ces_id')
        parameters['protocol'] = request.GET.get('protocol')
        parameters['local_fqdn'] = request.GET.get('local_fqdn')
        parameters['remote_fqdn'] = request.GET.get('remote_fqdn')
        parameters['direction'] = request.GET.get('direction')
        parameters['fqdn'] = request.GET.get('fqdn')
        parameters['msisdn'] = request.GET.get('msisdn')
        parameters['ipv4'] = request.GET.get('ipv4')
        parameters['username'] = request.GET.get('username')
        final_parameters = {k: v for k, v in parameters.items() if v is not None}
        return final_parameters


    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################


    async def get_firewall_policies_user(self, request):
        '''
        Sample URL = http://127.0.0.1/API/firewall_policy_user/FQDN/test101.gwa.demo.?policy_name="Something"
        Retrieves user policies of a particular user. Retrieves particular policy of a user or all policies of a user using any id parameter
        :param request: ID_TYPE (Compulsory) can be FQDN, USERNAME etc.
                    ID_VALUE (Compulsory) is value of FQDN or Username.
                    Policy_Name (Optional) is the type of policy to be retrieved. All policies are retrieved if this parameter is not provided
                    FORMAT (Optional) should be set false if policies needs to be retrieved without formatting.
        :return: Policies or Error if occured
        '''
        id_type = request.match_info.get('id_type')
        id_value = request.match_info.get('id_value')
        policy_name = request.GET.get('policy_name')
        format = request.GET.get('format')
        logger.info('\n\n------1------------------------------------------\nInput Parameters: \n ID_Type = {}\n ID_Value = {} \n Policy_Name = {}\n Format = {}\n'.format(id_type, id_value, policy_name, format))

        try:
            if policy_name:
                policy_name=policy_name.upper()
            data = await self.api_db.firewall_policy_user_get(id_type.lower(), id_value, policy_name, format)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def get_firewall_policies_table_instance(self, request):
        '''
        Sample URL = http://127.0.0.1/API/firewall_policy/{table_name}/{id}
        Retrieves single row from a table
        :param request: Table_Name (Compulsory) is the name of table from which policy needs to be retrieved
                        ID (Compulsory) is the id of a row in database table
                        Query Parameter can include any column based filtering and can filter the data based on the parameters provided
        :return: Policy Instance or Error if occured
        '''
        table_name = request.match_info.get('table_name')
        query_parameters = self.fetch_parameters(request)

        id_instance = request.match_info.get('id')
        logger.info('------2------------------------------------------\nInput Parameters: \n Policy_Table_name = {}\nQuery Parameters = {}\nID = {}\n'.format(table_name, query_parameters, id_instance))

        try:
            data = await self.api_db.host_policy_get(table_name.upper(), query_parameters, id_instance)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def get_firewall_policies_table(self, request):
        '''
        Sample URL = http://127.0.0.1/API/firewall_policy/{table_name}
        Retrieves all policies from a table or particular type of policy from a table
        :param request: Table_Name (Compulsory) is the name of table from which policy needs to be retrieved
                    Policy_Type (Optional) is the type of policy that needs to be retrieved from a table. If not provided
                                then all policies in a table are retrieved.
                    Query Parameter can include any column based filtering and can filter the data based on the parameters provided
        :return: Policy Instance or Error if occured
        '''
        table_name = request.match_info.get('table_name')
        query_parameters = self.fetch_parameters(request)
        logger.info('\n\n------3------------------------------------------\nInput Parameters: \n Policy_Table_name = {}\nQuery Parameters = {}\n'.format(table_name,query_parameters))

        try:
            data = await self.api_db.host_policy_get(table_name.upper(), query_parameters)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def insert_firewall_policies(self, request):
        '''
        Sample URL = http://127.0.0.1/API/firewall_policy/{table_name}
        Insert policy or list of policies in one table  per request.
        :param request: Table_Name (Compulsory) is the table in which policies needs to be inserted
                        Data received is in payload and the type of data must be list of dict
        :return: Null (200 OK) or Error if occured
        '''
        table_name = request.match_info.get('table_name')
        data_received = await request.read()
        data_received = json.loads(data_received.decode("utf-8"))
        logger.info('\n\n------4------------------------------------------\nInput Parameters: \n Policy_Table_name = {}\n Data Received = {}'.format(table_name, data_received))

        try:
            if type(data_received) is not list or type(data_received[0]) is not dict:
                raise API_ERROR(1005, 'Only accepted data format is list of dict')
            data = await self.api_db.host_policy_insert(table_name.upper(), data_received)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def update_firewall_policies(self, request):
        '''
        Sample URL = http://127.0.0.1/API/firewall_policy/{table_name}/{id}
        Update single policy per request because in update, ID of policy is used to edit entry in database
        :param request: Table_Name (Compulsory) is the table in which policy needs to be updated
                        ID (Compulsory) is the id of policy that needs to be updated
                        Data received is in payload and the type of data must be dict
        :return: Null (200 OK) or Error if occured
        '''
        table_name = request.match_info.get('table_name')
        id_instance = request.match_info.get('id')
        data_received = await request.read()
        data_received = json.loads(data_received.decode("utf-8"))
        logger.info('\n\n------5------------------------------------------\nInput PUT Parameters: \n Policy_Table_name = {}\n Data Received = {}\n ID = {}'.format(table_name, data_received, id_instance))

        try:
            #if type(data_received) is not list or type(data_received[0]) is not dict:
            #    raise API_ERROR(1005, 'Only accepted data format is list of dict')
            if not id_instance.isdigit() or type(data_received) is not dict:
                raise API_ERROR(1005, 'Only Accepted parameter for ID is integer. ID received = {}. and only accepted format '
                                      'is dict. Type received = {}'.format(id_instance,type(data_received)))
            data = await self.api_db.host_policy_update(table_name.upper(), data_received, id_instance)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp



    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################



    async def get_cetp_policies_node(self, request):
        '''
        Sample URL = http://127.0.0.1/API/cetp_policy_node?policy_name=something&lfqdn=something&rfqdn=something&direction=EGRESS
        Retrieve HOST CETP policies by CES in formatted form so that it can be used in CES
        :param request: Policy_name (optional) is used to retrieve particular type of policies (Available, Offer or Request)
                        lfqdn (optional) is the local fqdn of user whose policies needs to be retrieved. If not provided
                                then default policy would be retrieved
                        rfqdn (optional) is the remote fqdn of user whose policies needs to be retrieved. If not provided
                                then default policy would be retrieved
                        direction (optional) is the direction of policies needs to be retrieved. If not provided
                                then default policy would be retrieved
        :return: Policies or Error if occured
        '''
        policy_name = request.GET.get('policy_name')
        local_fqdn  = request.GET.get('lfqdn')
        remote_fqdn = request.GET.get('rfqdn')
        direction = request.GET.get('direction')
        logger.info('\n\n------6------------------------------------------\nInput PUT Parameters: \n Policy Name = {}\nLocal FQDN = {}\n Remote FQDN = {}\n Direction = {}'.format(policy_name, local_fqdn, remote_fqdn,direction))

        try:
            data = await self.api_db.host_cetp_policy_get(local_fqdn, remote_fqdn, direction, policy_name)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################



    async def get_ces_policies_node(self, request):
        '''
        Sample URL = http://127.0.0.1/API/ces_policy_node?ces_id=something&protocol=something&policy_name=something
        Retrieve CES CETP policies by CES in formatted form so that it can be used in CES
        :param request: Policy_name (optional) is used to retrieve particular type of policies (Available, Offer or Request)
                        ces_id (optional) is the host_ces_fqdn of ces whose policies needs to be retrieved. If not provided
                                then default policy would be retrieved
                        protocol (optional) is the type (tls, tcp etc) for which policies needs to be retrieved. If not provided
                                then default policy would be retrieved
        :return: Policies or Error if occured
        '''
        host_ces_id = request.GET.get('ces_id')
        protocol = request.GET.get('protocol')
        policy_name = request.GET.get('policy_name')
        logger.info('\n\n------7-----------------------------------------\nInput Parameters: \n Policy Name = {}\nCES ID = {}\n Trans_Protocol = {}\n'.format(policy_name,host_ces_id, protocol))

        try:
            data = await self.api_db.ces_policy_get(host_ces_id, protocol)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    ##################################################################################################
    ##################################################################################################
    ##################################################################################################


    async def get_bootstrap_policies_ces(self, request):
        '''
        Sample URL = http://127.0.0.1/API/bootstrap_policies_ces?policy_name=IPTABLES?
        Retrieve Bootstrap policies in formatted form so they can be executed at CES node
        :param request: Policy_name (optional) is used to retrieve particular type of policies (IPTABLES, IPSET etc)
        :return: Policies or Error if occured
        '''
        policy_name = request.GET.get('policy_name')
        logger.info('\n\n------8-----------------------------------------\nInput Parameters: \n Policy_Type = {}'.format(policy_name))

        try:
            data = await self.api_db.bootstrap_get_policies_ces(policy_name)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp



    async def get_bootstrap_policies_instance(self, request):
        '''
        Sample URL = http://127.0.0.1/API/bootstrap_policies/{id}
        Retrieve single row of bootstrap policy table
        :param request: ID (Compulsory) is the id of instance of policy in database table
        :return: Policies or Error if occured
        '''
        id_instance = request.match_info.get('id')
        policy_type = None
        logger.info('\n\n------9-----------------------------------------\nInput Parameters: \n ID = {}\n'.format(id_instance))

        try:
            data = await self.api_db.bootstrap_get_policies(policy_type, id_instance)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def get_bootstrap_policies(self, request):
        '''
        Sample URL = http://127.0.0.1/API/bootstrap_policies?policy_name=IPSET
        Retrieve all policies of bootstrap table or any particular type of policy without any formatting
        :param request: Policy_Name (optional) is type of policy that needs to be retrieved. If not provided then all policies are retrieved
        :return: Policies or Error if occured
        '''
        policy_type = request.GET.get('policy_name')
        logger.info('\n\n------10-----------------------------------------\nInput Parameters: \n Policy_Type = {}'.format(policy_type))

        try:
            if not policy_type:
                policy_type=''
            data = await self.api_db.bootstrap_get_policies(policy_type.upper())
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def insert_bootstrap_policies(self, request):
        '''
        Sample URL = http://127.0.0.1/API/bootstrap_policies
        Data = [{'name':'IPTABLES', 'type':'mREJECT', 'subtype':'requires', 'data':"{'table': 'mangle', 'chain': 'PREROUTING', 'create': false, 'flush': true}"}]
        Insert policies in bootstrap table
        :param request: Payload contains the data that needs to be inserted. Only accepted format is list of dict
        :return: Null (200 OK) or Error if occured
        '''
        data_received = await request.read()
        data_received = json.loads(data_received.decode("utf-8"))
        logger.info('\n\n------11-----------------------------------------\nInput Parameters: \n Data Received = {}'.format(data_received))

        try:
            if type(data_received) is not list or type(data_received[0]) is not dict:
                raise API_ERROR(1005, 'Only accepted data format is list of dict')
            data = await self.api_db.bootstrap_insert(data_received)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def update_bootstrap_policies(self, request):
        '''
        Sample URL = http://127.0.0.1/API/bootstrap_policies/3"
        Data = Data = {'name':'IPTABLES', 'type':'PACKET_MARKING', 'subtype':'requires', 'data':"{'table': 'mangle', 'chain': 'PREROUTING', 'create': false, 'flush': true}"}
        Update policies in bootstrap table
        :param request: ID (Compulsory) is the id of a policy instance in database table that needs to be updated
                        Payload contains the data that needs to be inserted. Only accepted format is dict
        :return: Null (200 OK) or Error if occured
        '''
        id_instance = request.match_info.get('id')
        data_received = await request.read()
        data_received = json.loads(data_received.decode("utf-8"))
        logger.info('\n\n------12-----------------------------------------\nInput Parameters: \n Data Received = {}\n ID = {}'.format(data_received, id_instance))

        try:
            if not id_instance.isdigit() or type(data_received) is not dict:
                raise API_ERROR(1005, 'Only Accepted parameter for ID is integer. ID received = {}. and only accepted format '
                                      'is dict. Type received = {}'.format(id_instance,type(data_received)))
            data = await self.api_db.bootstrap_update(data_received, id_instance)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    ##################################################################################################
    ##################################################################################################
    ##################################################################################################


    async def delete_policies(self, request):
        '''
        Sample URL = http://127.0.0.1/API/firewall_policy/{table_name}/{id}
        OR
        Sample URL = http://127.0.0.1/API/firewall_policy/{table_name}?parameters=value
        Delete policies from database (HOST_POLICIES) by ID or by query parameters
        :param request: Table_Name is the table from which policy needs to be deleted
                        ID is the id in database for any instance of policy which needs to be deleted
                        Query Parameter can include any column (of database table) based filtering and can filter the
                                data based on the parameters provided. All parameters are directly provided to SQL statement
        :return: Null (200 OK) or Error if occured
        '''
        table_name = request.match_info.get('table_name')
        id_instance = request.match_info.get('id')
        query_parameters = self.fetch_parameters(request)
        logger.info('\n\n------13-----------------------------------------\nInput Parameters: \n Policy_Table_name = {}\n ID = {}\n Query Parameters = {}'.format(table_name, id_instance, query_parameters))

        try:
            if id_instance:
                if not id_instance.isdigit() and all(item.isdigit() == True for item in id_instance.split(',')) != True:
                    raise API_ERROR(1005,'Only Accepted parameter for ID is integer or comma separated integers. '
                                         'ID received = {}'.format(id_instance))
                id_instance = id_instance if ',' not in id_instance else id_instance.split(',')
            data = await self.api_db.policy_delete(table_name.upper(), query_parameters, id_instance)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def delete_bootstrap_data(self, request):
        '''
        Sample URL = http://127.0.0.1/API/bootstrap_policies/{table_name}/{id}
        Delete policies from bootstrap table in ces_bootstrap database by ID
        :param request: ID is the id in database for any instance of policy which needs to be deleted
        :return: Null (200 OK) or Error if occured
        '''
        id_instance = request.match_info.get('id')
        logger.info('\n\n------14-----------------------------------------\nInput Parameters: \n ID = {}'.format(id_instance))

        try:
            if id_instance:
                if not id_instance.isdigit() and all(item.isdigit() == True for item in id_instance.split(',')) != True:
                    raise API_ERROR(1005,'Only Accepted parameter for ID is integer or comma separated integers. ID received = {}'.format(id_instance))
                id_instance = id_instance if ',' not in id_instance else id_instance.split(',')
            data = await self.api_db.host_bootstrap_delete(id_instance)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp

    """
    # http://127.0.0.1/API/delete_policy_cesapp/{id} or {ids}
    async def delete_policies_cesapp(self, request):
        id_instance = request.match_info.get('id')
        logger.info('\n\n------15-----------------------------------------\nInput Parameters: \n ID = {}'.format(id_instance))

        try:
            if not id_instance or not id_instance.isdigit() and all(item.isdigit() == True for item in id_instance.split(',')) != True:
                raise API_ERROR(1005, 'Only Accepted parameter for ID is integer or comma separated integers. ID received = {}'.format(id_instance))
            id_instance = id_instance if ',' not in id_instance else id_instance.split(',')
            data = await self.api_db.policy_delete_cesapp('HOST', 'FIREWALL', id_instance)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    # http://127.0.0.1/API/delete_policy_cesapp/all
    async def delete_policies_cesapp_all(self, request):
        logger.info('\n\n------16-----------------------------------------\nInput Parameters: \n Deleting all policies from Firewall table having CES ID'.format(id_instance))

        try:
            data = await self.api_db.policy_delete_cesapp('HOST', 'FIREWALL', None)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception  as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp

    """
    ##################################################################################################
    ##################################################################################################
    ##################################################################################################


    async def user_registration(self, request):
        '''
        Sample URL = http://127.0.0.1/API/user_registration/?username=something&ip=1.1.1.1&ttl=60
        User Registration from Captive Portal, sends a DDNS message to DNS server
        :param request: Username (compulsory) is needed to identify user
                        IP (Compulsory) is the ip address of the user that needs to be updated in DNS
        :return: Null (200 OK) or Error if occured
        '''
        username = request.GET.get('username')
        password = request.GET.get('password')
        ip = request.GET.get('ip')
        ttl = request.GET.get('ttl')
        logger.info('\n\n------17-----------------------------------------\nInput Parameters: \n Username = {}\n Password = {}\n IP = {}\n TTL = {}'.format(username, password, ip, ttl))

        try:
            data = await self.api_db.user_registration(username, password, ip, ttl)
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp


    async def host_retrieve_columns(self, request):
        '''
        Sample URL = http://127.0.0.1/API/tables_get_columns/{table_name}
        This function retrieves columns of a database table which is used in DJANGO application
        :param request: Table_name (compulsory) is the table for which columns needs to be retrieved
        :return: Column Details or Error if occured
        '''
        table_name = request.match_info.get('table_name')
        logger.info('\n\n------18-----------------------------------------\nInput Parameters: \n Table Name = {}'.format(table_name))

        try:
            data = await self.api_db.host_column_names(table_name.upper())
            resp = await self.response_creater(request, 200, 'OK', data, True)
        except Exception as e:
            http_code, error_reason = self.exception_handler(e)
            resp = await self.response_creater(request, http_code, None, error_reason, False)
        await resp.drain()
        return resp



    ##################################################################################################
    ##################################################################################################
    ##################################################################################################


#Routers to map specific urls with functions. Functions are called when the relevant URL is called by client
async def build_server(loop, address, port, sslcontext):
    app = web.Application(loop=loop)
    object = CES_API()
    await object.connect()


    ########################################
    ########################################


    # http://127.0.0.1/API/firewall_policy_user/{id_type}/{id_value}?policy_name="something"
    app.router.add_get("/API/firewall_policy_user/{id_type}/{id_value}?", object.get_firewall_policies_user)

    # http://127.0.0.1/API/firewall_policy/{table_name}/{id}"
    app.router.add_get("/API/firewall_policy/{table_name}/{id}", object.get_firewall_policies_table_instance)

    # http://127.0.0.1/API/firewall_policy/{table_name}" or added filters(?policy_type=something)
    app.router.add_get("/API/firewall_policy/{table_name}", object.get_firewall_policies_table)

    # http://127.0.0.1/API/firewall_policy/{table_name}"
    # Data = [{'fqdn':'raimo1.aalto.fi', 'msisdn':'0441414141', 'ipv4':'1.1.1.1'}]
    app.router.add_post("/API/firewall_policy/{table_name}", object.insert_firewall_policies)

    # http://127.0.0.1/API/firewall_policy/{table_name}"
    # Data = [{'fqdn':'raimo1.aalto.fi', 'msisdn':'0441414141', 'ipv4':'1.1.1.1'}]
    app.router.add_put("/API/firewall_policy/{table_name}/{id}", object.update_firewall_policies)



    ########################################
    ########################################


    # http://127.0.0.1/API/cetp_policy_node?policy_name=something&lfqdn=something&rfqdn=something&direction=EGRESS
    app.router.add_get("/API/cetp_policy_node?", object.get_cetp_policies_node)

    ########################################
    ########################################


    # http://127.0.0.1/API/ces_policy_node?protocol=something&link_alias=something&dest_ces=something&direction=EGRESS&policy=something
    app.router.add_get("/API/ces_policy_node?", object.get_ces_policies_node)


    ########################################
    ########################################


    # http://127.0.0.1/API/bootstrap_policies/{id}"
    app.router.add_get("/API/bootstrap_policies/{id}", object.get_bootstrap_policies_instance)

    # http://127.0.0.1/API/bootstrap_policies?policy_name=something"
    app.router.add_get("/API/bootstrap_policies", object.get_bootstrap_policies)

    # http://127.0.0.1/API/bootstrap_policies_ces" or added filters(?policy_name=something)
    app.router.add_get("/API/bootstrap_policies_ces", object.get_bootstrap_policies_ces)


    # http://127.0.0.1/API/bootstrap_policies"
    app.router.add_post("/API/bootstrap_policies", object.insert_bootstrap_policies)

    # http://127.0.0.1/API/bootstrap_policies/{id}"
    app.router.add_put("/API/bootstrap_policies/{id}", object.update_bootstrap_policies)



    ########################################
    ########################################


    # http://127.0.0.1/API/firewall_policy/{table_name}/{id} OR {ids}
    app.router.add_delete("/API/firewall_policy/{table_name}/{id}", object.delete_policies)

    # http://127.0.0.1/API/firewall_policy/{table_name}?parameters=value
    app.router.add_delete("/API/firewall_policy/{table_name}", object.delete_policies)

    # http://127.0.0.1/API/bootstrap_policies/{id} or {ids}
    app.router.add_delete("/API/bootstrap_policies/{id}", object.delete_bootstrap_data)

    # http://127.0.0.1/API/bootstrap_policies"
    app.router.add_delete("/API/bootstrap_policies", object.delete_bootstrap_data)

    '''

    #http://127.0.0.1/API/delete_policy_cesapp/{id}
    app.router.add_delete("/API/delete_policy_cesapp/{id}", object.delete_policies_cesapp)

    # http://127.0.0.1/API/delete_policy_cesapp/all
    app.router.add_delete("/API/delete_policy_cesapp/all", object.delete_policies_cesapp_all)

    '''
    ########################################
    ########################################

    #http://127.0.0.1/API/user_registration/?username=something&ip=1.1.1.1
    app.router.add_post("/API/user_registration/?", object.user_registration)


    # http://127.0.0.1/API/tables_get_columns/{table_name}"
    app.router.add_get("/API/tables_get_columns/{table_name}", object.host_retrieve_columns)

    ########################################
    ########################################


    return await loop.create_server(app.make_handler(), address, port)
    #return await loop.create_server(app.make_handler(), address, 443, ssl=sslcontext)


if __name__ == '__main__':
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslcontext.load_cert_chain('cert.pem', 'key.pem')

    loop = asyncio.get_event_loop()
    #loop.run_until_complete(build_server(loop, '0.0.0.0', 443, sslcontext))
    loop.run_until_complete(build_server(loop, '0.0.0.0', 80, sslcontext))
    print("Server ready!")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting Down!")
        loop.close()
