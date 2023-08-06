from service.app_t.app_t_fun import App_TFun


class App_TSql(App_TFun):

    def sql_open_haohan_relation_update(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_open_haohan_rights_update(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_points_pointsApp_signIn(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_points_pointsApp_myPoints(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_points_pointsApp_myPointsTotal(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_points_points_flowDetail(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_points_points_page(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_points_points_download(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out

    def sql_points_points_convertDetail(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out


if __name__ == '__main__':
    s = App_TSql()

