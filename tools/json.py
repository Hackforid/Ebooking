# -*- coding: utf-8 -*-

import simplejson as json
from datetime import date, datetime


def _default(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)


def json_encode(obj):
    return json.dumps(obj, default=_default)
