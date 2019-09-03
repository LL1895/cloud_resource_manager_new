# -*- coding:UTF-8 -*-
import requests, time, sys, os
sys.path.append(os.path.abspath(os.path.dirname(os.getcwd())))
from core import get_token,logger
from conf import settings, protected

def get_pattern_status(key_word_list, str):
    for element in key_word_list:
        if element in str:
            return False
    return True

class RDS_MANAGEMENT:
    """关系型数据库类"""
    def __init__(self, project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "rds.%s.myhuaweicloud.com"  % url_project

    def get_api_version(self):
        url = "https://%s/rds/" % self.field_endpoint
        headers = {"X-Auth-Token": self.project_token}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('rds', '[RDS_MANAGEMENT][ERROR][%s]Get MRS api version return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('rds', '[RDS_MANAGEMENT][INFO][%s]Get MRS api version return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["versions"]

    def get_relation_rds_instance(self,api_version):
        url = "https://%s/rds/%s/%s/instances" % (self.field_endpoint,api_version, self.project_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json', "X-Language":"en-us"}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('rds', '[RDS_MANAGEMENT][ERROR][%s]Get MRS return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('rds', '[RDS_MANAGEMENT][INFO][%s]Get MRS return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["instances"]

    def delete_instance(self,api_version, instance_id, name):
        url = "https://%s/rds/%s/%s/instances/%s" % (self.field_endpoint,api_version, self.project_id, instance_id)
        headers = {"X-Auth-Token": self.project_token, 'Content-Type': 'application/json', "X-Language": "en-us"}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.accepted:
            logger.logger('rds','[RDS_MANAGEMENT][ERROR][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, instance_id, request_result.status_code))
        else:
            logger.logger('rds','[RDS_MANAGEMENT][INFO][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, instance_id, request_result.status_code))

    def get_delete_instance_id_dict(self, instance_list, delete_time, not_delete_key_word_list):
        instance_id_dict = {}
        for instance in instance_list:
            tmp_time_str = instance['created']
            create_stamp = time.mktime(time.strptime(tmp_time_str[0:tmp_time_str.index("+")], format("%Y-%m-%dT%H:%M:%S"))) + 28800
            DELETE_time = create_stamp + delete_time * 3600
            if instance["status"] == "ACTIVE" and instance["id"] not in protected.RDS and get_pattern_status(not_delete_key_word_list,instance["name"]) and time.time() > DELETE_time and instance["type"] != "slave":
                instance_id_dict[instance["id"]] = instance["name"]
        logger.logger('rds', '[RDS_MANAGEMENT][INFO][%s]get target rds info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

class RADIS_MANAGEMENT:
    """分布式缓存服务"""
    def __init__(self,project_id, project_tokens, url_project):
        self.project_token = project_tokens
        self.project_id = project_id
        self.url_project = url_project
        self.field_endpoint = "dcs.%s.myhuaweicloud.com"  % url_project

    def get_instance_list_static(self):
        url = "https://%s/v1.0/%s/instances/statistic" % (self.field_endpoint,self.project_id)
        headers = {"X-Auth-Token": self.project_token}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('rds', '[cloud_desktop][ERROR][%s]Get radis_static return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        logger.logger('rds', '[cloud_desktop][INFO][%s]Get radis_static return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
        return request_result.json()["statistics"]

    def get_instance_list(self):
        url = "https://%s/v1.0/%s/instances"  % (self.field_endpoint,self.project_id)
        headers = {"X-Auth-Token": self.project_token}
        request_result = requests.get(url=url, headers=headers)
        if request_result.status_code != requests.codes.ok:
            logger.logger('rds', '[RADIS_MANAGEMENT][ERROR][%s]Get RADIS return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), request_result.status_code))
            return False
        return request_result.json()["instances"]

    def delete_instance(self, instance_id,name):
        url = "https://%s/v1.0/%s/instances/%s" % (self.field_endpoint,self.project_id, instance_id)
        headers = {"X-Auth-Token": self.project_token}
        request_result = requests.delete(url=url, headers=headers)
        if request_result.status_code != requests.codes.no_content:
            logger.logger('rds','[RADIS_MANAGEMENT][ERROR][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, instance_id, request_result.status_code))
        else:
            logger.logger('rds','[RADIS_MANAGEMENT][INFO][%s]Delete %s[%s] return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), name, instance_id, request_result.status_code))

    def get_delete_instance_id_dict(self,instance_list, delete_time, not_delete_key_word_list):
        instance_id_dict = {}
        for instance in instance_list:
            tmp_time_str = instance['created_at']
            create_stamp = time.mktime(time.strptime(tmp_time_str[0:tmp_time_str.index(".")], format("%Y-%m-%dT%H:%M:%S"))) + 28800
            DELETE_time = create_stamp + delete_time * 3600
            if instance["instance_id"] not in protected.RADIS and get_pattern_status(not_delete_key_word_list,instance["name"]) and time.time() > DELETE_time:
                #instance["status"] == "RUNNING" and
                instance_id_dict[instance["instance_id"]] = instance["name"]
        logger.logger('rds', '[RADIS_MANAGEMENT][INFO][%s]get target radis info[%s].\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), instance_id_dict.keys()))
        return instance_id_dict

if __name__ == '__main__':
    pass
    # url_project = 'cn-north-1'
    # sub_project_id = '10a85dd37bac4e8abf6f6c349c7edfdd'
    #
    # token = get_token.get_token(settings.iam['domainname'], settings.iam['username'], settings.iam['password'],
    #                             url_project, url_project)
    #
    # rds_handler = RDS_MANAGEMENT(sub_project_id, token, url_project)
    # api_version =  rds_handler.get_api_version()[0]["id"]
    # print api_version
    # instance_list =  rds_handler.get_relation_rds_instance(api_version)
    # print instance_list
    # delete_rds_dict =  rds_handler.get_delete_instance_id_dict(instance_list, 0, "wushan")
    # print delete_rds_dict
    # for key,value in delete_rds_dict.items():
    #     print rds_handler.delete_instance(api_version, key, value)

    # radis_handle = RADIS_MANAGEMENT(sub_project_id, token, url_project)
    # radis_instance_list = radis_handle.get_instance_list()
    # print radis_instance_list
    # radis_finaly_dict = radis_handle.get_delete_instance_id_dict(radis_instance_list, 0, "wushan")
    # print radis_finaly_dict
    # for key,value in radis_finaly_dict:
    #     radis_handle.delete_instance(key, value)


