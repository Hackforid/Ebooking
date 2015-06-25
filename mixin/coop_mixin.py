# -*- coding: utf-8 -*-

from tornado import gen
from exception.json_exception import JsonException

from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel
from models.cooperate_roomtype import CooperateRoomTypeModel
from models.inventory import InventoryModel

from tasks.stock import PushRatePlanTask, PushHotelTask
from utils.stock_push.rateplan import RatePlanPusher
from utils.stock_push.hotel import HotelPusher

class CooperateMixin(object):

    @gen.coroutine
    def delete_rateplan(self, rateplan):
        r = self._delete_rateplans([rateplan])
        raise gen.Return(r)

    @gen.coroutine
    def delete_hotel(self, hotel):
        if not hotel:
            raise gen.Return(True)
        r = yield self._delete_hotels([hotel])
        raise gen.Return(r)

    @gen.coroutine
    def delete_roomtype(self, roomtype):
        r = yield self._delete_roomtypes([roomtype])
        raise gen.Return(r)

    @gen.coroutine
    def _delete_hotels(self, hotels):
        if not hotels:
            gen.Return(True)

        for hotel in hotels:
            r = yield self._delete_roomtypes_by_hotel(hotel)
            if r:
                hotel.is_delete = 1
                r = yield HotelPusher(self.db).push_hotel(hotel)
                if not r:
                    raise gen.Return(False)
            else:
                raise gen.Return(False)
        else:
            raise gen.Return(True)

    @gen.coroutine 
    def _delete_roomtypes_by_hotel(self, hotel):
        roomtypes = CooperateRoomTypeModel.get_by_hotel_id(self.db, hotel.id)
        r = yield self._delete_roomtypes(roomtypes, notify_stock=False)
        raise gen.Return(r)

    @gen.coroutine
    def _delete_roomtypes(self, roomtypes, notify_stock=True):
        if not roomtypes:
            raise gen.Return(True)
        for roomtype in roomtypes:
            r = yield self._delete_rateplan_by_roomtype(roomtype)
            if not r:
                raise gen.Return(False)
            self._clear_inventoris_by_roomtype(roomtype)

        # delete roomtypes:
        for roomtype in roomtypes:
            roomtype.is_delete = 1

        if notify_stock:
            r = yield HotelPusher(self.db).push_hotel_by_id(roomtypes[0].hotel_id)
            if r:
                raise gen.Return(True)
            else:
                raise gen.Return(False)
        else:
            raise gen.Return(True)

    @gen.coroutine
    def _delete_rateplan_by_roomtype(self, roomtype):
        rateplans = RatePlanModel.get_by_roomtype(self.db, roomtype.id)
        r = yield self._delete_rateplans(rateplans)
        raise gen.Return(r)

    @gen.coroutine
    def _delete_rateplans(self, rateplans):
        if not rateplans:
            raise gen.Return(True)
        rateplan_ids = [rateplan.id for rateplan in rateplans]
        roomrates = RoomRateModel.get_by_rateplans(self.db, rateplan_ids)

        for rateplan in rateplans:
            rateplan.is_delete = 1
        for roomrate in roomrates:
            roomrate.is_delete = 1

        r = yield RatePlanPusher(self.db).update_rateplans_valid_status(rateplan_ids)
        raise gen.Return(r)

    def _clear_inventoris_by_roomtype(self, roomtype):
        InventoryModel.delete_by_roomtype_id(self.db, roomtype.id, commit=False)





