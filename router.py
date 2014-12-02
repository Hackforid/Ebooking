# -*- coding: utf8 -*-

from views.login import LoginHandler
from views.user import UserManageHandler

handlers = [
        (r"/login/?", LoginHandler),
        (r"/userManage/(?P<merchant_id>\d+)/?", UserManageHandler)
        ]
