#!/usr/bin/env python

import time
import uuid
import hashlib
import base64

# 需要先使用 pip install requests 命令安装依赖
import requests

# 开发准备：APP_Key
APP_KEY="YDk30yiBI5n2P5aNr7Nfqh71b902"
# 开发准备：APP_Secret
APP_SECRET="iPi1q81hj1dj40iN5orSA60899O3"

# 开发准备：APP接入地址 + 接口访问URI
url = 'https://117.78.29.66:10443/sms/batchSendSms/v1'

# 开发准备：签名通道号
sender="1069100121280106"

# 填写短信接收人号码
receiver="13333392837"

# 状态报告接收地址，为空或者不填表示不接收状态报告
statusCallBack=""

# 开发准备：模板ID
TEMPLATE_ID="4a74e40363834fd1ba7d3cf85b46cea9"
# 模板变量请务必根据实际情况修改，查看更多模板变量规则
# 如模板内容为“您有${NUM_2}件快递请到${TXT_32}领取”时，templateParas可填写为["3","人民公园正门"]
# 双变量示例：TEMPLATE_PARAM='["3","人民公园正门"]'
TEMPLATE_PARAM='["369751"]'

def buildWSSEHeader(appKey, appSecret):
    now = time.strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = str(uuid.uuid4()).replace('-', '')
    digest = hashlib.sha256((nonce + now + appSecret).encode()).hexdigest()

    digestBase64 = base64.b64encode(digest.encode()).decode()
    return 'UsernameToken Username="{}",PasswordDigest="{}",Nonce="{}",Created="{}"'.format(appKey, digestBase64, nonce, now);


def main():
    wsseHeader = buildWSSEHeader(APP_KEY, APP_SECRET)

    header= {'Authorization':'WSSE realm="SDP",profile="UsernameToken",type="Appkey"', 'X-WSSE': wsseHeader}
    formData = {'from':sender, 'to':receiver, 'templateId':TEMPLATE_ID, 
                'templateParas':TEMPLATE_PARAM, 'statusCallBack':statusCallBack}
    print(header)
    r = requests.post(url, data=formData, headers=header, verify=False)
    print(r.text)


if __name__ == '__main__':
    main() 
