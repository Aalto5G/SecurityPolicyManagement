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

import datetime, json, re, socket

from errorsfile import API_ERROR


class Validator():

    def _ipv4_validation(test_ip):
        '''
        check if ip address is a valid ipv4 address
        :param test_ip: input IP for test
        :return: none or raise an exception
        '''
        only_ip= test_ip.split('/')[0]
        try:
            if '.' in only_ip:
                socket.inet_pton(socket.AF_INET, only_ip)
            else:
                socket.inet_pton(socket.AF_INET6, only_ip)
        except socket.error:
            error = "{} is not a valid IPv4 Address".format(only_ip)
            raise API_ERROR(1005, error)
        return "'" + test_ip + "'"



    def _dictionary_test(data):
        '''
        Check if the raw_data is in dictionary format
        :param data: Input raw_data
        :return: None or raise an exception
        '''
        try:
            json.loads(data)
        except:
            try:
                data = data.replace("'", '"')
                json.loads(data)
            except Exception as e:
                error = "{} is not a valid dictionary format.".format(data)
                raise API_ERROR(1005, error)
        return "'" + data + "'"



    def _port_validation(port):
        '''
        Check if port number are comma separated integers or jsut one number
        :param port: port number string
        :return: none or raise an exception
        '''
        if port:
            try:
                test = re.match(r'(\d+(:\d+|,\d+)*)?$', str(port))
                if not test:
                    error = "{} is not correct format for port. Either an integer or comma separated integer is accepted".format(
                        port)
                    raise API_ERROR(1005, error)
            except:
                error = "{} is not correct format for port. Either an integer or comma separated integer is accepted.".format(
                    port)
                raise API_ERROR(1005, error)
        return "'" + str(port) + "'"


    def _protocol_validation(protocol):
        '''
        Check if protocol is present in options
        :param protocol: protocol string
        :return: none or raise an exception
        '''
        if protocol not in ['tls', 'tcp', 'udp', 'icmp', 'sctp', 'dccp', 'stp', 'dtp']:
            error = "{} is not supported in Protocols.".format(protocol)
            raise API_ERROR(1005, error)
        return "'" + protocol + "'"


    def _direction_validation(direction):
        '''
        Check if direction has the value of either INGRESS or EGRESS
        :param direction: input direction string
        :return: None or raise an exception
        '''
        if direction not in ['*', 'EGRESS', 'INGRESS']:
            error = "{} is not supported in direction. Only Acceptable values are EGRESS, INGRESS and *".format(direction)
            raise API_ERROR(1005, error)
        return "'" + direction + "'"


    def _target_validation(target):
        '''
        Check if target has the value of either ACCEPT or DROP
        :param target: input target string
        :return: None or raise an exception
        '''
        if target not in ['ACCEPT', 'DROP', 'REJECT']:
            error = "{} is not supported in Target. Only Acceptable values are ACCEPT, DROP and REJECT".format(target)
            raise API_ERROR(1005, error)
        return "'" + target + "'"


    def _firewall_type_validation(fw_type):
        '''
        Check if type has the value of either FIREWALL_ADMIN or FIREWALL_USER
        :param fw_type: input target string
        :return: None or raise an exception
        '''
        if fw_type not in ['FIREWALL_ADMIN', 'FIREWALL_USER']:
            error = "{} is not supported in type. Only Acceptable values are FIREWALL_ADMIN and FIREWALL_USER".format(fw_type)
            raise API_ERROR(1005, error)
        return "'" + fw_type + "'"


    def _type_in_cetp_required_test(type_cetp):
        '''
        Check if type has the value of either FIREWALL_ADMIN or FIREWALL_USER
        :param fw_type: input target string
        :return: None or raise an exception
        '''
        if type_cetp not in ['host_cetp_id', 'host_cetp_control_params', 'host_cetp_payload', 'host_cetp_rloc']:
            error = "{} is not supported in type. Only Acceptable values are host_cetp_id, host_cetp_control_params" \
                    "host_cetp_payload and host_cetp_rloc".format(type_cetp)
            raise API_ERROR(1005, error)
        return "'" + type_cetp + "'"


    def _date_validation(date):
        '''
        Check if schedule date has the correct format of '%Y-%m-%d %H:%M:%S'
        :param date: input schedule date
        :return: None or raise an exception
        '''
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except:
            error = "{} is not correct. The date must be in format 'YYYY-MM-DD HH:MM:SS'".format(date)
            raise API_ERROR(1005, error)
        return "'" + date + "'"


    def _schedule_validation(Schedule_Start, Schedule_End):
        '''
        Check if Schedule end date is in future of schedule start date. Also check if time difference is minimum 5 minutes
        :param Schedule_Start: Date of schedule start in a string
        :param Schedule_End: Date of schedule end in a string
        :return: nothing or raise an exception
        '''
        time_difference = datetime.datetime.strptime(Schedule_End, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(
            Schedule_Start, '%Y-%m-%d %H:%M:%S')
        if time_difference.days < 1:
            if time_difference.seconds < 300:
                error = "Time Difference between schedule start and schedule end should be minimum 5 minutes"
                raise API_ERROR(1005, error)


    def _adding_quotes_(input):
        return "'" + str(input) + "'"


    def _bootstrap_name_validation(name):
        '''
        Check if name has the value of either IPTABLES, IPSET or CIRCULARPOOL
        :param name: input target string
        :return: None or raise an exception
        '''
        if name not in ['IPTABLES', 'IPSET', 'CIRCULARPOOL']:
            error = "{} is not supported in type. Only Acceptable values are IPTABLES, IPSET or CIRCULARPOOL".format(name)
            raise API_ERROR(1005, error)
        return "'" + name + "'"

    def _type_validation(name):
        '''
        Check if name has the value of either IPTABLES, IPSET or CIRCULARPOOL
        :param name: input target string
        :return: None or raise an exception
        '''
        if name not in ['GROUP', 'CIRCULARPOOL', 'CARRIERGRADE', 'SFQDN', 'FIREWALL']:
            error = "{} is not supported in type. Only Acceptable values are GROUP, CIRCULARPOOL, CARRIERGRADE, SFQDN and FIREWALL".format(name)
            raise API_ERROR(1005, error)
        return "'" + name + "'"

    def _sub_type_validation(name):
        '''
        Check if name has the value of either IPTABLES, IPSET or CIRCULARPOOL
        :param name: input target string
        :return: None or raise an exception
        '''
        if name not in ['FIREWALL_ADMIN', 'FIREWALL_USER']:
            error = "{} is not supported in sub type. Only Acceptable values are FIREWALL_ADMIN and FIREWALL_USER".format(name)
            raise API_ERROR(1005, error)
        return "'" + name + "'"


    def _cetp_type_validation(name):
        '''
        Check if name has the value of either ID, PAYLOAD, CONTROL_PARAMS
        :param name: input target string
        :return: None or raise an exception
        '''
        if name not in ['available', 'request','offer']:
            error = "{} is not supported in cetp type. Only Acceptable values are available, request, offer".format(name)
            raise API_ERROR(1005, error)
        return "'" + name + "'"


    def bootstrap_subtype_validator(name):
        '''
        Check if name has the value of either request or rules
        :param name: input target string
        :return: None or raise an exception
        '''
        if name not in ['requires', 'rules']:
            error = "{} is not supported in subtype. Only Acceptable values are rules or requires".format(name)
            raise API_ERROR(1005, error)
        return "'" + name + "'"


    def _integer_validation(data):
        '''
        Check if input is an integer
        :param date: input variable
        :return: None or raise an exception
        '''
        try:
            int(data)
        except:
            error = "{} is not an integer.".format(data)
            raise API_ERROR(1005, error)
        return "'" + str(data) + "'"


    def _boolean_validation(data):
        '''
        Check if input is boolean field
        :param date: input variable
        :return: None or raise an exception
        '''
        try:
            if int(data) in [1, 0]:
                pass
            else:
                error = "{} is not BooleanValue. Only 1 or 0 are accepted values".format(data)
                raise API_ERROR(1005, error)
        except:
            error = "{} is not BooleanValue. Only 1 or 0 are accepted values".format(data)
            raise API_ERROR(1005, error)
        return int(data)


    def _number_validation(data):
        '''
        Check if input is number field
        :param date: input variable
        :return: None or raise an exception
        '''
        try:
            if data.isdigit():
                pass
            else:
                error = "{} is not number. Only digits are accepted in this field".format(data)
                raise API_ERROR(1005, error)
        except:
            error = "{} is not number. Only digits are accepted in this field".format(data)
            raise API_ERROR(1005, error)
        return "'" + str(data) + "'"


    ###################################################################################
    ###################################################################################
    ###################################################################################


    def _ids_validator(**kwargs):
        '''
        # Validate input ids for function host_ids. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from query
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['ipv4'] = 'Null' if 'ipv4' not in kwargs or not kwargs['ipv4'] else Validator._ipv4_validation(kwargs['ipv4'])
        kwargs['fqdn'] = Validator._adding_quotes_(kwargs['fqdn'])
        kwargs['username'] = Validator._adding_quotes_(kwargs['username'])
        kwargs['msisdn'] = 'Null' if 'msisdn' not in kwargs or not kwargs['msisdn'] else Validator._number_validation(kwargs['msisdn'])
        return kwargs


    def _firewall_policy_validator_old(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        if 'fqdn' not in kwargs or not kwargs['fqdn']:
            raise API_ERROR(1005, 'FQDN missing in query')
        kwargs['sport'] = 'Null' if 'sport' not in kwargs or not kwargs['sport'] else Validator._port_validation(kwargs['sport'])
        kwargs['dport'] = 'Null' if 'dport' not in kwargs or not kwargs['dport'] else Validator._port_validation(kwargs['dport'])
        kwargs['src'] = 'Null' if 'src' not in kwargs or not kwargs['src'] else Validator._ipv4_validation(kwargs['src'])
        kwargs['dst'] = 'Null' if 'dst' not in kwargs or not kwargs['dst'] else Validator._ipv4_validation(kwargs['dst'])
        kwargs['protocol'] = 'Null' if 'protocol' not in kwargs or not kwargs['protocol'] else Validator._integer_validation(kwargs['protocol'])
        kwargs['cesapp_id'] = 'Null' if 'cesapp_id' not in kwargs or not kwargs['cesapp_id'] else Validator._integer_validation(kwargs['cesapp_id'])
        kwargs['schedule_start'] = 'Null' if 'schedule_start' not in kwargs or not kwargs['schedule_start'] else Validator._date_validation(kwargs['schedule_start'])
        kwargs['schedule_end'] = 'Null' if 'schedule_end' not in kwargs or not kwargs['schedule_end'] else Validator._date_validation(kwargs['schedule_end'])
        kwargs['raw_data'] = "'{}'" if 'raw_data' not in kwargs or not kwargs['raw_data'] else Validator._dictionary_test(kwargs['raw_data'])
        kwargs['active'] = 1 if 'active' not in kwargs or not kwargs['active'] else Validator._boolean_validation(kwargs['active'])
        kwargs['comment'] = "'[]'" if 'comment' not in kwargs or not kwargs['comment'] else Validator._dictionary_test(kwargs['comment'])
        kwargs['type'] = "'FIREWALL_USER'" if 'type' not in kwargs or not kwargs['type'] else Validator._firewall_type_validation(kwargs['type'].upper())
        kwargs['direction'] = "'*'" if 'direction' not in kwargs or not kwargs['direction'] else Validator._direction_validation(kwargs['direction'].upper())
        kwargs['target'] = "'DROP'" if 'target' not in kwargs or not kwargs['target'] else Validator._target_validation(kwargs['target'].upper())
        kwargs['priority'] = 10 if 'priority' not in kwargs or not kwargs['priority'] else Validator._integer_validation(kwargs['priority'])
        return kwargs

    def _firewall_policy_validator_filter(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        if 'fqdn' not in kwargs or not kwargs['fqdn']:
            raise API_ERROR(1005, 'FQDN missing in query')
        kwargs['fqdn'] = Validator._adding_quotes_(kwargs['fqdn'])
        if 'types' not in kwargs or not kwargs['types']:
            raise API_ERROR(1005, 'Type missing in query')
        kwargs['types'] = Validator._type_validation(kwargs['types'].upper())

        if kwargs['types']=="'FIREWALL'":
            kwargs = Validator._firewall_firewall_policy_validator(kwargs)
        elif kwargs['types']=="'GROUP'":
            kwargs = Validator._firewall_group_policy_validator(kwargs)
        elif kwargs['types']=="'SFQDN'":
            kwargs = Validator._firewall_sfqdn_policy_validator(kwargs)
        elif kwargs['types']=="'CARRIERGRADE'":
            kwargs = Validator._firewall_carriergrade_policy_validator(kwargs)
        elif kwargs['types']=="'CIRCULARPOOL'":
            kwargs = Validator._firewall_circularpool_policy_validator(kwargs)
        return kwargs


    def _cetp_policy_identity_validator(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['local_fqdn'] = 'Null' if 'local_fqdn' not in kwargs or not kwargs['local_fqdn'] else Validator._adding_quotes_(kwargs['local_fqdn'])
        kwargs['remote_fqdn'] = 'Null' if 'remote_fqdn' not in kwargs or not kwargs['remote_fqdn'] else Validator._adding_quotes_(kwargs['remote_fqdn'])
        kwargs['reputation'] = 'Null' if 'reputation' not in kwargs or not kwargs['reputation'] else Validator._adding_quotes_(kwargs['reputation'])
        kwargs['direction'] = 'Null' if 'direction' not in kwargs or not kwargs['direction'] else Validator._direction_validation(kwargs['direction'].upper())
        return kwargs


    def _cetp_policies_validator(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        if 'policy_element' not in kwargs or not kwargs['policy_element']:
            raise API_ERROR(1005, 'Policy element missing in query')
        if 'types' not in kwargs or not kwargs['types']:
            raise API_ERROR(1005, 'Policy types missing in query')
        if 'uuid' not in kwargs or not kwargs['uuid']:
            raise API_ERROR(1005, 'UUID missing in query')
        kwargs['types'] = Validator._cetp_type_validation(kwargs['types'].lower())
        kwargs['policy_element'] = Validator._dictionary_test(kwargs['policy_element'])
        kwargs['uuid'] = Validator._adding_quotes_(kwargs['uuid'])
        return kwargs


    def _ces_policy_identity_validator(**kwargs):
        '''
        # Validate input policy for function ces policy identity. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        if 'host_ces_id' not in kwargs or not kwargs['host_ces_id']:
            raise API_ERROR(1005, 'CES ID missing in query')
        if 'protocol' not in kwargs or not kwargs['protocol']:
            raise API_ERROR(1005, 'Protocol missing in query')
        kwargs['host_ces_id'] = Validator._adding_quotes_(kwargs['host_ces_id'])
        kwargs['protocol'] = Validator._adding_quotes_(kwargs['protocol'])
        return kwargs


    def _firewall_firewall_policy_validator(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['sub_type'] = 'Null' if 'sub_type' not in kwargs or not kwargs['sub_type'] else Validator._sub_type_validation(kwargs['sub_type'].upper())
        if 'policy_element' not in kwargs or not kwargs['policy_element']:
            raise API_ERROR(1005, 'Policy missing in query')
        kwargs['policy_element'] = Validator._dictionary_test(kwargs['policy_element'])
        return kwargs


    def _firewall_group_policy_validator(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['sub_type'] = "''"
        if 'policy_element' not in kwargs or not kwargs['policy_element']:
            raise API_ERROR(1005, 'Policy missing in query')
        else:
            kwargs['policy_element'] = Validator._adding_quotes_(kwargs['policy_element'])
        return kwargs


    def _firewall_circularpool_policy_validator(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['sub_type'] = "''"
        if 'policy_element' not in kwargs or not kwargs['policy_element']:
            raise API_ERROR(1005, 'Policy missing in query')
        else:
            kwargs['policy_element'] = Validator._dictionary_test(kwargs['policy_element'])
        return kwargs


    def _firewall_carriergrade_policy_validator(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['sub_type'] = "''"
        if 'policy_element' not in kwargs or not kwargs['policy_element']:
            raise API_ERROR(1005, 'Policy missing in query')
        else:
            kwargs['policy_element'] = Validator._dictionary_test(kwargs['policy_element'])
        return kwargs


    def _firewall_sfqdn_policy_validator(**kwargs):
        '''
        # Validate input policy for function Firewall. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['sub_type'] = "''"
        if 'policy_element' not in kwargs or not kwargs['policy_element']:
            raise API_ERROR(1005, 'Policy missing in query')
        else:
            kwargs['policy_element'] = Validator._dictionary_test(kwargs['policy_element'])
        return kwargs


    def _sfqdn_validator(**kwargs):
        '''
        # Validate input sfqdn policy for function sfqdns. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        #uuid, fqdn, proxy_required, carriergrade, protocol, port, loose_packet, raw_data
        kwargs['sfqdn'] = "'" + kwargs['sfqdn'] + "'"
        kwargs['protocol'] = 'Null' if 'protocol' not in kwargs or not kwargs['protocol'] else Validator._integer_validation(kwargs['protocol'])
        kwargs['port'] = 'Null' if 'port' not in kwargs or not kwargs['port'] else Validator._port_validation(kwargs['port'])
        kwargs['raw_data'] = "'{}'" if 'raw_data' not in kwargs or not kwargs['raw_data'] else Validator._dictionary_test(kwargs['raw_data'])
        kwargs['loose_packet'] = 'Null' if 'loose_packet' not in kwargs or not kwargs['loose_packet'] else Validator._integer_validation(kwargs['loose_packet'])
        kwargs['carriergrade'] = 'Null' if 'carriergrade' not in kwargs or not kwargs['carriergrade'] else Validator._boolean_validation(kwargs['carriergrade'])
        kwargs['proxy_required'] = 'Null' if 'proxy_required' not in kwargs or not kwargs['proxy_required'] else Validator._boolean_validation(kwargs['proxy_required'])
        return kwargs


    def _bootstrap_validator(**kwargs):
        '''
        # Validate input bootstrap policy for bootstrap table. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        # name, types, sub_type, data
        if 'name' not in kwargs or not kwargs['name']:
            raise API_ERROR(1005, 'Name missing in query')
        if 'sub_type' not in kwargs or not kwargs['sub_type']:
            raise API_ERROR(1005, 'Sub Type missing in query')
        if 'data' not in kwargs or not kwargs['data']:
            raise API_ERROR(1005, 'data missing in query')
        kwargs['name'] = Validator._bootstrap_name_validation(kwargs['name'])
        kwargs['sub_type'] = Validator.bootstrap_subtype_validator(kwargs['sub_type'])
        kwargs['data'] = Validator._dictionary_test(kwargs['data'])
        kwargs['types'] = 'Null' if 'types' not in kwargs or not kwargs['types'] else Validator._adding_quotes_(kwargs['types'])
        return kwargs

    def cetp_get_policies(**kwargs):
        '''
        # Validate parameters to formulate CETP SQL get query for a host
        :param kwargs: Dictionary of all the query parameters received from client
        (local_fqdn, remote_fqdn, direction, policy_name)
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['local_fqdn'] = '' if 'local_fqdn' not in kwargs else kwargs['local_fqdn']
        kwargs['remote_fqdn'] = '' if 'remote_fqdn' not in kwargs or not kwargs['remote_fqdn'] else ' and remote_fqdn="{}"'.format(kwargs['remote_fqdn'])
        kwargs['direction'] = '*' if 'direction' not in kwargs or not kwargs['direction'] else ' and direction="{}"'.format(kwargs['direction'])
        kwargs['policy_name'] = '' if 'policy_name' not in kwargs or not kwargs['policy_name'] else ' and types="{}"'.format(kwargs['policy_name'])
        return kwargs


    def ces_get_policies(**kwargs):
        '''
        # Validate parameters to formulate CES SQL get query for a host
        :param kwargs: Dictionary of all the query parameters received from client
        (host_ces_id, protocol)
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        # host_ces_id, protocol
        kwargs['host_ces_id'] = Validator._adding_quotes_(kwargs['host_ces_id'])
        kwargs['protocol'] = Validator._adding_quotes_(kwargs['protocol'])
        return kwargs


    def firewall_get_policies(**kwargs): #/////////////////////////////////////////////////////////////////////////////
        '''
        # Validate parameters to formulate Firewall SQL get query for a host
        :param kwargs: Dictionary of all the query parameters received from client
        (id_type, id_value, policy_name)
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['id_type'] = '' if 'id_type' not in kwargs else kwargs['id_type']
        kwargs['id_value'] = '' if 'id_value' not in kwargs else kwargs['id_value']
        kwargs['policy_name'] = '' if 'policy_name' not in kwargs or not kwargs['policy_name'] else ' and types="{}"'.format(kwargs['policy_name'])
        return kwargs


    def _cetp_policy_negotiation_validator(**kwargs):
        '''
        # Validate input bootstrap policy for bootstrap table. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['local_fqdn'] = "'" + str(kwargs['local_fqdn']) + "'"
        kwargs['remote_fqdn'] = "'*'" if 'remote_fqdn' not in kwargs or not kwargs['remote_fqdn'] else "'" + str(kwargs['remote_fqdn']) + "'"
        kwargs['reputation'] = "'*'" if 'reputation' not in kwargs or not kwargs['reputation'] else "'" + str(kwargs['reputation']) + "'"
        kwargs['direction'] = "'*'" if 'direction' not in kwargs or not kwargs['direction'] else Validator._direction_validation(kwargs['direction'].upper())
        return kwargs


    def _cetp_policy_id_validator(**kwargs):
        '''
        # Validate input bootstrap policy for bootstrap table. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['local_fqdn'] = "'" + str(kwargs['local_fqdn']) + "'"
        kwargs['id_type'] = "'" + str(kwargs['id_type']) + "'"
        kwargs['value'] = "'" + str(kwargs['value']) + "'"
        return kwargs


    def _cetp_policy_control_validator(**kwargs):
        '''
        # Validate input bootstrap policy for bootstrap table. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        kwargs['local_fqdn'] = "'" + str(kwargs['local_fqdn']) + "'"
        kwargs['remote_fqdn'] = "'*'" if 'remote_fqdn' not in kwargs or not kwargs['remote_fqdn'] else "'" + str(kwargs['remote_fqdn']) + "'"
        kwargs['direction'] = "'*'" if 'direction' not in kwargs else Validator._direction_validation(kwargs['direction'].upper())
        kwargs['parameters'] = "'" + str(kwargs['parameters']) + "'"
        kwargs['value'] = 'Null' if 'value' not in kwargs or not kwargs['value'] else "'" + str(kwargs['value']) + "'"
        return kwargs


    def _cetp_policy_payload_validator(**kwargs):
        '''
        # Validate input bootstrap policy for bootstrap table. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        # uid, type, parameter, constraint,
        kwargs['local_fqdn'] = "'" + str(kwargs['local_fqdn']) + "'"
        kwargs['remote_fqdn'] = "'*'" if 'remote_fqdn' not in kwargs or not kwargs['remote_fqdn'] else "'" + str(kwargs['remote_fqdn']) + "'"
        kwargs['payload_type'] = "'" + str(kwargs['payload_type']) + "'"
        kwargs['value'] = 'Null' if 'value' not in kwargs or not kwargs['value'] else "'" + str(kwargs['value']) + "'"
        return kwargs


    def _cetp_policy_rloc_validator(**kwargs):
        '''
        # Validate input bootstrap policy for bootstrap table. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of all the values received from user
        :return: Either raise an error in case of validation failure or returns a dictionary
        '''
        # uid, type, parameter, constraint,
        kwargs['local_fqdn'] = "'" + str(kwargs['local_fqdn']) + "'"
        kwargs['remote_fqdn'] = "'*'" if 'remote_fqdn' not in kwargs or not kwargs['remote_fqdn'] else "'" + str(kwargs['remote_fqdn']) + "'"
        kwargs['rloc_type'] = "'" + str(kwargs['rloc_type']) + "'"
        kwargs['value'] = 'Null' if 'value' not in kwargs or not kwargs['value'] else "'" + str(kwargs['value']) + "'"
        return kwargs




    def _ces_policy_params_validator(**kwargs):
        '''
        # Validate input CES_PARAMS policy in ces_policy_params table. Put quotation marks at the ends to validate the policies to
        insert in table. Also set Null value for empty fiels
        :param kwargs: Dictionary of All values
        :return: Return Values after validation
        '''
        kwargs['trans_protocol'] = 'Null' if 'trans_protocol' not in kwargs or not kwargs[
            'trans_protocol'] else Validator._protocol_validation(kwargs['trans_protocol'].lower())
        kwargs['link_alias'] = "'*'" if 'link_alias' not in kwargs else "'" + str(kwargs['link_alias']) + "'"
        kwargs['dest_ces'] = "'*'" if 'dest_ces' not in kwargs else "'" + str(kwargs['dest_ces']) + "'"
        kwargs['reputation'] = "'*'" if 'reputation' not in kwargs else "'" + str(kwargs['reputation']) + "'"
        kwargs['direction'] = "'*'" if 'direction' not in kwargs or not kwargs[
            'direction'] else Validator._direction_validation(kwargs['direction'].upper())
        kwargs['parameter'] = "'" + str(kwargs['parameter']) + "'"
        kwargs['value'] = 'Null' if 'value' not in kwargs else "'" + str(kwargs['value']) + "'"
        return kwargs










