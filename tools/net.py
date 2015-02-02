# -*- coding: utf-8 -*-

import requests
from requests.adapters import HTTPAdapter

from config import API

req = requests.Session()
req.mount(API['POI'], HTTPAdapter(max_retries=5))
req.mount(API['STOCK'], HTTPAdapter(max_retries=5))
req.mount(API['ORDER'], HTTPAdapter(max_retries=5))
