import allure

from service.demo import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/demo")
def demo(mobile=None, headers=None, **kwargs):
    """
    发送手机验证码
    up_time=1657087679

    params: mobile :  : 用户电话号码
    params: headers : 请求
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : null : 
    """
    _method = "GET"
    _url = "/common/common/sendSmsCode"

    _headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    _headers.update({"headers": headers})

    _data = {
        "mobile": mobile,  # 用户电话号码
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)

