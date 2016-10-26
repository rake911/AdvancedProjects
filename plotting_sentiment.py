# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 13:58:16 2016

@author: anton
"""
import pandas as pd
import matplotlib.pyplot as plt

xls_file = pd.ExcelFile('output17.xlsx')
volume = xls_file.parse('Volume')
ohlc = xls_file.parse('Sentiment OHLC')
#print volume.head()

# can define grid and subplot sizes using two different ways:
# 1)
'''
plt.figure()
axes1 = plt.subplot2grid((4, 4), (0, 0), colspan=4, rowspan=3)
plt.plot(ohlc['close'])
axes2 = plt.subplot2grid((4, 4), (3, 0), colspan=4)
plt.plot(volume.index, volume['Volume'])
plt.show()
'''

# 2)

import matplotlib.gridspec as gridspec

gs = gridspec.GridSpec(4,4)
ax1 = plt.subplot(gs[:3, :])
plt.plot(ohlc.index, ohlc['close'])
ax2 = plt.subplot(gs[3, :], sharex=ax1)
plt.plot(volume.index, volume['Volume'])
