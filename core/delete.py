#!/usr/bin/env python
# Author:Zhangmingda
import requests,time
from core import logger
def del_ecs(token,url_project,sub_project_id,ecs_id,ecs_name):
    '''调用v1接口批量删除云服务器'''
    url = 'https://ecs.{_project}.myhuaweicloud.com/v1/{tenant_id}/cloudservers/delete'.format(_project=url_project,tenant_id=sub_project_id)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    body ={
        "servers":[{"id": "%s"% ecs_id}],#DELETE_list,
        "delete_publicip": 'false',
        "delete_volume": 'false'
    }
    r = requests.post(url=url,json=body,headers=headers)
    if r.status_code == 200:
        logger.logger('delete_ecs','%s  ECS %s Delete Successful result:%s return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), ecs_name, r.json(),r.status_code))
    else:
        logger.logger('delete_ecs_err', '%s  ECS %s Delete Failed:%s return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), ecs_name, r.json(), r.status_code))

def del_publicip(token,url_project,sub_project_id,publicip_id,ipaddress):
    '''调用V1接口删除单个IP地址'''
    url = 'https://vpc.{_project}.myhuaweicloud.com/v1/{tenant_id}/publicips/{publicip_id}'.format(_project=url_project,tenant_id=sub_project_id,publicip_id=publicip_id)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url,headers=headers)
    if r.status_code == 204 :
        logger.logger('del_publicip','%s  publicip %s delete Successful  return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), ipaddress,r.status_code))
    else:
        logger.logger('del_publicip_err', '%s  publicip %s delete Failed_info:%s return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), ipaddress,r.json(), r.status_code))
    # print('print del_publicip r.json():',r.json())
    # return r.status_code

def del_snat_rule(token,url_project,snat_rule_id,nat_ipaddress):
    url = 'https://nat.{_project}.myhuaweicloud.com/v2.0/snat_rules/{_snat_rule_id}'.format(_project=url_project,_snat_rule_id=snat_rule_id) #DELETE
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url, headers=headers)
    if r.status_code == 204:
        logger.logger('del_snat_rule','%s  delete snat_rules_ip: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), nat_ipaddress, r.status_code))
    else:
        logger.logger('del_snat_rule_err', '%s  delete snat_rules_ip: %s Failed info:%s return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), nat_ipaddress,r.json(), r.status_code))

def del_dnat_rule(token,url_project,dnat_rule_id,nat_ipaddress):
    url = 'https://nat.{_project}.myhuaweicloud.com/v2.0/dnat_rules/{_dnat_rule_id}'.format(_project=url_project,_dnat_rule_id=dnat_rule_id) #DELETE
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url, headers=headers)
    if r.status_code == 204:
        logger.logger('del_dnat_rule','%s  delete dnat_rules_ip: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), nat_ipaddress, r.status_code))
    else:
        logger.logger('del_dnat_rule_err', '%s  delete dnat_rules_ip: %s Failed info:%s return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), nat_ipaddress,r.json(), r.status_code))
    #
    # logger.logger('del_dnat_rule', '%s  delete dnat_rules_ip: %s info:%s return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), nat_ipaddress, r.json(), r.status_code))
    # # return r.status_code


def del_elb(token,url_project,sub_project_id,loadbalancer_id,vip_address):
    url = 'https://elb.{_project}.myhuaweicloud.com/v1.0/{tenant_id}/elbaas/loadbalancers/{loadbalancer_id}'.format(_project=url_project,tenant_id=sub_project_id,loadbalancer_id=loadbalancer_id)
    # print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url, headers=headers)
    if r.status_code == 200:
        logger.logger('del_elb', '%s  delete elb_vip_address: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), vip_address, r.status_code))
        return r.status_code
    else:
        logger.logger('del_elb_err', '%s  delete elb_vip_address: %s Failed return_code:%s info:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), vip_address, r.status_code,r.json()))
        return 
def del_enhance_elb(token,url_project,loadbalancer_id,vip_address):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v2.0/lbaas/loadbalancers/{loadbalancer_id}'.format(_project=url_project,loadbalancer_id=loadbalancer_id)
    print(url)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url, headers=headers)
    if r.status_code == 204:
        logger.logger('del_enhance_elb', '%s  delete elb_vip_address: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), vip_address, r.status_code))
    else:
        logger.logger('del_enhance_elb_err', '%s  delete enhance_elb_vip_address: %s Failed return_code:%s info:%s url:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), vip_address, r.status_code,r.json(),url))

def remove_elb_listener_ecs(token,url_project,sub_project_id,listener_id,backend_ecs):
    url = 'https://elb.{_project}.myhuaweicloud.com/v1.0/{tenant_id}/elbaas/listeners/{listener_id}/members/action'.format(_project=url_project,tenant_id=sub_project_id,listener_id=listener_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    body = {"removeMember": [{"id": "%s"% backend_ecs['id']}]}
    # print(body)
    r = requests.post(url=url,json=body,headers=headers)
    if r.status_code == 200:
        logger.logger('remove_elb_listener_ecs', '%s  remove_elb_listener_ecs: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), backend_ecs['server_address'], r.status_code))
    else:
        logger.logger('remove_elb_listener_ecs_err','%s  remove_elb_listener_ecs:  %s Failed return_code:%s info:%s url:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), backend_ecs['server_address'], r.status_code, r.json(), url))

def del_enhance_elb_listeners(token, url_project,listener_id):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v2.0/lbaas/listeners/{listener_id}'.format(_project=url_project,listener_id=listener_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url,headers=headers)
    print(r.status_code)
    if r.status_code == 204:
        logger.logger('del_enhance_elb_listeners', '%s  delete del_enhance_elb_listeners: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), listener_id, r.status_code))
    else:
        logger.logger('del_enhance_elb_listeners_err', '%s  delete del_enhance_elb_listeners: %s Failed return_code:%s info:%s url:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), listener_id, r.status_code,r.json(),url))
def del_enhance_elb_listener_backend_pool(token, url_project,pool_id):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v2.0/lbaas/pools/{pool_id}'.format(_project=url_project,pool_id=pool_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url,headers=headers)
    print(r.status_code)
    if r.status_code == 204:
        logger.logger('del_enhance_elb_listener_backend_pool', '%s  delete del_listener_backend_pool: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), pool_id, r.status_code))
    else:
        logger.logger('del_enhance_elb_listener_backend_pool_err', '%s  delete del_listener_backend_pool: %s Failed return_code:%s info:%s url:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), pool_id, r.status_code,r.json(),url))
def del_enhance_elb_healthmonitor(token, url_project,healthmonitor_id):
    url = 'https://vpc.{_project}.myhuaweicloud.com/v2.0/lbaas/healthmonitors/{healthmonitor_id}'.format(_project=url_project,healthmonitor_id=healthmonitor_id)
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.delete(url=url, headers=headers)
    if r.status_code == 204:
        logger.logger('del_enhance_elb_healthmonitor', '%s  del_enhance_elb_healthmonitor: %s Successful return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), healthmonitor_id, r.status_code))
    else:
        logger.logger('del_enhance_elb_healthmonitor_err', '%s  delete del_listener_backend_pool: %s Failed return_code:%s info:%s url:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), healthmonitor_id, r.status_code,r.json(),url))
