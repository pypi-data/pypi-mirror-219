# 查询类，获取
# data, card，user, self, websetting, cache的查询

import os
import requests
from .setting import INTERFACE_PATH,DATA_STORAGE_TYPE, DATA_DATA_TYPE, DATA_LANGUAGE, DATA_TASK_TYPE
import time
from .info import Information
import pprint

class QueryDigit():

    def __init__(self, api_token=Information().get_api_token()):
        self.api_token = api_token
        self.queryset = ""
        self.api_path = INTERFACE_PATH
        self.api_types = ['data', 'card', 'user', 'account', 'websetting','dataid']

        self.api = {api_type: f"{INTERFACE_PATH}/api/{api_type}/" for api_type in self.api_types}

        self.errors = []
        self.brief = {
            "data": ['data_id', 'name', ],
            "card": ['card_id', 'name', ],
            "user": ['name', 'real_name'],
            "account": ['user_id', 'name', 'real_name', 'email'],
            "websetting":[],
            "dataid":['data_id']

        }

    def _get_all_resources(self, api_type):
        # api_type 取值为data, card, user,account, websetting
        status_code = 0
        max_request = 10  # 重复请求最大次数
        count = 0
        self.errors = []  # 每次获取新的数据都需要将之前的错误清空
        self.queryset = []
        response = ''
        url = self.api.get(api_type)
        # url = 'http://127.0.0.1:8000/api/user/'
        headers = {'api-token': self.api_token}

        while status_code != 200:  # 循环调用接口，避免因为网络故障导致的请求失败
            response = requests.get(url, headers=headers)
            status_code = response.status_code
            if status_code != 200:
                count += 1
                time.sleep(1)
            if count == max_request:
                self.errors.append(f"status code: {status_code}")
                return False

        content = response.json()

        if content.get('status') != 200:
            self.errors.append(content.get('error'))
            return False

        self.queryset = content.get('data')  # 将获取的数据存入queryset中
        return True  # 请求成功了

    def _get_single_resource(self, api_type: str, id):
        # 当api_type = dataid时， id表示的可能是data_id，也可能是name
        status_code = 0
        max_request = 10  # 重复请求最大次数
        count = 0
        self.errors = []  # 每次获取新的数据都需要将之前的错误清空
        self.queryset = []
        response = ''
        url = f"{self.api.get(api_type)}{id}/"

        headers = {'api-token': self.api_token}

        if api_type not in ['data', 'card', 'user','dataid']:
            self.errors.append(f"'{api_type}'的值只能为['data'、'card'、'user','dataid]四者之一")
            return False

        while status_code != 200:  # 循环调用接口，避免因为网络故障导致的请求失败
            response = requests.get(url, headers=headers)
            status_code = response.status_code

            if status_code != 200:
                count += 1
                time.sleep(1)
            if count == max_request:
                self.errors.append(f"status code: {status_code}")
                return False
        content = response.json()
        if content.get('status') != 200:
            self.errors.append(content.get('error'))
            return False
        self.queryset = [content.get('data')]  # 将获取的数据存入queryset中
        return True  # 请求成功了

    # 美化输出
    def _pretty_print(self, api_type: str):
        if api_type != "websetting":
            briefs = self.brief.get(api_type)
            print("\t".join(briefs))
            for resource in self.queryset:
                print("\t".join([resource[i] for i in briefs]))

    """
    已经写好获取两种类型的数据函数，下面是用户请求，选择是否输出details"""

    def get_resources(self, api_type: str, id=None, detail=False):
        if id:
            if not self._get_single_resource(api_type=api_type, id=id):
                print(self.errors[0])
                return self.queryset
        else:
            if not self._get_all_resources(api_type=api_type):
                print(self.errors[0])
                return self.queryset

        if not detail:
            self._pretty_print(api_type=api_type)
        else:
            print(self.queryset)

        return self.queryset



    def get_category(self):
        cats = ['storage_type', 'data_type', 'language', 'task_type', ]
        cats_name = [DATA_STORAGE_TYPE, DATA_DATA_TYPE, DATA_LANGUAGE, DATA_TASK_TYPE]
        category = {c:cats_name[index] for index, c in enumerate(cats)}
        pprint.pprint(category)
        return category