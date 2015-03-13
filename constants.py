# -*- coding: utf-8 -*-

from tornado.util import ObjectDict

PERMISSIONS = ObjectDict({
    'admin'                    : (1<<0),
    'update_order'             : (1<<1),
    'view_order'               : (1<<2),
    'view_cooperated_hotel'    : (1<<3),
    'choose_hotel'             : (1<<4),
    'inventory'                : (1<<5),
    'pricing'                  : (1<<6),
    'order_statistics'         : (1<<7),
    'income_statistics'        : (1<<8),
    'update_password'          : (1<<9),
    'root'                     : (1<<10),
})

#Celery Queue
QUEUE_DEFAULT = "DEFAULT"
QUEUE_ORDER = "ORDER"
QUEUE_STOCK_PUSH = "ORDER_STOCK_PUSH"

CHAIN_ID = 6

OTA = {
    1: u'去哪儿(优品房源)',
    2: u'淘宝旅行',
    3: u'美团',
    4: u'携程(预付)',
    5: u'艺龙',
    6: u'去哪儿(酒店联盟)',
    7: u'去哪儿(快团)',
    8: u'去哪儿(酒店直销)',
    9: u'百达屋',
    10: u'携程(团购)',
}

BED_TYPE = {
    0: u'单床',
    1: u'大床',
    2: u'双床',
    3: u'三床',
    4: u'三床（1大2单）',
    5: u'榻榻米',
    6: u'拼床',
    7: u'水床',
    8: u'榻榻米双床',
    9: u'榻榻米单床',
    10: u'圆床',
    11: u'上下铺',
    12: u'大床活双床',
    -1: u'未知',
}
