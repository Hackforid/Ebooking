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
    'user_manage'              : (1<<9),
    'update_password'          : (1<<10)
})

