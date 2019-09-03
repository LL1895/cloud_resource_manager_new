# -*- coding:UTF-8 -*-
import requests, time, json, sys, os
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from core import get_token,logger
from conf import settings, protected

def get_pattern_status(key_word_list, str):
    for element in key_word_list:
        if element in str:
            return False
    return True

class EVS_MANAGEMENT:
    def __init__(self,project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "evs.%s.myhuaweicloud.com"  % url_project

    def get_evs_list(self):
        url = "https://%s/v2/%s/volumes/detail?status=available" % (self.field_endpoint, self.project_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('storage', '[EVS_MANAGEMENT][ERROR][%s]Get EVS api version return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('storage', '[EVS_MANAGEMENT][INFO][%s]Get EVS api version return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["volumes"]

    def get_delete_evs_id_dict(self,evs_id_list, delete_time, not_delete_key_word_list):
        instance_id_dict = {}
        for instance in evs_id_list:
            tmp_time_str = instance['created_at']
            create_stamp = time.mktime(time.strptime(tmp_time_str[0:tmp_time_str.index(".")], format("%Y-%m-%dT%H:%M:%S"))) + 28800
            DELETE_time = create_stamp + delete_time * 3600
            if instance["id"] not in protected.EVS and get_pattern_status(not_delete_key_word_list,instance["name"]) and time.time() > DELETE_time:
                instance_id_dict[instance['id']] = instance['name']
        logger.logger('storage', '[EVS_MANAGEMENT][INFO][%s]get target EVS info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

    def delete_evs_id(self,evs_id,name):
        url = "https://%s/v2/%s/volumes/%s?cascade=true" % (self.field_endpoint, self.project_id, evs_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.accepted:
            logger.logger('storage','[EVS_MANAGEMENT][ERROR][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, evs_id, request_result.status_code))
        else:
            logger.logger('storage','[EVS_MANAGEMENT][INFO][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, evs_id, request_result.status_code))

if __name__ == '__main__':
    pass
    # url_project = 'cn-north-1'
    # sub_project_id = '10a85dd37bac4e8abf6f6c349c7edfdd'
    #
    # token = get_token.get_token(settings.iam['domainname'], settings.iam['username'], settings.iam['password'],
    #                             url_project, url_project)
    # evs_handle = EVS_MANAGEMENT(sub_project_id, token, url_project)
    # evs_list = evs_handle.get_evs_list()
    # print evs_list
    # target_list = evs_handle.get_delete_evs_id_dict(evs_list, "liliang")
    # print target_list
    # for key,value in target_list.items():
    #     evs_handle.delete_evs_id(key,value)