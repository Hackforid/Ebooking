# -*- coding: utf-8 -*-

def add_get_params(url, params):
    r = url
    query = '&'.join(['='.join((key, str(params.get(key)))) for key in params if params.get(key) is not None])
    if query is not None:
        r = r + '?' + query

    return r
