# -*- coding: utf-8 -*-

from exception.json_exception import InvalidJsonArgumentError

def get_and_valid_arguments(arg_dict, *names):
    for name in names:
        if name not in arg_dict:
            raise InvalidJsonArgumentError(errmsg="缺少参数 " + name)
    return tuple([arg_dict.get(name) for name in names])
