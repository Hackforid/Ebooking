# -*- coding: utf-8 -*-

import time

class Pusher(object):

    def __init__(self, db):
        self.db = db

    def generate_track_id(self, data):
        return "{}|{}".format(data, time.time())
