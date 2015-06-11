# -*- coding: utf-8 -*-

import datetime

from exception.json_exception import InvalidJsonArgumentError

def get_and_valid_arguments(arg_dict, *names):
    for name in names:
        if name not in arg_dict:
            raise InvalidJsonArgumentError(errmsg="缺少参数 " + name)
    return tuple([arg_dict.get(name) for name in names])

def clear_domain_cookie(request, name, domain=None):
    if domain:
        value = "{}=;Domain={}; expires=Mon, 02 Jun 2014 08:44:09 GMT; Path=/".format(name, domain)
    else:
        value = "{}=; expires=Mon, 02 Jun 2014 08:44:09 GMT; Path=/".format(name)

    request.add_header("Set-Cookie", value)


