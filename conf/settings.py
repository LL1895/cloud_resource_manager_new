# -*- coding:UTF-8 -*-
#!/usr/bin/env python
# Author:Zhangmingda
import time
#设置测试账号的用户名和密码
iam = {
    #'domainname':'hwcloudsom1',
    #'username':'zhangmingda',
    #'password':'237828Zhang?'
    'domainname': 'hwcloudsom5',
    'username': 'hwcloudsom5',
    'password': 'v4jszc@syzc'
}
#设置不同时段的主机关机和删除时间
if 9 * 3600 < time.time()%86400 + 28800 < 19 * 3600:
    off_time = {
        'ecs': 9  # 关机时间
    }
    del_time = {
        'ecs': 11,  # 删除时间
        'publicip': 11,
        'cce': 8,
        'cloud_destop':8,
        'mrs': 4,
        'dws':4,
        'nat': 23,
        'rds':6,
        'radis':6,
        'evs':12
    }
else:
    off_time = {
        'ecs':5 #小时后关机
    }
    del_time = {
        'ecs':11, #小时后删除
        'publicip':11,
        'cce':8,
        'cloud_destop':8,
        'mrs':4,
        'dws':4,
        'nat':23,
        'rds':6,
        'radis':6,
        'evs': 12
    }

#设置不被关机和删除的ECS名字。创建包含这样名字的主机将不会被管理关机和删除
nodel_ecs_name = '勿删'
nodel_bandwidth_name = '勿删'
nodel_common_list = ['勿删','not_delete']
#账户下的不同地区的详细项目名称和项目ID
Endpoint_project_id = {
    'cn-north-1':{'cn-north-1':'10a85dd37bac4e8abf6f6c349c7edfdd'},
    #华北-北京一'cn-northeast-1':{'cn-northeast-1':'b5295dc8e09042a981b73175e8507050'},
    'cn-east-2':{ 'cn-east-2':'e30de5f42aee4f8586b6ff28fe713422'},#上海,
    'cn-south-1':{'cn-south-1':'521f1245f60341ba84107aaca247688c'},#广州
    'ap-southeast-1':{ 'ap-southeast-1':'dafc92e501c84cbcb2d29fef11a9e67f'},#香港cn-south-1_monitor-Tencent
    #'af-south-1':{ 'af-south-1':'bf9aa95d6d9f40cc9c93ca09f23b8256'},#非洲-约翰内斯堡
    #'cn-north-3':{ 'cn-north-3':'c90f4e2021314719936122ef44a056bd'},#华北-北京三
    'cn-north-4':{ 'cn-north-4':'28cac7af2b2141fc8dd5084cd2f735a3'},#华北-北京四
    #'cn-south-2':{ 'cn-south-2':'b4f4bed0aa5e44c89bd82842fd29a1f9'},#华南-深圳
}
#短信功能使用的项目名称
smn_project = 'cn-north-1'
#IAM子用户ID和名字电话设置(发送短信通知使用)
userinfo = {
    '4b372386848b4e4999d30eea0fdd8fad':{'name':'老司机','phone':[18676636792]},
    '1db02a4ae90447809f3ff84287818e28':{'name':'龙司机','phone':[15011162532]},
    '6b0d39b17b714f55989129e97a71f450':{'name':'大红姐','phone':[17331675057]},
    '99699734dd484f96a6f1b31c83543022': {'name': '澎举 ', 'phone': [13313268337]},
    '299e9fc2095348619338f5ef7da92c01': {'name': '燕永进', 'phone': [18639196087]},
    '8cf34e6bd22c479780a2998b2fe44537': {'name': '亮司机', 'phone': [13323268512]},
    '35fc3ab231854d179f03f79d8a81d79b': {'name': '老司机', 'phone': [18676636792]},
    '02c79aaa02964b3881517c83b89f2784': {'name': '智总', 'phone': [18610808247]},
    '6ce6bcb01d3841b89d7680cb5699b210': {'name': '王军', 'phone': [15010596086]},
    '1741ebc247904f81aeefafed6fcaea70': {'name': '雪磊', 'phone': [18691575009]},
    'e136092f32924d4bbd4861ee0e73176c': {'name': '少军', 'phone': [15332366299]},
    'ad9b1a2f659f47a3ba8d0c730ca20ca8': {'name': '董盼', 'phone': [15706017162]},
    '7561789204e94cf2aaf4c397d3125700': {'name': '田博', 'phone': [18629651443]},
    '94fb14f7c7b141a6a1c6c8cbe63ccd9a': {'name': '聪聪', 'phone': [18310008939]},
    '05066a23868010e11fa4c00f00efcb85': {'name': '安配', 'phone': [13663808934]},
    '5fe8d422f9e24d5a9c833c15cf95ae31': {'name': '殿宇', 'phone': [13943865251]},
    '05f0c36b2b0026061fb8c00fd45b45ae': {'name': '清潭', 'phone': [18824612507]},
}
#全员电话列表(发送短信通知使用，当被创建的资源无法区分为哪个子用户，关机&删除时发送给全员)

#全员电话列表(发送短信通知使用，当被创建的资源无法区分为哪个子用户，关机&删除时发送给全员)
all_phone = []
for user_ID in userinfo:
    for phone in userinfo[user_ID]['phone']:
        all_phone.append(phone)

