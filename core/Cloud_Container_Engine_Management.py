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

class CCE_MANAGEMENT:
    def __init__(self,project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "cce.%s.myhuaweicloud.com"  % url_project

    def get_cce_cluster_list(self):
        url = "https://%s/api/v3/projects/%s/clusters" % (self.field_endpoint, self.project_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('cce_log', '[CCE_MANAGEMENT][ERROR][%s]get CCE info return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('cce_log', '[CCE_MANAGEMENT][INFO][%s]get CCE info return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["items"]

    def get_delete_cce_id_dict(self,cce_id_list, delete_time, not_delete_key_word_list):
        instance_id_dict = {}
        for instance in cce_id_list:
            tmp_time_str = instance['metadata']["creationTimestamp"]
            create_stamp = time.mktime(time.strptime(tmp_time_str[0:tmp_time_str.index(".")], format("%Y-%m-%d %H:%M:%S"))) + 28800
            DELETE_time = create_stamp + delete_time * 3600
            if instance['metadata']["uid"] not in protected.CCE and get_pattern_status(not_delete_key_word_list,instance['metadata']["name"]) and time.time() > DELETE_time:
                #instance["status"]["phase"] == "Available" and 
                instance_id_dict[instance['metadata']["uid"]] = instance['metadata']["name"]
        logger.logger('cce_log', '[CCE_MANAGEMENT][INFO][%s]get target CCE info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

    def delete_cce_cluster(self,id, name):
        url = "https://%s/api/v3/projects/%s/clusters/%s" % (self.field_endpoint, self.project_id, id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('cce_log','[CCE_MANAGEMENT][ERROR][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name,id, request_result.status_code))
        else:
            logger.logger('cce_log','[CCE_MANAGEMENT][INFO][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name,id, request_result.status_code))


if __name__ == '__main__':
    # url_project = 'cn-east-2'
    # sub_project_id = 'e30de5f42aee4f8586b6ff28fe713422'
    #
    # token = get_token.get_token(settings.iam['domainname'], settings.iam['username'], settings.iam['password'],
    #                             url_project, url_project)
    # cce_handle = CCE_MANAGEMENT(sub_project_id, token, url_project)
    # cce_list = cce_handle.get_cce_cluster_list()
    # print cce_list
    # target_list = cce_handle.get_delete_cce_id_dict(cce_list, 0, "liliang")
    # print target_list
    # for key,value in target_list.items():
    #     cce_handle.delete_cce_cluster(key,value)
    pass

        