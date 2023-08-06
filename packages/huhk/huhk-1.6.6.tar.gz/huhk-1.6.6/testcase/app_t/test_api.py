import pytest
import allure

from service.app_t.app_t_api_fun import App_TApiFun


@allure.epic("针对单api的测试")
@allure.feature("场景：")
class TestApi:
    def setup(self):
        self.f = App_TApiFun()

    @pytest.mark.skip("待维护")
    @allure.step(title="浩瀚模块-关联关系-Y")
    def test_open_haohan_relation_update(self):
        self.f.open_haohan_relation_update()


    @pytest.mark.skip("待维护")
    @allure.step(title="浩瀚模块 - 更改充电桩权益状态-Y")
    def test_open_haohan_rights_update(self):
        self.f.open_haohan_rights_update()


    @pytest.mark.skip("待维护")
    @allure.step(title="APP-用户签到")
    def test_points_pointsApp_signIn(self):
        self.f.points_pointsApp_signIn()


    @pytest.mark.skip("待维护")
    @allure.step(title="APP - 查看我的积分")
    def test_points_pointsApp_myPoints(self):
        self.f.points_pointsApp_myPoints()


    @pytest.mark.skip("待维护")
    @allure.step(title="APP - 总积分查询")
    def test_points_pointsApp_myPointsTotal(self):
        self.f.points_pointsApp_myPointsTotal()


    @pytest.mark.skip("待维护")
    @allure.step(title="查看积分明细- - 积分流水分页查询")
    def test_points_points_flowDetail(self):
        self.f.points_points_flowDetail()


    @pytest.mark.skip("待维护")
    @allure.step(title="积分统计-分页查询积分")
    def test_points_points_page(self):
        self.f.points_points_page()


    @pytest.mark.skip("待维护")
    @allure.step(title="积分统计 - 导出")
    def test_points_points_download(self):
        self.f.points_points_download()


    @pytest.mark.skip("待维护")
    @allure.step(title="用户中心-兑换明细 - 分页查询")
    def test_points_points_convertDetail(self):
        self.f.points_points_convertDetail()


