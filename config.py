# -*- coding: utf-8 -*-

Config = {
    'mysql-connector': 'mysql+mysqlconnector://btw:btw@10.171.249.95:3306/devine_ebooking?charset=utf8',
}

API = {
    'POI': 'http://121.41.112.197:9001',
    'STOCK': 'http://121.41.23.128:8080/stock2',
    'ORDER': 'http://121.40.120.72:8080/',
}


CHAIN_ID = 6

IS_PUSH_TO_STOCK = True

BROKER_URL = "amqp://devine:devine@10.251.251.192:5672/ebooking"
CELERY_RESULT_BACKEND = "amqp://:devine:devine@10.251.251.192:5672/ebooking"
