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

class MRS_MANAGEMENT:
    def __init__(self,project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "mrs.%s.myhuaweicloud.com"  % url_project

    def get_instance_list(self):
        url = "https://%s/v1.1/%s/cluster_infos"  % (self.field_endpoint,self.project_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('EI', '[MRS_MANAGEMENT][ERROR][%s]Get MRS return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('EI', '[MRS_MANAGEMENT][INFO][%s]Get MRS return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["clusters"]

    def get_stop_rds_instance_dict(self, mrs_list, stop_time, not_delete_key_word_list):
        instance_id_dict = {}
        for element in mrs_list:
            tmp_time_stap = int(element["createAt"])
            if tmp_time_stap is not None:
                DELETE_time = tmp_time_stap + stop_time * 3600
                if element["clusterState"] == "running" and element["clusterId"] not in protected.MRS and get_pattern_status(not_delete_key_word_list,element["clusterName"]) and time.time() > DELETE_time:
                    #element["clusterState"] == "running" and  
                    instance_id_dict[element["clusterId"]] = element["clusterName"]
        logger.logger('EI', '[MRS_MANAGEMENT][INFO][%s]get target MRS info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

    def stop_instance(self, cluster_id, name):
        url = "https://%s/v1.1/%s/clusters/%s" % (self.field_endpoint,self.project_id, cluster_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.no_content:
            logger.logger('EI','[MRS_MANAGEMENT][ERROR][%s]Stop %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, cluster_id, request_result.status_code))
        else:
            logger.logger('EI','[MRS_MANAGEMENT][INFO][%s]Stop %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, cluster_id, request_result.status_code))

class DWS_MANAGEMENT:
    def __init__(self,project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "dws.%s.myhuaweicloud.com"  % url_project

    def get_instance_list(self):
        url = "https://%s/v1.0/%s/clusters" % (self.field_endpoint, self.project_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('EI', '[DWS][ERROR][%s]Get MRS return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('EI', '[DWS][INFO][%s]Get MRS return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["clusters"]

    def delete_instance(self,cluster_id, name):
        url = "https://%s/v1.0/%s/clusters/%s" % (self.field_endpoint, self.project_id, cluster_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json'}
        body = {"keep_last_manual_snapshot":0}
        request_result = requests.delete(url=url, headers=headers, data=json.dumps(body))
        if request_result.status_code != requests.codes.accepted:
            logger.logger('EI','[DWS][ERROR][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, cluster_id, request_result.status_code))
        else:
            logger.logger('EI','[DWS][INFO][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, cluster_id, request_result.status_code))


    def get_delete_cluster_list(self,dws_list, delete_time, not_delete_key_word_list):
        instance_id_dict = {}
        for element in dws_list:
            tmp_time_str = element["created"]
            if tmp_time_str is not None:
                create_stamp = time.mktime(time.strptime(tmp_time_str, format("%Y-%m-%dT%H:%M:%S"))) + 28800
                DELETE_time = create_stamp + delete_time * 3600
                if element["status"] == "AVAILABLE" and element["id"] not in protected.DWS and get_pattern_status(not_delete_key_word_list,element["name"]) and time.time() > DELETE_time:
                    instance_id_dict[element["id"]] = element["name"]
        logger.logger('EI', '[DWS][INFO][%s]get target DWS info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

if __name__ == '__main__':
    pass
    # url_project = 'cn-north-1'
    # sub_project_id = '10a85dd37bac4e8abf6f6c349c7edfdd'
    #
    # token = get_token.get_token(settings.iam['domainname'], settings.iam['username'], settings.iam['password'],
    #                             url_project, url_project)
    # '''
    # mrs_handle = MRS_MANAGEMENT(sub_project_id, token, url_project)
    # mrs_list = mrs_handle.get_instance_list()
    # print mrs_list
    # yy = mrs_handle.get_stop_rds_instance_dict(mrs_list, 0, "dfdfd")
    # print yy
    # for key,value in yy.items():
    #     print mrs_handle.stop_instance(key, value)
    # '''
    # dws_handle = DWS_MANAGEMENT(sub_project_id, token, url_project)
    # dws_list =  dws_handle.get_instance_list()
    # print(dws_list)
    # target_list = dws_handle.get_delete_cluster_list(dws_list, 0, "aaaaaaaaaaaa")
    # print(target_list)
    # for key,value in target_list.items():
    #     dws_handle.delete_instance(key, value)