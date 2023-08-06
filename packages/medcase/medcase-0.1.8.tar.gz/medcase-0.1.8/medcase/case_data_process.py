# -*- coding: utf-8 -*-
# @Author  : jackxclei
# @Time    : 2023/6/29 10:50 上午
# @Function:
import requests
import time
import hashlib
def case_data_process(business='',date_ranage= ''):
    appid = 'urftian'
    token = "1053813a-224e-417a-b46f-b3ca2ae84a7f"
    user = 'urftian'
    timestamp = str(int(time.time()))
    print(timestamp)
    signature = timestamp + token + timestamp
    hash_object = hashlib.sha256(signature.encode('utf-8'))
    signature = hash_object.hexdigest()
    print(signature)
    headers = {
        "AppID":appid,
        "Signature":signature,
        "Timestamp":timestamp,
        "X-User":user
    }
    url = 'http://30.162.219.142/api/v1/medapimanager/interface/api_data_draft?business=慧用药&api_id=083b9dc5-84fa-4663-8859-b4e69e362042'
    res = requests.get(url=url,headers=headers).json()["data"]
    print(res[0])
    return res

if __name__ == '__main__':
    case_data_process()