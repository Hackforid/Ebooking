# -*- coding: utf-8 -*-

from tornado.escape import json_encode, json_decode

from views.base import BtwBaseHandler
from models.room_type import RoomTypeModel



class GetRoomTypeByHotelsAPIHandler(BtwBaseHandler):

    def get(self):
        ids = self.get_query_argument('hotel_ids', None)
        try:
            ids = json_decode(ids)
        except:
            self.finish_json(errcode=1000, errmsg="wrong arguments:hotel_ids")
            return

        if ids:
            rooms = RoomTypeModel.gets_by_hotel_ids(self.db, ids)
            self.finish_json(result=dict(
                    room_types=[room.todict() for room in rooms],
                ))
        else:
            self.finish_json(result=dict(
                    room_types=[],
                ))



