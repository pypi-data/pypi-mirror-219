import json
import os.path
import re
import sys
import requests
import time

from huhk.unit_fun import FunBase
from huhk import admin_host, projects_path, service_path, testcase_path


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

    def get_init_value(self):
        """
            生成项目__init__.py文件
        """
        value = 'from huhk.init_project import GetApi\n' \
                'from huhk.unit_request import UnitRequest\n\n\n' \
                'class Request(UnitRequest):\n    pass\n\n\n' \
                'unit_request = UnitRequest("SIT", "%s")\n' \
                '# 环境变量\nvariable = unit_request.variable\n' \
                'http_requester = unit_request.http_requester\n\n\n' \
                'if __name__ == "__main__":\n' % (self.app_key)
        if self.app_key:
            value += "    GetApi(app_key=APP_KEY)\n"
        else:
            value += "    GetApi("
            value += "api_type=%s, " % self.api_type if self.api_type else ""
            value += "value='%s', " % self.value if self.value else ""
            value += "name='%s', " % self.name if self.name else ""
            value += "yapi_url='%s', " % self.yapi_url if self.yapi_url else ""
            value = value[:-2] + ")"
        return value



if __name__ == "__main__":
    BaseProject().get_init_value()
