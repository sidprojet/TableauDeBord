#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 11:19:42 2018

@author: formationsid
"""
import json
from twython import Twython
APP_KEY : 'spCeZNMn8cwFX3HWoGT10LClp'
APP_SECRET : 'C0j8qy2w234kEclWzX1foRspQRtHXwFEgS9hgf1QJNsMhsY60Z'
OAUTH_TOKEN : '2469788862-7D84Hu84zheUAeJ2zCfdsm9hRvquXrVknrO1ArL'
OAUTH_TOKEN_SECRET : 'u8cDBsEoDllNPRULvDPGFbFZYxcWQwuWPrYg8NBDn3Qmq'
twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
timeline = twitter.get_timeline()
print (json.dumps(timeline))