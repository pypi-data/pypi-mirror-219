import json
import os.path
import re
import sys
import requests
import time

from huhk.unit_fun import FunBase
from huhk import admin_host, projects_path, service_path, testcase_path, service_json_path
from huhk.unit_logger import logger


class BaseProject:
    def __init__(self, api_type=1, value="", name="", yapi_url="", app_key=""):
        """api_type: 0时，value是swagger的api，json的url
                     1时，value值为yapi项目token,
                     2时，value是yapi下载的json文件名，文件放在file目录下,
                     3时，value是yapi的yapi-swagger.json
           name:项目名称，空时默认当前py文件所在文件名上级目录
        """
        self.dir = projects_path
        self.url = admin_host
        self.api_testcase_list = []
        self.api_testcase_file_str = ""
        self.api_testcase_file_path = ""
        self.sql_fun_list = None
        self.name2 = None
        self.api_fun_fun_list = None
        self.api_fun_file_str = None
        self.api_fun_file_path = None
        self.assert_fun_list = None
        self.assert_file_str = None
        self.assert_file_path = None
        self.sql_file_str = None
        self.sql_file_str = None
        self.sql_file_path = None
        self.fun_init_list = None
        self.fun_init_str = None
        self.fun_file_path = None
        self.fun_file_str = None
        self.testcase_dir = ""
        self.api_file_path = ""
        self.service_dir = ""
        self.api_file_str = ""
        self.size_names = ("pageSize", "size")
        self.page_names = ("pageNum", "current")
        self.page_and_size = self.size_names + self.page_names
        self.yapi_url = yapi_url
        self.value = value
        self.api_type = api_type
        self.app_key = app_key
        self.name = name
        self.name2 = name
        self.api_list_old = []
        self.api_list = []
        self.error = ""
        self.api_dir = ""
        self.fun_dir = ""
        self.assert_dir = ""
        self.sql_dir = ""
        self.this_file_list = {}

    def get_init_value(self):
        """
            生成项目__init__.py文件
        """
        value = 'from huhk.init_project import GetApi\n' \
                'from huhk.unit_request import UnitRequest\n\n\n' \
                'class Request(UnitRequest):\n    pass\n\n\n' \
                'APP_KEY = "%s"\n\n\n' \
                'unit_request = Request("SIT", APP_KEY)\n' \
                '# 环境变量\nvariable = unit_request.variable\n' \
                'http_requester = unit_request.http_requester\n\n\n' \
                'if __name__ == "__main__":\n' % (self.app_key)
        if self.app_key:
            value += "    GetApi(app_key=APP_KEY).create_or_update_project()\n"
        else:
            value += "    GetApi("
            value += "api_type=%s, " % self.api_type if self.api_type else ""
            value += "value='%s', " % self.value if self.value else ""
            value += "name='%s', " % self.name if self.name else ""
            value += "yapi_url='%s', " % self.yapi_url if self.yapi_url else ""
            value = value[:-2] + ").create_or_update_project()\n"
        return value

    @staticmethod
    def get_service_value(key):
        """获取项目本地变量"""
        if os.path.exists(service_json_path):
            with open(service_json_path, encoding="utf-8") as fp:
                data = json.load(fp)
                return data.get(key)
        return None

    @staticmethod
    def set_service_value(key, value):
        """设置项目本地变量"""
        if not os.path.exists(service_json_path):
            FunBase.write_file(service_json_path, value="{}")
        with open(service_json_path) as fp:
            try:
                data = json.load(fp)
            except Exception as e:
                logger.error(str(e))
                data = {}
        with open(service_json_path, 'w') as fp:
            data[key] = value
            json.dump(data, fp, indent=4)

    def get_this_api_list(self):
        for dirpath, dirnames, filenames in os.walk(self.service_dir):
            for filename in filenames:
                key = filename.split("_")[-1].split(".")[0]
                if key in ("api", "fun", "assert", "sql"):
                    if self.this_file_list.get(key):
                        self.this_file_list[key].append(os.path.join(dirpath, filename))
                    else:
                        self.this_file_list[key] = [os.path.join(dirpath, filename)]
        print(self.this_file_list)


if __name__ == "__main__":
    a = BaseProject()
    a.service_dir = r"D:\projects\python_test\huhk-common\service\demo"
    a.get_this_api_list()
