from service.demo.demo_fun import DemoFun


class DemoSql(DemoFun):

    def sql_demo(self, **kwargs):
        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段
        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  # 模糊查询字段，数组包含查询字段，区间字段处理
        # kwargs["order_by"] = None  # 排序
        sql_str = self.get_sql_str("table", **kwargs)  # 生成sql语句
        # out = self.run_mysql(sql_str)  # 执行sql语句
        # return out


if __name__ == '__main__':
    s = DemoSql()

