# -*- coding: utf-8 -*-
import hashlib

def generate_password(salt, password):
    m = hashlib.md5()
    m.update(password)
    password = m.hexdigest()

    m = hashlib.md5()
    m.update("{}|{}".format(password, salt))
    password = m.hexdigest()
    return password

if __name__ == '__main__':
    import sys
    print generate_password(sys.argv[1], sys.argv[2])
