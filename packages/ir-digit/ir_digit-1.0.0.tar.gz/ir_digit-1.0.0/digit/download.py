import json

from .info import Information
from .setting import CACHE_PATH
import os
from .query import QueryDigit
import shutil
import git
import stat


class Download():
    """
    downlaod 主要就是repo下载
    初始化时检查是否存在对应的文件目录
    不存在则创建
    """

    def __init__(self):
        self.info = Information()
        self.cache_path = CACHE_PATH
        self.qd = QueryDigit()
        self._verity_cache_path()  # 初始化目录是都存在，不存在则创建，存在则无动作

    def _verity_cache_path(self):
        # 检查是否建立了该目录，没有建立则建立
        if not os.path.exists(self.cache_path):
            os.mkdir(self.cache_path)
            os.chmod(self.cache_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

    def _get_data_id(self, data_id_or_name):
        # 检测是否已经缓存, 
        qs = self.qd.get_resources(api_type="dataid", id=data_id_or_name)

        if not qs:
            print(f"data_id_or_name = {data_id_or_name}的资源不存在")
            return False
        data_id = qs[0].get('data_id')
        return data_id

    def _generate_config(self, data_obj):
        print("开始生成config.json文件")
        # {
        #     "name": "test",
        #     "url_or_path": "https://gitee.com/fkliu/digit_test.git",
        #     "storage_type": 1,
        #     "data_type": 1,
        #     "language": 1,
        #     "task_type": 11,
        #     "tags": ["示例标签1", "示例标签2"],
        #     "description": ""
        # }
        sort_json = ['data_id', 'user_id', 'url', 'name', 'author', 'storage_type', 'data_type', 'language',
                     'task_type', 'tags', 'description', 'picture', 'md_instruction', 'usage_number',
                     'permission_level', 'status', 'create_time', 'update_time']
        temp = {i: data_obj.get(i) for i in sort_json}

        with open(os.path.join(self.cache_path, data_obj.get("data_id"),'config.json'), 'w', encoding="utf-8") as f:
            json.dump(temp, f, indent=4)
        print(f"资源信息已保存至config.json：{os.path.join(self.cache_path, data_obj.get('data_id'), 'config.json')}")
        return True

    def _delete_cache(self, data_id):
        if not os.path.exists(os.path.join(self.cache_path, data_id)):
            print(f"资源{data_id} 在缓存目录中不存在")
            return False  # 不存在，未进行删除
        shutil.rmtree(os.path.join(self.cache_path, data_id))
        self.info.delete_data(data_id=data_id)  # 在缓存表中删除

        print(f"资源{data_id} 已从缓存目录中删除")
        return True

    def _update_cache(self, data_id):
        data_obj = self.qd.get_resources(api_type="data", id=data_id)[0]

        url = data_obj.get("url") if data_obj.get("url").endswith(".git") else data_obj.get("url") + ".git"  # git仓库

        print("正在下载/更新 Git远程仓库")

        if not os.path.exists(os.path.join(self.cache_path, data_id)):
            # 获取资源
            os.mkdir(os.path.join(self.cache_path, data_id))  # 创建缓存目录，以data_id命名

            try:
                git.Repo.clone_from(url, os.path.join(self.cache_path, data_id))
            except Exception as e:
                print("Git拉取远程仓库出错, 请检查url", e)


        else:
            ### 如果已存在，则进行更新操作
            try:
                git.Repo(os.path.join(self.cache_path, data_id)).remotes.origin.pull()
            except Exception as e:
                print("Git拉取远程仓库更新出错, 请检查url", e)
        print("更新完成")
        # 下载或更新完成后
        self.info.add_data(data_id=data_id)  # 在缓存表中更新
        print("更新信息缓存表信息")

        self._generate_config(data_obj=data_obj)  # 生成config.json文件

        return data_id

    def download_repo(self, data_id_or_name: str, update=False):
        # 检测是否已经缓存
        data_id = self._get_data_id(data_id_or_name=data_id_or_name)
        if update:
            self._update_cache(data_id=data_id)
        else:
            if not self.info.query_data(data_id=data_id):  # 虽然是更新，但缓存中不存在，则仍需要更新
                self._update_cache(data_id=data_id)
            else:
                print(f"资源 {data_id_or_name} 存在缓存资源中，可直接使用，如需更新资源请将调整参数update=True")
        return data_id

    def clean_cache(self):
        shutil.rmtree(self.cache_path)
        self.info.delete_all_data()
        print("已清除全部缓存")
        return True

    def clean_cache_by_id(self, data_id):
        self._delete_cache(data_id=data_id)
        print(f"资源{data_id}缓存已清除")
        return True
