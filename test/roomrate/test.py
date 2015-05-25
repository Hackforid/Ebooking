# -*- coding: utf-8 -*-

import sys
import requests
import MySQLdb
import datetime
import random
import time

v = 0

def init_db():
    global db
    if v == 0:
        db = MySQLdb.connect("114.215.87.177", "btw", "btw123", "devine_stock2")
    elif v == 1:
        db = MySQLdb.connect("10.163.118.152", "btw", "btw123", "devine_stock2")
    elif v == 2:
        db = MySQLdb.connect("10.168.251.93", "btw", "btwPassw0rd", "devine_stock2")

def finish():
    global db
    db.close()


def get_stock_roomrate(roomrate, date):
    global db
    column = 'month%d' % date.month
    SQL = 'SELECT %s from RoomRate \
           WHERE ChainId = %d AND ChainHotelId = %s AND ChainRoomTypeId = %s AND ChainRatePlanId = %s '\
          % (column, 6, roomrate['hotel_id'], roomrate['roomtype_id'], roomrate['rate_plan_id'])
    print SQL
    cursor = db.cursor()
    try:
        cursor.execute(SQL)
        result = cursor.fetchone()
        if result:
            prices = result[0]
            print prices
            return prices
    except Exception, e:
        raise Exception('db error')
    finally:
        db.commit()
        cursor.close()

def valid_stock_price(prices, date, price):
    price_arr = prices.split('|')
    price_stock = int(price_arr[date.day-1].split(',')[0])
    if price == price_stock:
        print 'SUCCESS'
    else:
        print '%d %d' % (price, price_stock)
        raise Exception('NOOOOOOOO')


def start_request(data):
    if v == 0:
        url = 'http://ebookingtest.betterwood.com/api/inner/test/roomrate/'
    elif v == 1:
        url = 'http://127.0.0.1:9501/api/inner/test/roomrate/'
    elif v == 2:
        url = 'http://10.168.234.38:9701/api/inner/test/roomrate/'
    r = requests.put(url, json=data)
    if r.status_code == 200:
        roomrate = r.json()['result']['roomrate']
        return roomrate
    else:
        raise Exception('request fail')



def test_roomrate(merchant_id, roomrate_id):
    date = datetime.date.today()
    price = random.randint(100, 1000) * 100
    json_args = {
            'merchant_id': merchant_id,
            'roomrate_id': roomrate_id,
            'price': price,
            'start_date': str(date),
            'end_date': str(date),
            }
    print json_args
    roomrate = start_request(json_args)
    prices = get_stock_roomrate(roomrate, date)
    valid_stock_price(prices, date, price)

def test(merchant_id, roomrate_id):
    for i in xrange(1, 1000):
        print 'test %d' % i
        test_roomrate(merchant_id, roomrate_id)

def main():
    global v
    merchant_id = sys.argv[1]
    roomrate_id = sys.argv[2]
    if len(sys.argv) == 4:
        v = int(sys.argv[3])
    init_db()
    test(merchant_id, roomrate_id)
    finish()


if __name__ == '__main__':
    main()
