# -*- coding:UTF-8 -*-
#!/usr/bin/env python
# Author:Zhangmingda
import  os,sys,json,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
sys.path.append(BASE_DIR)

def logger(filename,message):
    '''这是一个非常low的日志记录功能'''
    log_file = "{base_dir}/logs/{filename}.log".format(base_dir=BASE_DIR,filename=filename)
    if  os.path.isfile(log_file):
        with open(log_file,'a+',encoding='utf-8') as f:
            f.write(message)
            f.flush()
            f.close()

    else:
        with open(log_file,'w',encoding='utf-8') as f:
            f.write(message)
            f.flush()
            f.close()
