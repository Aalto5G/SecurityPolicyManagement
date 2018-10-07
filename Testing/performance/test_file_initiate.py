import unittest
import requests, json, time



class TestStringMethods(unittest.TestCase):



    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   INSERT ID in HOST POLICIES


    # Inserting Policy in ID Table, host_negotiation table with correct parameters
    def test_insert_id_correct_parameters(self):
        data = {'fqdn':'test.gwa.demo.', 'msisdn':'0000000100', 'ipv4':'192.168.0.100'}
        url = "http://127.0.0.1/API/host_policy/id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)

        self.aaatest_insert_cetp_negotiations_correct_parameters()
        self.aaatest_insert_cetp_negotiations_only_fqdn()


    # Inserting Policy in ID Table with only fqdn
    def test_insert_id_only_fqdn_parameters(self):
        data = {'fqdn':'test2.gwa.demo.'}
        url = "http://127.0.0.1/API/host_policy/id"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)

###############################################################################
    ###############################################################################
    ###############################################################################
    #   INSERT CETP POLICIES


    # Inserting Policy in CETP_NEGOTIATIONS Table with correct parameter
    def aaatest_insert_cetp_negotiations_correct_parameters(self):
        data = {'local_fqdn':'test.gwa.demo.', 'direction':'EGREss'}
        url = "http://127.0.0.1/API/host_cetp/cetp_negotiations"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


    # Inserting Policy in CETP_NEGOTIATIONS Table with only fqdn. Incomplete parameters
    def aaatest_insert_cetp_negotiations_only_fqdn(self):
        data = {'local_fqdn':'test.gwa.demo.'}
        url = "http://127.0.0.1/API/host_cetp/cetp_negotiations"
        data = requests.post(url, data=json.dumps(data))
        self.assertEqual(data.status_code, 200)


if __name__ == '__main__':
    unittest.main()










