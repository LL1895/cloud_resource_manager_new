# -*- coding:UTF-8 -*-
#!/usr/bin/env python
# Author:Zhangmingda
import os,sys,requests,time
# BASE_NAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(BASE_NAME)
from core import logger

def get_token(domainname,username,password,url_project,sub_project):
        """通过用户名密码获取token"""
        #requests模块所需参数如下
        post_data = {"auth": {"identity": {"methods": ["password"],"password": {"user": {"name": username,"password": password,"domain": {"name": domainname}}}},"scope": {"project": {"name":sub_project}}}}
        headers = {"content-type":"application/json",}
        url_str = "https://iam.{_project}.myhuaweicloud.com/v3/auth/tokens".format(_project=url_project)
        # print(url_str)
        #使用requests模块发起gettoken动作
        r = requests.post(url=url_str, json=post_data, headers=headers)
        if r.status_code == 201:
                token = r.headers['X-Subject-Token']
                # print(token)
                # logger.logger('get_token_OK','%s  get project %s token Successful.\n'%(time.strftime("%Y-%m-%d %H:%M:%S"),sub_project) )
                return token
        else:
                # logger.logger('get_token_failed','%s  get project %s token Failed. return_code:%s ,info %s\n' % (time.strftime("%Y-%m-%d %H:%M:%S"),sub_project,r.status_code,r.json()))
                return
