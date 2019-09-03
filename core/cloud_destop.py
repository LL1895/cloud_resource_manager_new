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

class CD_MANAGEMENT:
    def __init__(self,project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "workspace.%s.myhuaweicloud.com"  % url_project

    def get_cloud_destop_list(self):
        url = "https://%s/v1.0/%s/desktops" % (self.field_endpoint, self.project_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('cloud_desktop', '[CD_MANAGEMENT][ERROR][%s]Get cloud_desktop return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('cloud_desktop', '[CD_MANAGEMENT][INFO][%s]Get cloud_desktop return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["desktops"]

    def get_delete_cd_id_dict(self,cd_id_list, delete_time, not_delete_key_word_list):
        instance_id_dict = {}
        for instance in cd_id_list:
            tmp_time_str = instance['created']
            create_stamp = time.mktime(time.strptime(tmp_time_str[0:tmp_time_str.index(".")], format("%Y-%m-%dT%H:%M:%S"))) + 28800
            DELETE_time = create_stamp + delete_time * 3600
            if instance["desktop_id"] not in protected.CD and get_pattern_status(not_delete_key_word_list,instance["computer_name"]) and time.time() > DELETE_time:
                instance_id_dict[instance['desktop_id']] = instance['computer_name']
        logger.logger('cloud_desktop', '[CD_MANAGEMENT][INFO][%s]get target cloud_desktop info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

    def delete_cd_id(self, desktop_id, name):
        url = "https://%s/v1.0/%s/desktops/%s" % (self.field_endpoint, self.project_id, desktop_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.no_content:
            logger.logger('cloud_desktop','[CD_MANAGEMENT][ERROR][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, desktop_id, request_result.status_code))
        else:
            logger.logger('cloud_desktop','[CD_MANAGEMENT][INFO][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, desktop_id, request_result.status_code))


if __name__ == '__main__':
    pass
    # url_project = 'cn-north-1'
    # sub_project_id = '10a85dd37bac4e8abf6f6c349c7edfdd'
    #
    # token = get_token.get_token(settings.iam['domainname'], settings.iam['username'], settings.iam['password'],
    #                             url_project, url_project)
    # cd_handle = CD_MANAGEMENT(sub_project_id, token, url_project)
    # cd_list = cd_handle.get_cloud_destop_list()
    # print cd_list
    # target_list = cd_handle.get_delete_cd_id_dict(cd_list, 0, "ddddddddddd")
    # print target_list
    # for key,value in target_list.items():
    #     cd_handle.delete_cd_id(key,value)