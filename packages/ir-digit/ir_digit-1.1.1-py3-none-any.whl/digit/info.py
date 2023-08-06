import json
import sys
import os

"""
加载info文件， 其中包括api_token和data的字典，如果已经缓存，则data字典中有对应data的data_id，
"""



class Information:
    def __init__(self):
        if getattr(sys, 'frozen', None): # 确保在不同环境下都能加载正确的文件路径， 无论是打包后的执行文件还是为打包的python脚本
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)
        self.file_path = os.path.join(basedir ,"info.json")
        self.api_token = ""
        self.data = {}
        self._load_data()

    def _load_data(self):
        with open(self.file_path) as json_file:
            data = json.load(json_file)
            self.data = data.get("data", {})
            self.api_token = data.get("api_token", "")

    def _save_data(self):
        try:
            with open(self.file_path, "w") as json_file:
                data = {
                    "api_token": self.api_token,
                    "data": self.data
                }
                json.dump(data, json_file, indent=4)
        except Exception as e:
            print(f"修改出错，错误信息：{e}")

    def update_api_token(self, new_token):
        if new_token:
            self.api_token = new_token
            self._save_data()
        else:
            print("new_token 为空")

    def get_api_token(self):
        return self.api_token

    def add_data(self, data_id):
        # 增加已经下载的数据的缓存表，表示该数据已下载
        self.data[data_id] = data_id
        self._save_data()

    def delete_data(self, data_id):
        # 删除data_id对应的缓存判断表。查询不到，表示该数据未下载
        self.data.pop(data_id)
        self._save_data()

    def delete_all_data(self):
        self.data = []
        self._save_data()

    def query_data(self, data_id):
        if data_id in self.data:
            return self.data.get(data_id) # 如果存在则返回data_id
        return False # 如果不存在则返回False
