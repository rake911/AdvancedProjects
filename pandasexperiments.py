# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:21:41 2016

@author: anton
"""
import pandas as pd
import datetime
import random
import matplotlib.pyplot as plt

# import the data we collected and arranged into pd dataframe
# drop all the irrelevant data
# assign new index to the text of the tweets by the time of their posting
# reformat time of the tweets into the format of reuters data

from granstweets4 import tweets

tweets = tweets[tweets['corn'] == True]
tweets2 = tweets.drop(['lang', 'soybean', 'wheat', 'link', 'corn'], axis=1)

# iterrows works as iteration over indexed items in a dataframe/series

def pandas_to_reuters_time(data):
    return datetime.datetime.strptime(data, 
           "%a %b %d %H:%M:%S +%f %Y").strftime("%Y-%m-%d %H:%M:%S")
    
for index, row in tweets2.iterrows():
    tweets2['time'][index] = pandas_to_reuters_time(tweets2['time'][index])    

re_index = tweets2['time']
tweets2.index = re_index
tweets3 = tweets2.drop('time', axis=1)

# import the excel file with the hourly prices of the corn future
# assign new index to the table for date and time
# add percent changes to the data calculated from last prices
# drop the irrelevant data

hourly_corn_xls_file = pd.ExcelFile('hourly_corn_price.xlsx')
hourly_corn_price = hourly_corn_xls_file.parse('Sheet1')

corn_index = hourly_corn_price['Date (GMT)']
hourly_corn_price.index = corn_index
corn = hourly_corn_price.drop('Date (GMT)', axis=1)

corn['Percent']=corn['Last'].pct_change()
corn2 = corn.drop(['Open', 'High', 'Low', 'Last'], axis=1)
corn2 = corn2.reindex(corn2.index.rename('time'))
corn3 = corn2.resample('S', fill_method='ffill')

# join the tables
tweets_prices = tweets3.join(corn3)
tweets_prices['Probability'] = [(0.5-random.random()) for i in range(len(tweets_prices['text']))]
tweets_prices['Cumsum_Prob'] = tweets_prices['Probability'].cumsum()

tweets_prices['Count'] = 1
tweets_volume = tweets_prices['Count'].resample('1h', how='sum')
tweets_sentiment_ohlc = tweets_prices['Cumsum_Prob'].resample('1h', how='ohlc')
#print tweets_sentiment_ohlc.tail() 
#print tweets_volume.tail()


fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 3)
ax1.plot(tweets_sentiment_ohlc['close'], 'k')
ax2.plot(tweets_volume)

#tweets_volume.plot(kind='bar')
#tweets_sentiment_ohlc['close'].plot()
'''
from pandas import ExcelWriter
writer = ExcelWriter('output17.xlsx')
tweets_volume.to_excel(writer,'Sheet1')
tweets_sentiment_ohlc.to_excel(writer, 'Sheet2')
writer.save()
'''