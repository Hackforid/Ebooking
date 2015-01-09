# -*- coding: utf-8 -*-

Config = {
    'mysql-connector': 'mysql+mysqlconnector://root:root@192.168.10.15:3306/devine_ebooking?charset=utf8',
}

API = {
    'POI': 'http://192.168.10.15:9000',
    'STOCK': 'http://121.41.23.128:8080/stock2',
    'ORDER': 'http://121.40.120.72:8080/',
}


CHAIN_ID = 6

IS_PUSH_TO_STOCK = False

BROKER_URL = "amqp://admin:admin@localhost:5672/ebooking"
CELERY_RESULT_BACKEND = "amqp://:admin:admin@localhost:5672/ebooking"

LISTENER_IP = "0.0.0.0"

PASSWORD_SALT = "ah%235^2jh135f"
