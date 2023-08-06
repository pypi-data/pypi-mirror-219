from service.demo.demo_assert import DemoAssert
from service.demo import demo_api

import allure


class DemoApiFun(DemoAssert):
    @allure.step(title="发送手机验证码")
    def demo(self, mobile="$None$", headers="$None$", _assert=True,  **kwargs):
        """url=/common/common/sendSmsCode
        params: mobile :  : 用户电话号码"""
        mobile = self.get_value_choice(mobile, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = demo_api.demo(**_kwargs)

        self._v_mobile = mobile

        if _assert is True:
            self.assert_demo(**_kwargs)
        elif _assert is not False:
            assert self.res.rsp.code == _assert, "校验code=%s不通过" % _assert
        return self.res


if __name__ == '__main__':
    s = DemoApiFun()

