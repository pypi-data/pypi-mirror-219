# -*- coding:utf-8 -*-
"""
core中继承了所有类的中的所有功能
"""
from .query import QueryDigit
from .info import Information
from .setting import *
from .download import Download
from .data import Data
from .child_base_data import *


class Core():

    def __init__(self):
        self.query = QueryDigit()
        self.info = Information()
        self.download = Download()
        self.data = Data()
        self.data_id = ''

    def update_api_token(self, new_token: str):
        """
        new_token: api-token字符串
        该方法来自Information类
        """
        self.info.update_api_token(new_token)

    def get_resources(self, api_type: str = 'data', id=None, detail: bool = False):
        """
        该函数用于查询digit平台现有资源，返回资源元数据
        :param api_type: 使用何种类型的api,api_type 可选{'data','card','user','account','websetting','dataid'}
        :param id:  查询特定资源时用用该资源的id进行查看
        :param detail: 是否输出可获取的所有元数据字段
        :return: queryset 查询结果
        """
        self.query.get_resources(api_type="data", id=None, detail=False)

    def get_category(self):
        """
        该函数用于查看digit平台分类体系编码与对应的实际含义，['storage_type', 'data_type', 'language', 'task_type', ]
        :return:
        """
        self.query.get_category()

    def download_repo(self, data_id_or_name: str, update: bool = False):
        """
        该函数可以根据data_id或name下载对应的资源至本地
        :param data_id_or_name:
        :param update: 是否更新缓存
        :return:
        """
        self.data_id = self.download.download_repo(data_id_or_name, update)

    def load(self, data_id_or_name: str, imp_class="DigitData"):
        """
        该函数用于加载下载的脚本代码中的DigitData类
        :return:

        :param data_id_or_name:
        :param imp_class: 导入类的类型名称
        :return: imp_class_instance 导入类的实例
        """
        data_id = ''
        if self.data_id:
            data_id = self.data_id
        else:
            data_id = data_id_or_name
        return self.data.load(data_id_or_name=data_id, imp_class=imp_class)

    def run(self):
        self.data.run()

    def all_in_one(self, data_id_or_name: str, update: bool = False, imp_class: str = "DigitData"):
        # 下载并加载repo， 相当于download_repo()和 load两个函数
        self.download_repo(data_id_or_name, update)
        self.load(data_id_or_name=self.data_id, imp_class=imp_class)
        self.run()

    def get_data_id(self):
        """
        获取当前下载仓库的 data_id
        :return: data_id:str
        """
        print(self.data_id)
        return self.data_id

    def upload(self,md_instruction_path,config_path):
        # 上传data资源
        self.data.upload(md_instruction_path,config_path)

    def delete(self, data_id_or_name):
        # 删除自己的data
        self.data.delete(data_id_or_name)




