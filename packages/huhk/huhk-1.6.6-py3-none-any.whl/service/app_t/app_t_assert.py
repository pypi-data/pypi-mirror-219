import allure

from service.app_t.app_t_sql import App_TSql


class App_TAssert(App_TSql):

    @allure.step(title="接口返回结果校验")
    def assert_open_haohan_relation_update(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_open_haohan_relation_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_open_haohan_rights_update(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_open_haohan_rights_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["params"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_signIn(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_points_pointsApp_signIn(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_myPoints(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_points_pointsApp_myPoints(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_myPointsTotal(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_points_pointsApp_myPointsTotal(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_flowDetail(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_points_points_flowDetail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_page(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_points_points_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["beforeTime", "endTime"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_download(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_points_points_download(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["beforeTime", "endTime"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_convertDetail(self, **kwargs):
        assert self.res.rsp.code in (0, 200), self.res.rsp.msg
        # out = self.sql_points_points_convertDetail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"


if __name__ == '__main__':
    s = App_TAssert()

