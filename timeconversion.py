# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 09:48:47 2016

@author: anton
"""

import datetime
import time
from pandasexperiments import tweets2
t = tweets2[:10]
#print t
x = datetime.datetime.strptime(t['time'][0], "%a %b %d %H:%M:%S +%f %Y").strftime("%Y-%m-%d %H:%M:%S")
print x