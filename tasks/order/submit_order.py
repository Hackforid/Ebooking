# -*- coding: utf-8 -*-]

import datetime

from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask

from tasks.models.inventory import InventoryModel
from models.order import OrderModel
from constants import QUEUE_ORDER

def get_stay_days(checkin_date, checkout_date):
    aday = datetime.timedelta(days=1)
    days = []
    while checkin_date < checkout_date:
        days.append(checkin_date)
        checkin_date= checkin_date + aday

    return days


def combin_year_month(year, month):
    return int("{}{:0>2d}".format(year, month))

def valid_inventory(session, order):
    print '# valid inventory for order ', order.id
    stay_days = get_stay_days(order.checkin_date, order.checkout_date)
    year_months = [(day.year, day.month) for day in stay_days]
    year_months = {}.fromkeys(year_months).keys()

    inventories = InventoryModel.get_by_merchant_hotel_roomtype_dates(
        session, order.merchant_id,
        order.hotel_id, order.room_type_id, year_months)
    
    if not inventories:
        print "no inventory"
        return False

    for inventory in inventories:
        print inventory.todict()


    for day in stay_days:
        inventory = None
        month = combin_year_month(day.year, day.month)
        print '...finding', month

        for _inventory in inventories:
            if _inventory.month == month:
                inventory = _inventory
                break
        else:
            print 'day', day, 'not found'
            return False

        if inventory.get_day(day.day, 0) < order.room_quantity:
            print 'day', day, ' is not enough (inventory = '+inventory.get_day(day.day, 0) + ')'
            return False
    else:
        print 'found'
        return True



def create_order(order):
    order = OrderModel.get_by_main_order_id(order.id)
    if order:
        return

    order = OrderModel.new_order(order)
    if order:
        return order

def create_order_success(order):
    pass


def create_order_fail(order):
    pass

def get_order(session, order_id):
    return OrderModel.get_by_id(session, order_id)


@app.task(base=SqlAlchemyTask, bind=True, queue=QUEUE_ORDER, ignore_result=True)
def start_order(self, order_id):
    print 'hello world'

    session = self.session
    order = get_order(session, order_id)
    if not valid_inventory(session, order):
        print 'more room please'
        order.status = 200
        session.commit()
        return
    else:
        order.status = 100
        session.commit()




    
    #stay_days = get_stay_days(order['checkInDate'], order['checkOutDate'])

    #if not valid_inventory(order, stay_days):
        #pass

    #create_order(order)



