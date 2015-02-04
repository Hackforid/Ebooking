# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from tasks.stock import PushRatePlanTask, PushHotelTask

from models.merchant import MerchantModel
from models.user import UserModel
from models.cooperate_hotel import CooperateHotelModel
from exception.celery_exception import CeleryException



@app.task(base=SqlAlchemyTask, bind=True)
def suspend_merchant(self, merchant_id, is_suspend):
    is_suspend = int(is_suspend)
    merchant = MerchantModel.get_by_id(self.session, merchant_id)
    if not merchant:
        raise CeleryException(errcode=404, errmsg="merchant not fount")

    merchant.is_suspend = is_suspend
    CooperateHotelModel.set_suspend_by_merchant_id(self.session, merchant_id, is_suspend)

    self.session.commit()

    PushHotelTask().push_hotel_suspend_by_merchant_id(merchant_id)
    return merchant

