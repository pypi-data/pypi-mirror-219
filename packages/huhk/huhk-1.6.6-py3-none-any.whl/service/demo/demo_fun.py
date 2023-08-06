import requests

from huhk.unit_fun import FunBase
from huhk import admin_host


class DemoFun(FunBase):
    def __init__(self):
        super().__init__()
        self.res = None
        self._v_mobile = None

    def run_mysql(self, sql_str):
        # id是后台http://47.96.124.102/admin 项目数据库链接的id
        out = requests.post(admin_host + "/sql/running_sql/", json={"id": 1, "sql_str": sql_str}).json()
        if out.get("code") == "0000":
            return out.get("data")
        else:
            assert False, sql_str + str(out.get("msg"))


if __name__ == '__main__':
    f = DemoFun()
    out = f.run_mysql("SELECT * FROM `t_accept_log`  LIMIT 1;")
    print(out)

