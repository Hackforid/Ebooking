# -*- coding: utf8 -*-

from views.room_type import GetRoomTypeByHotelsAPIHandler


handlers = [
        (r"/hotels/?", GetRoomTypeByHotelsAPIHandler),
        ]
