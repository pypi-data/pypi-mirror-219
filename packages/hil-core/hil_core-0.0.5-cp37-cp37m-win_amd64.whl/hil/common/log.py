'''
Copyright (c) 2023 by Deebug
Author: notmmao@gmail.com
Date: 2023-03-02 14:46:06
LastEditors: notmmao@gmail.com
LastEditTime: 2023-03-02 15:36:55
Description: 

==========  =============  ================
When        Who            What and why
==========  =============  ================

==========  =============  ================
'''
import requests
import time

class LogPostman(object):
    '''
    发送日志到客户端协议分析
    '''
    url = "http://127.0.0.1:28001/runner/log/stream"
    header = {}

    def __init__(self, input) -> None:
        runnerEnv = input.get("runnerEnv")
        jwt = runnerEnv.get("jwt")
        origin = runnerEnv.get("origin")
        url = f"{origin}/runner/log/stream"
        header = {
            # "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Cookie": f"jwt={jwt}"
        }
        self.url = url
        self.header = header

    def post(self, id, body, type="UDS", tag="log"):
        url = self.url
        header = self.header

        postdata = {
            # "type": "CAN"| "UDS" | "DOIP",
            "type": type,
            "tag": tag,
            "data": [
                {
                    "time": time.time(),
                    "id": id,
                    "data" : body
                }
            ]
        }
           
        r = requests.post(url=url, json=postdata, headers=header)
        return r