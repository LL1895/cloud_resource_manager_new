#!/usr/bin/python
# _*_ coding:utf-8 _*_
import requests  #导入http协议请求模块
import sys, time, os, getpass,json#, son

#定义获取token函数
def get_tocken():
#通过用户名密码获取token
	return_code = 0
	while return_code != 201:	
		 #从命令行获取用户名和密码
		domainname = raw_input("请输入技服组使用的华为云用户名:") 
		username = raw_input("请输入子用户名:")
		password = getpass.getpass('请输入密码:')
		#requests模块所需参数如下
        	post_data = {"auth": {"identity": {"methods": ["password"],"password": {"user": {"name": username,"password": password,"domain": {"name": domainname}}}},"scope": {"project": {"name":"cn-north-1"}}}}
        	headers = {"content-type":"application/json",}
        	url_str = "https://iam.cn-north-1.myhwclouds.com/v3/auth/tokens"
		#使用requests模块发起gettoken动作
		r = requests.post(url=url_str, json=post_data, headers=headers)
        	r_headers = r.headers #获取返回头
		#检查返回头字典中Token是否获取成功，如不成功会报错。用来判断密码是否正确。
		try:
			r_tocken = r_headers['X-Subject-Token']
		except :
			print "用户名或密码错误！"
		return_code = r.status_code #只有状态码为201(token获取成功)时才终止循环

	print "用户名密码正确，获取tocken success! "
	return r_tocken		#返回token

	#regions_headers = {'Content-Type':'application/json;charset=utf8',"X-Auth-Token":r_tocken}
	#regions_url = "https://iam.cn-north-1.myhwclouds.com/v3/regions"
	#regions = requests.get(url=regions_url,headers=regions_headers)
	#print "regions is:",regions
	#print "r_tocken :",r_tocken

#定义发送短信息函数
def send_message(s_url,phones,token, message):
	#message = raw_input("请输入短信内容:")	#命令行输入短信内容
	message = message
	############################################################
	for char in ['3','2','1'] :	#后悔药结构开始！！！
    		print '短信发送倒计时...%s\r' % char,
		sys.stdout.flush()
    		time.sleep(1)		#后悔药结束
	############################################################
	auth_tocken = token		#短信条件1:token
	SMN_headers = {"Content-type": "application/json", "X-Auth-Token": auth_tocken}  #header
	#print "Tocken is :", auth_tocken	#写脚本过程中拍错用！
	for phone in phones:		#接口不允许群发短信，弄个循环搞定,phone取值后type为<str>
		nameinfo = json.dumps(phones[phone], encoding="utf-8", ensure_ascii=False)
		#http请求body和请求操作如下
		body = {"endpoint": phone,"message": message}  #消息体json格式，从帮助中心获得！
		s = requests.post(url=s_url,headers=SMN_headers,json=body)  #发送短信，将返回值给变量s
		#根据返回值判断是否发送成功,如下
		if s.status_code == 200:				
			#print "短信已发到 ", 
			print nameinfo,"成功！",
			time.sleep(0.1)
	
		else:
			print "短信到 ", nameinfo, "失败！",s.status_code,":", s.content, 
	
#获取电话号码函数
def phones():
	if os.path.exists("./phones.txt"):
		print "已找到文件phones.txt. 请确保每个电话号码 姓名一行(中间空格隔开)"
		man = open('./phones.txt')
		line = man.readline() #line的type为str
		tn = {}
		while line:
			arr = line.split(' ') #arr的type为list
			t = arr[0]	#t的type为t
			n = arr[1]
			tn[t] = n.strip('\n')
			line = man.readline()
		man.close()
		renshu = len(tn)
		namesinfo = json.dumps(tn.values(),encoding="utf-8", ensure_ascii=False)
		print "名单:",namesinfo, "收件人共",renshu,"人"
		#send_message(s_url=url,phones=phones,token=token) #do it！
		return tn
	else:
		print "没找到phones.txt,请将phones.txt文件放到本目录下,并且每个电话号码 姓名一行(中间空格隔开)。"
		print "请将文件放在当前脚步目录后重新执行脚本"
		return None
#读取短信文本
def getmessage():
	
	if os.path.exists('message.txt'):
		#print "已找到短信文件message.txt"
		m = open("message.txt")
		content = m.read()
		message = content.replace('\n','')
		#message = json.dumps(content, encoding='UTF-8', ensure_ascii=False)
		m.close()
		print "\n请检查短信内容:",message
		yesorno = raw_input("\n确认短信内容无误?是输入y:")
 		if yesorno is "y":
			return message
		else:
			return None
	
	else:
		print "当前目录message.txt文件Not found！,请将短信内容写入文件放在当前脚步目录后重新执行脚本"
		return None
#执行函数	
if __name__ == '__main__':
	token = get_tocken()	#搞到token
	#project_id = ????
	url = "https://smn.cn-north-1.myhuaweicloud.com/v2/10a85dd37bac4e8abf6f6c349c7edfdd/notifications/sms"  #华北SMN的API
	phones = phones()
	message = getmessage()
	if phones:
		if message:
			send_message(s_url=url,phones=phones,token=token,message=message) #do it！
