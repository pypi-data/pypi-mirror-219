import os
import time
import calendar
import hashlib
import json
import requests

def get_task_detail(name, code):
    params = {"code": code, "name": name}

    sign, userName, timestamp = get_sign()
    headers = {"VG-Request-User": userName, "VG-Request-Sign": sign,
               "VG-Request-Time": str(timestamp)}
    url = 'http://dev.vango_tapd_1166744_openapi.data-ad.37ops.com/openapi/task/detail'

    response = requests.get(url=url, params=params, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text)
    return None;


def upload_task_file(task_id, file_path):
    data = {"task_id": task_id}

    with open(file_path, "rb") as upload_file:
        files = {"file": upload_file}

        sign, userName, timestamp = get_sign()
        headers = {"VG-Request-User": userName, "VG-Request-Sign": sign,
                   "VG-Request-Time": str(timestamp)}
        url = 'http://10.16.23.3:8000/openapi/task/file_upload'

        response = requests.post(url=url, files=files, data=data, headers=headers)
        if response.status_code == 200:
            return json.loads(response.text)
        return None;


def get_sign():
    user = get_user_info()
    userName = ''
    password = ''
    if user[0]:
        userName = user[0]
    if user[1]:
        password = user[1]
    timestamp = calendar.timegm(time.gmtime())

    md5 = hashlib.md5()
    md5.update(userName.encode('utf-8'))
    md5.update(password.encode('utf-8'))
    md5.update(str(timestamp).encode('utf-8'))
    sign = md5.hexdigest().upper()

    return sign, userName, timestamp;


def get_user_info():
    userFile = './user.txt';
    user = []
    if os.path.exists(userFile):
        with open(userFile, 'r') as f:
            userInfo = f.read()
            f.close()
        user = userInfo.split(' ')
    return user;