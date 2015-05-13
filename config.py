# -*- coding: utf-8 -*-

Config = {
    'mysql-mysqldb': 'mysql+mysqldb://root:root@192.168.10.15:3306/devine_ebooking?charset=utf8',
    'mysql-connector': 'mysql+mysqlconnector://root:root@192.168.10.15:3306/devine_ebooking?charset=utf8',
    'mysql-pymysql': 'mysql+pymysql://root:root@192.168.10.15:3306/devine_ebooking?charset=utf8',
}

API = {
    #'POI': 'http://115.28.43.75:9001',
    'POI': 'http://127.0.0.1:9001',
    'STOCK': 'http://121.41.23.128:8080/stock2',
    'ORDER': 'http://121.40.120.72:8080/',
    'ORDER_VALID': 'http://192.168.50.4:8080',
}


IS_PUSH_TO_STOCK = False
IS_PUSH_TO_POI = True

BROKER_URL = "amqp://admin:admin@localhost:5672/ebooking"
CELERY_RESULT_BACKEND = "amqp://:admin:admin@localhost:5672/ebooking"

LISTENER_IP = "0.0.0.0"

PASSWORD_SALT = "google"

COOKIE_SALT = "you never know me"

ORDER_CONTACTS = [
        '13071218832', '18513956997',
        ]

SPEC_STOCK_PUSH = {
        21: 13,
        }

BACKSTAGE_HOST = 'http://121.42.8.247:8080'
BACKSTAGE_USERNAME_KEY = "test_op_username"
BACKSTAGE_ENABLE = False

BACKSTAGE_PERMISSIONS = {
        'admin': 63,
        }

