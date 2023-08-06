from huhk.init_project import GetApi
from huhk.unit_request import UnitRequest


class Request(UnitRequest):
    pass


APP_KEY = "a63ca17b-3cf3-46cb-b8b6-9ad20518e1e12"


unit_request = Request("SIT", APP_KEY)
# 环境变量
variable = unit_request.variable
http_requester = unit_request.http_requester


if __name__ == "__main__":
    GetApi(app_key=APP_KEY).create_or_update_project()
