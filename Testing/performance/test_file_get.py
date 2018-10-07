import unittest
import requests, json, time



class TestStringMethods(unittest.TestCase):


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   Get all policies of host tables and single policy of host tables


    # Getting all policies of Firewall Table
    def test_get_table_Firewall(self):
        url="http://127.0.0.1/API/host_policy/FIREWALL"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)

    # Getting all policies of SFQDN Table
    def test_get_table_SFQDN(self):
        url="http://127.0.0.1/API/host_policy/SFQDN"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)

    # Getting all policies of CIRCULARPOOL Table
    def test_get_table_CIRCULARPOOL(self):
        url="http://127.0.0.1/API/host_policy/CIRCULARPOOL"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of CARRIERGRADE Table
    def test_get_table_CARRIERGRADE(self):
        url="http://127.0.0.1/API/host_policy/CARRIERGRADE"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of ID Table
    def test_get_table_ID(self):
        url = "http://127.0.0.1/API/host_policy/ID"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of Table with random table name
    def test_get_policies_wrong_table_name(self):
        url="http://127.0.0.1/API/host_policy/adfgafgasdf"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    # Getting policies with random wrong url
    def test_get_policies_wrong_URL(self):
        url="http://127.0.0.1/testing/"
        data = requests.get(url)
        self.assertEqual(data.status_code, 404)


    # Getting single policy with ID in Firewall Table
    def test_get_table_Firewall_instance(self):
        url = "http://127.0.0.1/API/host_policy/FIREWALL/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policy with ID in SFQDN Table
    def test_get_table_SFQDN_instance(self):
        url = "http://127.0.0.1/API/host_policy/SFQDN/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policy with ID in CIRCULARPOOL Table
    def test_get_table_CIRCULARPOOL_instance(self):
        url = "http://127.0.0.1/API/host_policy/CIRCULARPOOL/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policy with ID in CARRIERGRADE Table
    def test_get_table_CARRIERGRADE_instance(self):
        url = "http://127.0.0.1/API/host_policy/CARRIERGRADE/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policy with ID in ID Table
    def test_get_table_ID_instance(self):
        url = "http://127.0.0.1/API/host_policy/ID/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   Get all policies of cetp tables and single policy of cetp tables


    # Getting all policies of CETP_AVAILABLE Table
    def test_get_table_CETP_AVAILABLE(self):
        url = "http://127.0.0.1/API/host_cetp/available"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of CETP_OFFERED Table
    def test_get_table_CETP_OFFERED(self):
        url = "http://127.0.0.1/API/host_cetp/request"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)



    # Getting all policies of CETP_REQUIRED Table
    def test_get_table_CETP_REQUIRED(self):
        url = "http://127.0.0.1/API/host_cetp/offer"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of cetp_negotiations Table
    def test_get_table_cetp_negotiations(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_negotiations"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of cetp_id Table
    def test_get_table_cetp_id(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_id"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of cetp_payload Table
    def test_get_table_cetp_payload(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_payload"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of cetp_rloc Table
    def test_get_table_cetp_rloc(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_rloc"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of cetp_control_params Table
    def test_get_table_cetp_control_params(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_control_params"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of Table with random table name
    def test_get_cetp_policies_wrong_table_name(self):
        url = "http://127.0.0.1/API/host_cetp/hga34trwe"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    # Getting single policies of CETP_AVAILABLE Table
    def test_get_table_CETP_AVAILABLE_instance(self):
        url = "http://127.0.0.1/API/host_cetp/available/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of CETP_OFFERED Table
    def test_get_table_CETP_OFFERED_instance(self):
        url = "http://127.0.0.1/API/host_cetp/request/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of CETP_REQUIRED Table
    def test_get_table_CETP_REQUIRED_instance(self):
        url = "http://127.0.0.1/API/host_cetp/offer/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of cetp_negotiations Table
    def test_get_table_cetp_negotiations_instance(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_negotiations/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of cetp_id Table
    def test_get_table_cetp_id_instance(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_id/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of cetp_payload Table
    def test_get_table_cetp_payload_instance(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_payload/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of cetp_rloc Table
    def test_get_table_cetp_rloc_instance(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_rloc/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of cetp_control_params Table
    def test_get_table_cetp_control_params_instance(self):
        url = "http://127.0.0.1/API/host_cetp/cetp_control_params/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   Get all policies of ces tables and single policy of ces tables


    # Getting all policies of Table with random table name
    def test_get_ces_policies_wrong_table_name(self):
        url = "http://127.0.0.1/API/host_ces/hga34trwe"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    # Getting all policies of CES_AVAILABLE Table
    def test_get_table_CES_AVAILABLE(self):
        url = "http://127.0.0.1/API/host_ces/available"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of CES_OFFERED Table
    def test_get_table_CES_OFFERES(self):
        url = "http://127.0.0.1/API/host_ces/offer"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of CES_REQUIRED Table
    def test_get_table_CES_REQUIRED(self):
        url = "http://127.0.0.1/API/host_ces/request"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of ces_negotiations Table
    def test_get_table_ces_negotiations(self):
        url = "http://127.0.0.1/API/host_ces/ces_negotiations"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all policies of ces_params Table
    def test_get_table_ces_params(self):
        url = "http://127.0.0.1/API/host_ces/ces_params"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of CES_AVAILABLE Table
    def test_get_table_CES_AVAILABLE_instance(self):
        url = "http://127.0.0.1/API/host_ces/available/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of CES_OFFERED Table
    def test_get_table_CES_OFFERES_instance(self):
        url = "http://127.0.0.1/API/host_ces/offer/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of CES_REQUIRED Table
    def test_get_table_CES_REQUIRED_instance(self):
        url = "http://127.0.0.1/API/host_ces/request/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of ces_negotiations Table
    def test_get_table_ces_negotiations_instance(self):
        url = "http://127.0.0.1/API/host_ces/ces_negotiations/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policies of ces_params Table
    def test_get_table_ces_params_instance(self):
        url = "http://127.0.0.1/API/host_ces/ces_params/2"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   Get HOST POLICIES of USER using different parameters


    # Getting all policies of a user using fqdn
    def test_get_all_user_policies(self):
        url = "http://127.0.0.1/API/host_policy_user/fqdn/test1.aalto.fi"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)
        print ('hassaanuah')


    # Getting single type policies of a user using fqdn
    def test_get_single_type_user_policies(self):
        url = "http://127.0.0.1/API/host_policy_user/fqdn/test1.aalto.fi?policy_name=firewall"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting Multiple type policies of a user using fqdn
    def test_get_multiple_type_user_policies(self):
        url = "http://127.0.0.1/API/host_policy_user/fqdn/test1.aalto.fi?policy_name=id,sfqdn,circularpool"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting policies with wrong tablename
    def test_get_wrong_policyname_user_policies(self):
        url = "http://127.0.0.1/API/host_policy_user/fqdn/test1.aalto.fi?policy_name=id,45612d"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    # Getting policies with wrong id type. Using fqqddnn instead of fqdn
    def test_get_wrong_fqdn_user_policies(self):
        url = "http://127.0.0.1/API/host_policy_user/fqqddnn/abcabcabc?policy_name=id"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   Get CETP POLICIES of USER using different parameters


    # Getting all policies of a user using fqdn
    def test_get_all_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cetp_user?lfqdn=hosta1.cesa.lte.&direction=EGRESS"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single type policies of a user using fqdn
    def test_get_single_type_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cetp_user?lfqdn=hosta1.cesa.lte.&direction=EGRESS&policy_name=available"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting Multiple type policies of a user using fqdn
    def test_get_multiple_type_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cetp_user?lfqdn=hosta1.cesa.lte.&direction=EGRESS&policy_name=available,request"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting policies with wrong tablename
    def test_get_wrong_policyname_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cetp_user?lfqdn=hosta1.cesa.lte.&direction=EGRESS&policy_name=123123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    # Getting policies with wrong direction
    def test_get_wrong_direction_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cetp_user?lfqdn=hosta1.cesa.lte.&direction=123123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 602)


    # Getting policies with wrong URL
    def test_get_wrong_url_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cet12121p_user?lfqdn=hosta1.cesa.lte.&direction=123123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 404)


    # Getting policies with wrong variable
    def test_get_wrong_variable_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cetp_user?lfq12dn=123123123&dir12ection=123123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 602)


    # Getting policies without any parameter
    def test_get_without_parameter_user_cetp_policies(self):
        url = "http://127.0.0.1/API/host_cetp_user"
        data = requests.get(url)
        self.assertEqual(data.status_code, 602)


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   Get CES POLICIES using different parameters


    # Getting all policies of a user using fqdn
    def test_get_all_ces_policies(self):
        url = "http://127.0.0.1/API/host_ces_node?protocol=tls&link_alias=*&dest_ces=cesa.lte.&direction=*"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single type policies of a user using fqdn
    def test_get_single_type_ces_policies(self):
        url = "http://127.0.0.1/API/host_ces_node?protocol=tls&link_alias=*&dest_ces=cesa.lte.&policy_name=available"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting Multiple type policies of a user using fqdn
    def test_get_multiple_type_ces_policies(self):
        url = "http://127.0.0.1/API/host_ces_node?protocol=tls&link_alias=*&dest_ces=cesa.lte.&policy_name=request,offer"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting policies with wrong tablename
    def test_get_wrong_policyname_ces_policies(self):
        url = "http://127.0.0.1/API/host_ces_node?protocol=tls&link_alias=*&dest_ces=cesa.lte.&policy_name=123123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    # Getting policies with wrong direction
    def test_get_wrong_direction_ces_policies(self):
        url = "http://127.0.0.1/API/host_ces_node?protocol=tls&link_alias=*&dest_ces=cesa.lte.&direction=12123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 602)


    # Getting policies with wrong URL
    def test_get_wrong_url_ces_policies(self):
        url = "http://127.0.0.1/API/host_112321ces_node?protocol=tls&link_alias=*&dest_ces=cesa.lte.&direction=12123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 404)


    # Getting policies with wrong variable
    def test_get_wrong_variable_ces_policies(self):
        url = "http://127.0.0.1/API/host_ces_node?protoc321ol=tls&lin12312k_alias=*&des321t_ces=cesa.lte."
        data = requests.get(url)
        self.assertEqual(data.status_code, 602)


    # Getting policies without any parameter
    def test_get_without_parameter_ces_policies(self):
        url = "http://127.0.0.1/API/host_ces_node"
        data = requests.get(url)
        self.assertEqual(data.status_code, 602)


    ###############################################################################
    ###############################################################################
    ###############################################################################
    #   Get Bootstrap policies. Either full or a single row


    # Getting all policies of bootstrap table with formatting
    def test_get_all_bootstrap_policies(self):
        url = "http://127.0.0.1/API/host_bootstrap"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policy from bootstrap Table
    def test_get_single_bootstrap_policy(self):
        url = "http://127.0.0.1/API/host_bootstrap/550"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting single policy from bootstrap Table using a variable as ID
    def test_get_single_bootstrap_using_wrong_id(self):
        url = "http://127.0.0.1/API/host_bootstrap/abc"
        data = requests.get(url)
        self.assertEqual(data.status_code, 607)


    # Getting all policies of bootstrap table without formatting
    def test_get_all_bootstrap_noformatting_policies(self):
        url = "http://127.0.0.1/API/host_bootstrap_all"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all bootstrap policies of single type
    def test_get_all_bootstrap_policies_one_type(self):
        url = "http://127.0.0.1/API/host_bootstrap?name=IPTABLES"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all bootstrap policies of single type with wrong type
    def test_get_all_bootstrap_policies_wrong_type(self):
        url = "http://127.0.0.1/API/host_bootstrap?name=123123123"
        data = requests.get(url)
        self.assertEqual(data.status_code, 601)


    # Getting all bootstrap policies of single type with wrong variable
    def test_get_all_bootstrap_policies_wrong_variable(self):
        url = "http://127.0.0.1/API/host_bootstrap?nam1e=IPTABLES"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)


    # Getting all bootstrap policies of multip[e types
    def test_get_all_bootstrap_policies_multiple_types(self):
        url = "http://127.0.0.1/API/host_bootstrap?nam1e=IPTABLES,CIRCULARPOOL"
        data = requests.get(url)
        self.assertEqual(data.status_code, 200)





if __name__ == '__main__':
    unittest.main()










