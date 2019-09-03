#!/usr/bin/env python
# Author:Zhangmingda
import requests,time
from core import logger

def smn(token,url_project,sub_project_id,phone_list,message):
    '''调用smn接口发送短信，可以批量发送，传入的电话号码为列表
    message:发送的消息内容字符串
    '''
    url = "https://smn.{_project}.myhwclouds.com/v2/{sub_project_id}/notifications/sms".format(_project=url_project,sub_project_id=sub_project_id)
    for phone in phone_list:
        body = {"endpoint": phone, "message": message}
        headers = {"Content-type": "application/json", "X-Auth-Token": token}
        r = requests.post(url=url, headers=headers, json=body)
        if r.status_code == 200:
            logger.logger('smn_send_successful','%s  send to %s  Successful.\n' % (time.strftime("%Y-%m-%d %H:%M:%S"),phone))
        else:
            print(url, 'SMN Failed')
            logger.logger('smn_send_err','%s  send to %s  Failed. code:%s info:%s\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), phone,r.status_code,r.json()))
    # token = get_tocken(url_project,domainname,username)
