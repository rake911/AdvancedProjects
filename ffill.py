# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 13:05:53 2016

@author: anton
"""
import numpy as np
import pandas as pd
from pandas import Series, DataFrame 

hourly_corn_xls_file = pd.ExcelFile('hourly_corn_price.xlsx')
hourly_corn_price = hourly_corn_xls_file.parse('Sheet1')

corn_index = hourly_corn_price['Date (GMT)']
hourly_corn_price.index = corn_index
corn = hourly_corn_price.drop('Date (GMT)', axis=1)
corn['Percent']=corn['Last'].pct_change()
corn2 = corn.drop(['Open', 'High', 'Low', 'Last'], axis=1)
corn2 = corn2.reindex(corn2.index.rename('time'))
#print corn2.head()

corn3 = corn2.resample('S', fill_method='ffill')
#print corn3.tail()

corn4 = corn3.resample('4h', how='ohlc')
print corn4.tail()

