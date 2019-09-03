#!/usr/bin/env python
# Author:Zhangmingda
import  requests,time
from core import logger
def search_ecs(token,url_project,sub_project_id):
    url = 'https://ecs.{_project}.myhuaweicloud.com/v2/{tenant_id}/servers/detail'.format(_project=url_project,tenant_id=sub_project_id)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url,headers=headers)
    # print(r.json())
    try:
        r.json()['servers']
    except KeyError:
        logger.logger('search_ecs_error','%s  search ecs_liset Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []
    return r.json()['servers']

def search_publicips(token,url_project,sub_project_id):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v1/{tenant_id}/publicips'.format(_project=url_project,tenant_id=sub_project_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url,headers=headers)
    # print(r.json())
    try:
        r.json()['publicips']
    except KeyError:
        logger.logger('search_publicips_error','%s  search publicips_list Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []
    else:
        return r.json()['publicips']

# def search_bandwidth_charge_mode(token,url_project,sub_project_id,bandwidth_id):
#     # if url_project != ''
#     url = 'https://vpc.{_project}.myhuaweicloud.com/v1/{tenant_id}/bandwidths/{bandwidth_id}'.format(_project=url_project,tenant_id=sub_project_id,bandwidth_id=bandwidth_id)
#     # print(url)
#     headers = {"Content-type": "application/json", "X-Auth-Token": token}
#     r = requests.get(url=url, headers=headers)
#     # return r.json()
#     try:
#         r.json()['bandwidth']['charge_mode']
#     except KeyError :
#         return r.json()
#     else:
#         return r.json()['bandwidth']['charge_mode']
def search_port_owner(token,url_project,port_id):
    '''查询ACTIVE状态的IP的port所有者，判断是是不是NAT网关在用'''
    url = 'https://vpc.{_project}.myhuaweicloud.com/v1/ports/{_port_id}'.format(_project=url_project,_port_id=port_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url, headers=headers)
    try:
        device_owner= r.json()['port']['device_owner']
    except KeyError :
        logger.logger('search_port_owner_error','%s  search port_owner_liset Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return r.json()
    else:
        # print(r.json())
        return device_owner
    # return r.json()['bandwidth']['charge_mode']

def search_snat_rules(token,url_project):#,sub_project_id
    url = 'https://nat.{_project}.myhuaweicloud.com/v2.0/snat_rules'.format(_project=url_project)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url, headers=headers)
    # print(r.json())
    try :
        r.json()['snat_rules']
    except KeyError:
        logger.logger('search_snat_rules_error','%s  search search_snat_rules_liset Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []
    else:
      return r.json()['snat_rules']
def search_dnat_rules(token,url_project):#,sub_project_id
    url = 'https://nat.{_project}.myhuaweicloud.com/v2.0/dnat_rules'.format(_project=url_project)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url, headers=headers)
    try :
        r.json()['dnat_rules']
    except KeyError:
        logger.logger('search_dnat_rules_error','%s  search search_dnat_rules_liset Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []
    else:
      return r.json()['dnat_rules']
    # print(r.json())
def search_elb_list(token, url_project,sub_project_id):
    url = 'https://elb.{_project}.myhuaweicloud.com/v1.0/{tenant_id}/elbaas/loadbalancers'.format(_project=url_project,tenant_id=sub_project_id)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url,headers=headers)
    try:
        r.json()["loadbalancers"]
    except KeyError:
        logger.logger('search_elb_list_error','%s  search elb_liset Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []
    else:
        return r.json()["loadbalancers"]
def search_enhance_elb_list(token, url_project):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v2.0/lbaas/loadbalancers'.format(_project=url_project)
    print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url,headers=headers)
    try:
        r.json()["loadbalancers"]
    except KeyError:
        logger.logger('search_enhance_elb_list_error','%s  search enhance_elb_liset Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []
    else:
        return r.json()["loadbalancers"]

def search_elb_listeners(token, url_project,sub_project_id,loadbalancer_id):
    url = 'https://elb.{_project}.myhuaweicloud.com/v1.0/{tenant_id}/elbaas/listeners?loadbalancer_id={loadbalancer_id}'.format(_project=url_project,tenant_id=sub_project_id,loadbalancer_id=loadbalancer_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        logger.logger('search_elb_listeners_error', '%s  search elb_listeners Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []
def search_enhance_elb_listeners(token, url_project):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v2.0/lbaas/listeners'.format(_project=url_project)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        print(r.json()["listeners"])
        return r.json()["listeners"]
    else:
        logger.logger('search_elb_listeners_error', '%s  search elb_listeners Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []

def search_elb_listen_backend_ecs_list(token, url_project,sub_project_id,listener_id):
    url = 'https://elb.{_project}.myhuaweicloud.com/v1.0/{tenant_id}/elbaas/listeners/{listener_id}/members?limit=100'.format(_project=url_project,tenant_id=sub_project_id,listener_id=listener_id)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        logger.logger('search_elb_listen_backend_ecs_list_error', '%s  search elb_listener_backend_ecs Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []

def search_enhance_elb_healthmonitors(token, url_project):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v2.0/lbaas/healthmonitors'.format(_project=url_project) #GET
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.get(url=url,headers=headers)
    if r.status_code == 200:
        print(r.json()["healthmonitors"])
        return r.json()["healthmonitors"]
    else:
        logger.logger('search_enhance_elb_"healthmonitors"_error', '%s  search elb_listeners Failed  return_code:%s  info:%s url:%s:.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), r.status_code, r.json(), url))
        return []

# https://vpc.ap-sout
# heast-1.myhuaweicloud.com/v1/ccce0d1ed57e4621bce16ed18d8e8f71/publicips
# import os,sys,time
# BASE_NAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_NAME)
# from core import get_token
# from conf import settings
# token = get_token.get_token('hwcloudsom1', 'zhangmingda', '237828Zhang?','cn-north-1','cn-north-1')
# print(token)
# def search_user_id(token):
#     url = 'https://iam.myhuaweicloud.com/v3/users'
#     headers = {"Content-type": "application/json", "X-Auth-Token": token}
#     r = requests.get(url=url, headers=headers)
#     print(r.json())
# search_user_id(token)