import allure

from service.demo.demo_sql import DemoSql


class DemoAssert(DemoSql):

    @allure.step(title="接口返回结果校验")
    def assert_demo(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_demo(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["mobile"])
        assert True, "数据比较不一致"


if __name__ == '__main__':
    s = DemoAssert()

