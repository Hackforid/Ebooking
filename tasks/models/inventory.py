# -*- coding: utf-8 -*-


from tasks.celery_app import app
from tasks.base_task import SqlAlchemyTask
from models.inventory import InventoryModel



@staticmethod
@app.task(base=SqlAlchemyTask, bind=True)
def get_by_id(task_self, id):
    return task_self.session.query(InventoryModel)\
            .filter(InventoryModel.id == id)\
            .filter(InventoryModel.is_delete == 0)\
            .first()

@staticmethod
@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id(task_self, merchant_id, hotel_id):
    return task_self.session.query(InventoryModel)\
            .filter(InventoryModel.merchant_id == merchant_id)\
            .filter(InventoryModel.hotel_id == hotel_id)\
            .filter(InventoryModel.is_delete == 0)\
            .all()


@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id_and_date(task_self, merchant_id, hotel_id, year, month):
    return InventoryModel.get_by_merchant_id_and_hotel_id_and_date(task_self.session,
            merchant_id, hotel_id, year, month)

@staticmethod
@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_id_and_hotel_id_and_days(task_self, merchant_id, hotel_id, days):
    months = [InventoryModel.combin_year_month(day[0], day[1]) for day in days]
    return task_self.session.query(InventoryModel)\
            .filter(InventoryModel.merchant_id == merchant_id)\
            .filter(InventoryModel.hotel_id == hotel_id)\
            .filter(InventoryModel.month.in_(months))\
            .filter(InventoryModel.is_delete == 0)\
            .all()

@staticmethod
@app.task(base=SqlAlchemyTask, bind=True)
def get_by_merchant_hotel_roomtype_date(task_self, merchant_id, hotel_id, roomtype_id, year, month):
    month = InventoryModel.combin_year_month(year, month)
    return task_self.session.query(InventoryModel)\
            .filter(InventoryModel.merchant_id == merchant_id)\
            .filter(InventoryModel.hotel_id == hotel_id)\
            .filter(InventoryModel.roomtype_id == roomtype_id)\
            .filter(InventoryModel.month == month)\
            .filter(InventoryModel.is_delete == 0)\
            .all()

@staticmethod
@app.task(base=SqlAlchemyTask, bind=True)
def insert_by_year(task_self, merchant_id, hotel_id, roomtype_id, year):
    for month in range(1,13):
        inventory = InventoryModel.get_by_merchant_hotel_roomtype_date(merchant_id, hotel_id, roomtype_id, year, month)
        if inventory:
            continue
        else:
            _month = InventoryModel.combin_year_month(year, month)
            inventory = InventoryModel(merchant_id=merchant_id, hotel_id=hotel_id, roomtype_id=roomtype_id, month=_month)
            task_self.session.add(inventory)
    task_self.session.commit()

@staticmethod
@app.task(base=SqlAlchemyTask, bind=True)
def update(task_self, merchant_id, hotel_id, roomtype_id, year, month, day, price_type, val):
    inventory = InventoryModel.get_by_merchant_id_and_hotel_id_and_date(merchant_id, hotel_id, roomtype_id, year, month)
    if not inventory:
        return
    _val = inventory.get_day(day, price_type)
    if _val + val < 0:
        return

    inventory.set_val_by_day(day, price_type, val)
    task_self.session.commit()



@staticmethod
def combin_year_month(year, month):
    return int("{}{:0>2d}".format(year, month))


def get_day(self, day, type=0):
    if day < 1 or day > 31:
        return 0
    day_key = 'day' + day
    value = getattr(self, day_key)
    return int(value.splite('|')[type])

def set_val_by_day(self, day, price_type, val):
    day_key = 'day' + day
    value = getattr(self, day_key)
    price_reserved, price_manual = value.splite('|')
    if price_type == 0:
        price_reserved = int(price_reserved) + val
    else:
        price_manual = int(price_manual) + val

    value = "{}|{}".format(price_reserved, price_manual)
    setattr(self, day_key, value)




