#!/usr/bin/env python
# Author:Zhangmingda
import requests,json,time
from core import logger
def poweoff_ecs(token,url_project,sub_project_id,SHUT_list):
    # print(SHUT_list['id_dict']) #SHUTOFF_list['id']
    '''调用V1接口批量关机云服务器'''
    url = 'https://ecs.{_project}.myhuaweicloud.com/v1/{tenant_id}/cloudservers/action'.format(_project=url_project,tenant_id=sub_project_id)
    body = {
        "os-stop": {
            "type": "HARD",
            "servers": SHUT_list['id_dict']
        }
    }
    headers = {"Content-type": "application/json", "X-Auth-Token": token}
    r = requests.post(url,json=body,headers=headers)
    logger.logger('shut_off_ecs','%s   ECS: %s Shut Off!  result:%s return_code:%s.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), SHUT_list['ecs_name'], r.json(),r.status_code))