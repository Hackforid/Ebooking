# -*- coding: utf-8 -*-

import datetime
from time import mktime
import simplejson as json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        return json.JSONEncoder.default(self, obj)



def json_encode(obj):
    return json.dumps(obj, cls=DateTimeEncoder)



