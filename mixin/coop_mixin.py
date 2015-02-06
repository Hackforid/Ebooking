# -*- coding: utf-8 -*-

from exception.json_exception import JsonException

from models.rate_plan import RatePlanModel
from models.room_rate import RoomRateModel
from models.cooperate_roomtype import CooperateRoomTypeModel
from models.inventory import InventoryModel

from tasks.stock import PushRatePlanTask, PushRoomTypeTask

class CooperateMixin(object):

    def delete_roomtype(self, roomtype):
        self.delete_roomtypes([roomtype])

    def delete_roomtypes(self, roomtypes):
        for roomtype in roomtypes:
            self.delete_rateplan_by_roomtype(roomtype)
            self.clear_inventoris_by_roomtype(roomtype)

        # delete roomtypes:
        for roomtype in roomtypes:
            roomtype.is_delete = 1
        self.db.commit()

        roomtype_ids = [roomtype.id for roomtype in roomtypes]
        PushRoomTypeTask().update_roomtype_valid.delay(roomtype_ids)

    def delete_rateplan(self, rateplan):
        self.delete_rateplans([rateplan])

    def delete_rateplan_by_roomtype(self, roomtype):
        rateplans = RatePlanModel.get_by_roomtype(self.db, roomtype.id)
        self.delete_rateplans(rateplans)

    def delete_rateplans(self, rateplans):
        rateplan_ids = [rateplan.id for rateplan in rateplans]
        roomrates = RoomRateModel.get_by_rateplans(self.db, rateplan_ids)

        for rateplan in rateplans:
            rateplan.is_delete = 1
        for roomrate in roomrates:
            roomrate.is_delete = 1

        self.db.commit()

        PushRatePlanTask().update_rateplans_valid_status.delay(rateplan_ids)

    def clear_inventoris_by_roomtype(self, roomtype):
        InventoryModel.delete_by_roomtype_id(self.db, roomtype.id)





