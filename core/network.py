# -*- coding:UTF-8 -*-
import requests, time, json, sys, os
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from core import get_token, logger
from conf import settings, protected

def get_pattern_status(key_word_list, str):
    for element in key_word_list:
        if element in str:
            return False
    return True

class NAT_MANAGEMENT:
    def __init__(self,project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "nat.%s.myhuaweicloud.com"  % url_project

    def get_nat_list(self):
        url = "https://%s/v2.0/nat_gateways" % (self.field_endpoint)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('network', '[NAT_MANAGEMENT][ERROR][%s]Get nat return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('network', '[NAT_MANAGEMENT][INFO][%s]Get nat return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["nat_gateways"]

    def get_delete_nat_id_dict(self,nat_id_list, delete_time, not_delete_key_word_list):
        instance_id_dict = {}
        for instance in nat_id_list:
            tmp_time_str = instance['created_at']
            create_stamp = time.mktime(time.strptime(tmp_time_str[0:tmp_time_str.index(".")], format("%Y-%m-%d %H:%M:%S"))) + 28800
            DELETE_time = create_stamp + delete_time * 3600
            if instance["id"] not in protected.NAT and get_pattern_status(not_delete_key_word_list,instance["name"]) and time.time() > DELETE_time:
                instance_id_dict[instance['id']] = instance['name']
        logger.logger('network', '[NAT_MANAGEMENT][INFO][%s]get target nat info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

    def delete_nat_id(self, nat_gateway_id,name):
        snat_rule_list = self.get_snat_list()
        if snat_rule_list is not False and snat_rule_list is not None:
            for element in snat_rule_list:
                self.delete_snat_rule(element["id"])
        dnat_rule_list = self.get_dnat_list()
        if dnat_rule_list is not False and snat_rule_list is not None:
            for element in dnat_rule_list:
                self.delete_dnat_rule(element["id"])
        url = "https://%s/v2.0/nat_gateways/%s" % (self.field_endpoint, nat_gateway_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.no_content:
            logger.logger('network','[NAT_MANAGEMENT][ERROR][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"),name, nat_gateway_id, request_result.status_code))
        else:
            logger.logger('network','[NAT_MANAGEMENT][INFO][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"),name, nat_gateway_id, request_result.status_code))

    def get_snat_list(self):
        url = "https://%s/v2.0/snat_rules"  % (self.field_endpoint)
        headers = {"X-Auth-Token": self.project_token}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('network', '[NAT_MANAGEMENT][ERROR][%s]Get snat rule return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('network', '[NAT_MANAGEMENT][INFO][%s]Get snat return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["snat_rules"]

    def delete_snat_rule(self,snat_rule_id):
        url = "https://%s/v2.0/snat_rules/%s" % (self.field_endpoint, snat_rule_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.no_content:
            logger.logger('network', '[NAT_MANAGEMENT][ERROR][%s]Delete snat rule[%s] return_code:%s.\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S"), snat_rule_id, request_result.status_code))
        else:
            logger.logger('network', '[NAT_MANAGEMENT][INFO][%s]Delete snat rule[%s] return_code:%s.\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S"), snat_rule_id, request_result.status_code))

    def get_dnat_list(self):
        url = "https://%s/v2.0/dnat_rules"  % (self.field_endpoint)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('network', '[NAT_MANAGEMENT][ERROR][%s]Get dnat rulel return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('network', '[NAT_MANAGEMENT][INFO][%s]Get dnat return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["dnat_rules"]

    def delete_dnat_rule(self,dnat_rule_id):
        url = "https://%s/v2.0/dnat_rules/%s" % (self.field_endpoint, dnat_rule_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.no_content:
            logger.logger('network', '[NAT_MANAGEMENT][ERROR][%s]Delete dnat rule[%s] return_code:%s.\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S"), dnat_rule_id, request_result.status_code))
        else:
            logger.logger('network', '[NAT_MANAGEMENT][INFO][%s]Delete dnat rule[%s] return_code:%s.\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S"), dnat_rule_id, request_result.status_code))


if __name__ == '__main__':
    pass
    # url_project = 'cn-north-1'
    # sub_project_id = '10a85dd37bac4e8abf6f6c349c7edfdd'
    #
    # token = get_token.get_token(settings.iam['domainname'], settings.iam['username'], settings.iam['password'],
    #                             url_project, url_project)
    # nat_handle = NAT_MANAGEMENT(sub_project_id, token, url_project)
    # nat_list = nat_handle.get_nat_list()
    # print nat_list
    # target_list = nat_handle.get_delete_nat_id_dict(nat_list, 0, "uuu")
    # print target_list
    # for key,value in target_list.items():
    #     nat_handle.delete_nat_id(key, value)
