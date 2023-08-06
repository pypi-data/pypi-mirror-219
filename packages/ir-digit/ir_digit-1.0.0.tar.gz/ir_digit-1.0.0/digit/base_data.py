"""
base_data.py
其中包含BaseData类，用于存储数据
"""
import json
import os
from .setting import  CACHE_PATH, DATA_STORAGE_TYPE, DATA_DATA_TYPE, DATA_LANGUAGE, DATA_TASK_TYPE


class BaseData(object):
    def __init__(self, data_id: str):
        self.data_id = data_id
        self.config = self._load_config()
        self.data = self.load_data()



    def _load_config(self):
        """
        加载配置文件
        """

        config_path = os.path.join(CACHE_PATH, self.data_id, 'config.json')
        if not os.path.exists(config_path):
            print(f"配置文件config.json不存在，请检查路径：{config_path}是否正确")
            return False
        with open(config_path, 'r', encoding='utf-8') as f:
            print(f"配置文件config.json读取成功")
            return json.load(f)


    def get_name(self):
        name = self.config.get("name")
        print("name: ",end='')
        print(name)
        return name

    def get_url(self):
        url = self.config.get("url_or_path")
        print("url_or_path: ", end='')
        print(url)
        return url

    def get_tags(self):
        tags = self.config.get("tags")
        print("tags: ", end='')
        print(tags)
        return tags

    def get_category(self,number=False):
        cats = ['storage_type','data_type','language','task_type',]
        cats_name = [DATA_STORAGE_TYPE, DATA_DATA_TYPE, DATA_LANGUAGE,DATA_TASK_TYPE]
        if not number:
            cat = {c: cats_name[index].get(self.config.get(c)) for index, c in enumerate(cats)}
        else:
            cat = {c: self.config.get(c) for c in cats}
        print(cat)
        return cat

    def get_description(self):
        """
        数据使用说明,包括数据集说明和代码说明
        默认使用config.json中的description字段
        可自行重构方法
        """
        data_description = self.config.get('description')
        print("description: ",end='')
        print(data_description)
        return data_description

    def get_readme(self):
        md_path = os.path.join(CACHE_PATH, self.data_id, 'README.md')
        md = ''
        with open(md_path, 'r',encoding="utf-8") as f:
            md = f.read()
        print(f"README.md文件的路径为：{md_path}")

        return md



    def get_config(self,number=False):
        self.get_name()
        self.get_url()
        self.get_category(number=False)
        self.get_tags()
        self.get_description()



    def load_data(self):
        """
        !!! 必须重构方法
        加载数据
        可自行重构方法
        :return : dataset
        """

        pass

    def data_preview(self):
        """
        数据预览
        """
        pass

    def data_statistics(self):
        """
        描述性统计
        """
        pass

    def data_distribution(self):
        """
        数据分布
        """
        pass

    def data_preprocessing(self):
        """
        数据预处理
        """
        pass




    def run(self):
        """
        ## 函数执行自定义顺序
        :return:
        """
        print("====="+"元数据"+"=====")
        self.get_config()

        print("====="+"计算"+"=====")
        self.data_preview()
        self.data_statistics()
        self.data_distribution()
        self.data_preprocessing()







