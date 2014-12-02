# -*- coding: utf8 -*-

from views.login import LoginHandler


handlers = [
        (r"/login/?", LoginHandler),
        ]
