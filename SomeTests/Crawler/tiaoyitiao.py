#coding=utf-8
import requests

import json

import time

from Crypto.Cipher import AES

import base64

action_data = { "score": 10086, "times": 666, "game_data": "{}" }

session_id = "ZYFOFW06gJexCvao2g78UklHkPaXqmcX9f2cGD6grKZH3stLu8KZXilrVPLACK//3z2e7rvQitYRoYmw2EzQlBJ6OMxoW4vqR8bTBak8OdXHnBgp+eZ72zjd7WDqsaoa2qs0qoC/SOnwDVAAy7F8kA\u003d\u003d"

aes_key = session_id[0:16]
aes_iv = aes_key

cryptor = AES.new(aes_key, AES.MODE_CBC, aes_iv)

str_action_data = json.dumps(action_data).encode("utf-8")
print("json_str_action_data ", str_action_data)

# Pkcs7
length = 16 - (len(str_action_data) % 16)
str_action_data += bytes([length]) * length

cipher_action_data = base64.b64encode(cryptor.encrypt(str_action_data)).decode("utf-8")
print("action_data ", cipher_action_data)

post_data = {
    "base_req": {
        "session_id": session_id,
        "fast": 1,
    },
    "action_data": cipher_action_data
}

headers = {
    "charset": "utf-8",
    "Accept-Encoding": "gzip",
    "referer": "https://servicewechat.com/wx7c8d593b2c3a7703/3/page-frame.html",
    "content-type": "application/json",
    "User-Agent": "MicroMessenger/6.6.1.1200(0x26060130) NetType/WIFI Language/zh_CN",
    "Content-Length": "0",
    "Host": "mp.weixin.qq.com",
    "Connection": "Keep-Alive"
}

url = "https://mp.weixin.qq.com/wxagame/wxagame_settlement"

response = requests.post(url, json=post_data, headers=headers)
print(json.loads(response.text))

# 作者：kiwi_fung
# 链接：https://www.jianshu.com/p/9fe14cbdee60
# 來源：简书
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。