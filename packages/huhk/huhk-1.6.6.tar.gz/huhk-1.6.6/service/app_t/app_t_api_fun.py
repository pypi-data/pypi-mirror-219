from service.app_t.app_t_assert import App_TAssert
from service.app_t import app_t_api

import allure


class App_TApiFun(App_TAssert):
    @allure.step(title="浩瀚模块-关联关系-Y")
    def open_haohan_relation_update(self, userId="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/open/haohan/relation/update
        params: userId :  : 用户ID（数据类型：String）"""
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.open_haohan_relation_update(**_kwargs)

        self._v_userId = userId

        if _assert is True:
            self.assert_open_haohan_relation_update(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="浩瀚模块 - 更改充电桩权益状态-Y")
    def open_haohan_rights_update(self, params="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/open/haohan/rights/update
        params: params : object :
        data : string : 加密数据"""
        params = self.get_value_choice(params, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.open_haohan_rights_update(**_kwargs)

        self._v_params = params

        if _assert is True:
            self.assert_open_haohan_rights_update(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="APP-用户签到")
    def points_pointsApp_signIn(self, userId="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/points/pointsApp/signIn
        params: userId :  : 用户ID"""
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_pointsApp_signIn(**_kwargs)

        self._v_userId = userId

        if _assert is True:
            self.assert_points_pointsApp_signIn(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="APP - 查看我的积分")
    def points_pointsApp_myPoints(self, userId="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/points/pointsApp/myPoints
        params: userId :  : 用户ID"""
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_pointsApp_myPoints(**_kwargs)

        self._v_userId = userId

        if _assert is True:
            self.assert_points_pointsApp_myPoints(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="APP - 总积分查询")
    def points_pointsApp_myPointsTotal(self, userId="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/points/pointsApp/myPointsTotal
        params: userId :  : 用户ID"""
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_pointsApp_myPointsTotal(**_kwargs)

        self._v_userId = userId

        if _assert is True:
            self.assert_points_pointsApp_myPointsTotal(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="查看积分明细- - 积分流水分页查询")
    def points_points_flowDetail(self, userId="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/points/points/flowDetail
        params: userId :  : 用户ID"""
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_flowDetail(**_kwargs)

        self._v_userId = userId

        if _assert is True:
            self.assert_points_points_flowDetail(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="积分统计-分页查询积分")
    def points_points_page(self, current=1, size=10, beforeTime="$None$", endTime="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/points/points/page
        params: current :  :
        params: size :  :
        params: beforeTime :  :
        params: endTime :  :"""
        if self.has_true(locals()) and not self._list_beforeTime:
            self.points_points_page(_assert=False)

        beforeTime = self.get_list_choice(beforeTime, self._list_beforeTime)
        endTime = self.get_list_choice(endTime, self._list_endTime)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_page(**_kwargs)

        self._list_beforeTime = self.get_res_value_list('beforeTime')
        self._list_endTime = self.get_res_value_list('endTime')
        self._v_beforeTime = beforeTime
        self._v_endTime = endTime

        if _assert is True:
            self.assert_points_points_page(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="积分统计 - 导出")
    def points_points_download(self, current=1, size=10, beforeTime="$None$", endTime="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/points/points/download
        params: current :  :
        params: size :  :
        params: endTime :  :
        params: beforeTime :  :"""
        beforeTime = self.get_value_choice(beforeTime, list_or_dict=None)
        endTime = self.get_value_choice(endTime, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_download(**_kwargs)

        self._v_beforeTime = beforeTime
        self._v_endTime = endTime

        if _assert is True:
            self.assert_points_points_download(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="用户中心-兑换明细 - 分页查询")
    def points_points_convertDetail(self, userId="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/points/points/convertDetail
        params: userId :  : 用户ID"""
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_convertDetail(**_kwargs)

        self._v_userId = userId

        if _assert is True:
            self.assert_points_points_convertDetail(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res


if __name__ == '__main__':
    s = App_TApiFun()

