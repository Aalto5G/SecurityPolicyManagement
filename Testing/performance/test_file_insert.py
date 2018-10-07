import unittest
import requests, json, time



class TestStringMethods(unittest.TestCase):



    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   INSERT HOST POLICIES



    # Inserting Policy in ID Table with only fqdn
    def test_insert_id_duplicate_entry_parameters(self):
        data = {'fqdn':'test.gwa.demo.', 'msisdn':'0000000100', 'ipv4':'192.168.0.100'}
        url = "http://127.0.0.1/API/host_policy/id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)


    # Inserting Policy in ID Table with wrong ip address
    def test_insert_id_wrong_ip_address(self):
        data = {'fqdn':'test3.gwa.demo.', 'msisdn':'0000000100', 'ipv4':'192.168.0.1001'}
        url = "http://127.0.0.1/API/host_policy/id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.content.decode("utf-8"), '"192.168.0.1001 is not a valid IPv4 Address"')
        self.assertEqual(data.status_code, 605)


    # Inserting Policy in ID Table without parameters
    def test_insert_id_no_parameters(self):
        data = {}
        url = "http://127.0.0.1/API/host_policy/id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)

    ##############################################################################################################

    # Inserting Policy in SFQDN Table with correct parameters
    def test_insert_sfqdn_correct_parameters(self):
        data = {'fqdn': 'test.gwa.demo.', 'sfqdn': 'udp1235.test.gwa.demo', 'proxy_required': '0', 'carriergrade': 0,
                'protocol': '17', 'port': '1234', 'loose_packet': '-1', 'raw_data': '{"autobind": "false", "timeout": "3600"}'}
        url = "http://127.0.0.1/API/host_policy/sfqdn"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in SFQDN Table with wrong format in raw_data
    def test_insert_sfqdn_with_wrong_json_rawdata(self):
        data = {'fqdn': 'test.gwa.demo.', 'sfqdn': 'udp1235.test.gwa.demo', 'proxy_required': '0', 'carriergrade': 0,
                'protocol': '17', 'port': '1234', 'loose_packet': '-1', 'raw_data': '"autobind": "false", "timeout": "3600"}'}
        url = "http://127.0.0.1/API/host_policy/sfqdn"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 605)


    # Inserting Policy in SFQDN Table with incomplete parameters
    def test_insert_sfqdn_incomplete_parameters(self):
        data = {'fqdn': 'test.gwa.demo.', 'sfqdn': 'ssh.test.gwa.demo'}
        url = "http://127.0.0.1/API/host_policy/sfqdn"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200) #608


    # Inserting Policy in SFQDN Table with invalid parameters
    def test_insert_sfqdn_invalid_parameters(self):
        data = {'fqdn': 'test.gwa.demo.', 'sfqdn': 'udp1235.test.gwa.demo', 'proxy_required': 'asdfasd', 'carriergrade': 123,
                'protocol': '17', 'port': '1234', 'loose_packet': '-1', 'raw_data': '{"autobind": "false", "timeout": "3600"}'}
        url = "http://127.0.0.1/API/host_policy/sfqdn"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 605)


    # Inserting Policy in SFQDN Table with duplicate Entry
    def test_insert_sfqdn_duplicate_entry(self):
        data = {'fqdn': 'test.gwa.demo.', 'sfqdn': 'udp1235.test.gwa.demo', 'proxy_required': '0', 'carriergrade': 0,
                'protocol': '17', 'port': '1234', 'loose_packet': '-1', 'raw_data': '{"autobind": "false", "timeout": "3600"}'}
        url = "http://127.0.0.1/API/host_policy/sfqdn"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)


    # Inserting Policy in SFQDN Table without parameter
    def test_insert_sfqdn_no_parameters(self):
        data = {}
        url = "http://127.0.0.1/API/host_policy/sfqdn"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)


    ##############################################################################################################


    # Inserting Policy in FIREWALL Table with correct parameters
    def test_insert_firewall_correct_parameters(self):
        data = {'fqdn': 'test.gwa.demo.', 'type': 'FIREWALL_ADMIN', 'priority': '0', 'direction': 'EGRESS',
                'dport': '53', 'protocol':'17', 'target':'REJECT', 'comment':"{'comment':'Host DNS limit'}", 'raw_data':"{'hashlimit': {'hashlimit-above':'5/sec', 'hashlimit-burst':'50', 'hashlimit-name':'DnsLanHosts', 'hashlimit-mode':'srcip', 'hashlimit-htable-expire':'1001'}}"}
        url = "http://127.0.0.1/API/host_policy/firewall"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in FIREWALL Table with incomplete parameters
    def test_insert_firewall_incomplete_parameters(self):
        data = {'fqdn': 'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_policy/firewall"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in FIREWALL Table with invalid parameters
    def test_insert_firewall_invalid_parameters(self):
        data = {'fqdn': 'test.gwa.demo.', 'type': 'FIREWALL_AaDMIN', 'priority': 'a', 'direction': 'EGsRESS',
                'dport': '5d3', 'protocol': '17', 'target': 'sssas', 'comment': "'comment':'Host DNS limit'}",
                'raw_data': "{'hashlimit': {'hashlimit-above':'5/sec', 'hashlimit-burst':'50', 'hashlimit-name':'DnsLanHosts', 'hashlimit-mode':'srcip', 'hashlimit-htable-expire':'1001'}}"}
        url = "http://127.0.0.1/API/host_policy/firewall"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 605)


    # Inserting Policy in FIREWALL Table with duplicate Entry
    def test_insert_firewall_duplicate_entry(self):
        data = {'fqdn': 'test.gwa.demo.', 'type': 'FIREWALL_ADMIN', 'priority': '0', 'direction': 'EGRESS',
                'dport': '53', 'protocol': '17', 'target': 'REJECT', 'comment': "{'comment':'Host DNS limit'}",
                'raw_data': "{'hashlimit': {'hashlimit-above':'5/sec', 'hashlimit-burst':'50', 'hashlimit-name':'DnsLanHosts', 'hashlimit-mode':'srcip', 'hashlimit-htable-expire':'1001'}}"}
        url = "http://127.0.0.1/API/host_policy/firewall"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200) #608


    # Inserting Policy in FIREWALL Table without parameter
    def test_insert_firewall_no_parameters(self):
        data = {}
        url = "http://127.0.0.1/API/host_policy/firewall"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)


    ##############################################################################################################


    # Inserting Policy in CIRCULARPOOL Table with correct parameters
    def test_insert_circularpool_correct_parameters(self):
        time.sleep(1)
        data = {'fqdn': 'test.gwa.demo.', 'raw_data':'{"max": 100}'}
        url = "http://127.0.0.1/API/host_policy/circularpool"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CIRCULARPOOL Table with incomplete parameters
    def test_insert_circularpool_incomplete_parameters(self):
        data = {'fqdn': 'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_policy/circularpool"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)


    # Inserting Policy in CIRCULARPOOL Table with invalid parameters
    def test_insert_circularpool_invalid_parameters(self):
        data = {'fqdn': 'test.gwa.demo.', 'raw_data': '{max: 100}'}
        url = "http://127.0.0.1/API/host_policy/circularpool"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 605)


    # Inserting Policy in CIRCULARPOOL Table with duplicate Entry
    def test_insert_circularpool_duplicate_entry(self):
        data = {'fqdn': 'test.gwa.demo.', 'raw_data': '{"max": 100}'}
        url = "http://127.0.0.1/API/host_policy/circularpool"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)


    # Inserting Policy in CIRCULARPOOL Table without parameter
    def test_insert_circularpool_no_parameters(self):
        data = {}
        url = "http://127.0.0.1/API/host_policy/circularpool"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)


    ##############################################################################################################


    # Inserting Policy in CARRIERGRADE Table with correct parameters
    def test_insert_carriergrade_correct_parameters(self):
        time.sleep(1)
        data = {'fqdn': 'test.gwa.demo.', 'raw_data':'{"ipv4": "192.168.0.10"}'}
        url = "http://127.0.0.1/API/host_policy/carriergrade"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CARRIERGRADE Table with incomplete parameters
    def test_insert_carriergrade_incomplete_parameters(self):
        data = {'fqdn': 'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_policy/carriergrade"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)


    # Inserting Policy in CARRIERGRADE Table with invalid parameters
    def test_insert_carriergrade_invalid_parameters(self):
        data = {'fqdn': 'test.gwa.demo.', 'raw_data': '{ipv4: 192.168.0.10}'}
        url = "http://127.0.0.1/API/host_policy/carriergrade"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 605)


    # Inserting Policy in CARRIERGRADE Table with duplicate Entry
    def test_insert_carriergrade_duplicate_entry(self):
        data = {'fqdn': 'test.gwa.demo.', 'raw_data': '{"ipv4": "192.168.0.10"}'}
        url = "http://127.0.0.1/API/host_policy/carriergrade"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)


    # Inserting Policy in CARRIERGRADE Table without parameter
    def test_insert_carriergrade_no_parameters(self):
        data = {}
        url = "http://127.0.0.1/API/host_policy/carriergrade"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)


    ##############################################################################################################


    # Inserting Policy in GROUP Table with correct parameters
    def test_insert_group_correct_parameters(self):
        time.sleep(1)
        data = {'fqdn': 'test.gwa.demo.', 'group':'IPS_GROUP_POSTPAID'}
        url = "http://127.0.0.1/API/host_policy/group"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in GROUP Table with incomplete parameters
    def test_insert_group_incomplete_parameters(self):
        data = {'fqdn': 'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_policy/group"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)



    # Inserting Policy in GROUP Table with duplicate Entry
    def test_insert_group_duplicate_entry(self):
        data = {'fqdn': 'test.gwa.demo.', 'group': 'IPS_GROUP_POSTPAID'}
        url = "http://127.0.0.1/API/host_policy/group"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)


    # Inserting Policy in GROUP Table without parameter
    def test_insert_group_no_parameters(self):
        data = {}
        url = "http://127.0.0.1/API/host_policy/group"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 609)


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   INSERT CETP POLICIES

    # Inserting Policy in CETP_PAYLOAD Table with correct parameters
    def test_insert_cetp_payload_correct_parameters(self):
        data = {'local_fqdn':'test.gwa.demo.', 'payload_type':'eth'}
        url = "http://127.0.0.1/API/host_cetp/cetp_payload"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CETP_PAYLOAD Table with only fqdn. Incomplete parameters
    def test_insert_cetp_payload_only_fqdn(self):
        data = {'local_fqdn':'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_cetp/cetp_payload"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CETP_PAYLOAD Table with wrong parameters
    def test_insert_cetp_payload_incorrect_parameters(self):
        data = {'local_fqdn': 'test.gwa.d12312emo.', 'payload_type': 'e123th'}
        url = "http://127.0.0.1/API/host_cetp/cetp_payload"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CETP_PAYLOAD Table with correct parameters. Duplicate Policy
    def test_insert_cetp_payload_correct_parameters_duplicate(self):
        data = {'local_fqdn':'test.gwa.demo.', 'payload_type':'eth'}
        url = "http://127.0.0.1/API/host_cetp/cetp_payload"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)


    ##############################################################################################################


    # Inserting Policy in CETP_RLOC Table with correct parameters
    def test_insert_cetp_rloc_correct_parameters(self):
        data = {'local_fqdn':'test.gwa.demo.', 'rloc_type':'ipv4', 'value':'1.1.1.1'}
        url = "http://127.0.0.1/API/host_cetp/cetp_rloc"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CETP_RLOC Table with only fqdn. Incomplete parameters
    def test_insert_cetp_rloc_only_fqdn(self):
        data = {'local_fqdn':'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_cetp/cetp_rloc"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CETP_RLOC Table with wrong parameters
    def test_insert_cetp_rloc_incorrect_parameters(self):
        data = {'local_fqdn': 'test.gwa.d12312emo.', 'rloc_type': 'ipv123124'}
        url = "http://127.0.0.1/API/host_cetp/cetp_rloc"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CETP_RLOC Table with correct parameters. Duplicate
    def test_insert_cetp_rloc_correct_parameters_duplicate(self):
        data = {'local_fqdn':'test.gwa.demo.', 'rloc_type':'ipv4', 'value':'1.1.1.1'}
        url = "http://127.0.0.1/API/host_cetp/cetp_rloc"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)


    ##############################################################################################################


    # Inserting Policy in cetp_id Table with correct parameters
    def test_insert_cetp_id_correct_parameters(self):
        data = {'local_fqdn':'test.gwa.demo.', 'rloc_type':'ipv4', 'value':'1.1.1.1'}
        url = "http://127.0.0.1/API/host_cetp/cetp_id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in cetp_id Table with only fqdn. Incomplete parameters
    def test_insert_cetp_id_only_fqdn(self):
        data = {'local_fqdn':'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_cetp/cetp_id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in cetp_id Table with wrong parameters
    def test_insert_cetp_id_incorrect_parameters(self):
        data = {'local_fqdn': 'test.gwa.d12312emo.', 'rloc_type': 'ipv123124'}
        url = "http://127.0.0.1/API/host_cetp/cetp_id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in cetp_id Table with correct parameters. Duplicate
    def test_insert_cetp_id_correct_parameters_duplicate(self):
        data = {'local_fqdn':'test.gwa.demo.', 'rloc_type':'ipv4', 'value':'1.1.1.1'}
        url = "http://127.0.0.1/API/host_cetp/cetp_id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 608)



if __name__ == '__main__':
    unittest.main()







