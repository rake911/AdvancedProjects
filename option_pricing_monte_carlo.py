# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 09:21:26 2016

@author: anton
"""
import pandas as pd
import numpy as np
import random

#monte carlo price simulation function
def monte_carlo_price_sim(price, ndays, nreps, plong, pshort, maglong, magshort):
    
    #initial transformations and base matrix creation
    maglong_cents = price/100*maglong
    magshort_cents = -price/100*magshort
    nmatrix = (ndays, nreps)
    simarray = np.ones(nmatrix)
        
    #simulation of price changes
    for i in range(ndays):
        for n in range(nreps):
            simarray[i, n] = random.random()
            if simarray[i, n] >= plong:
                simarray[i, n] = maglong_cents
            elif simarray[i, n] <= pshort:
                simarray[i, n] = magshort_cents
            else:
                simarray[i, n] = 0
    
    #setting initial price and summing over the progression of days    
    simarray[0] = price
    
    for i in range(nreps):
        simarray[:,i] = np.cumsum(simarray[:,i])
        
    # transformation into a pandas dataframe and generation of labels
    colnames = []
    rownames = []
    
    for i in range(nreps):
        colnames.append("rep" + str(i+1))
    for i in range(ndays):
        rownames.append("day" + str(i+1))
    
    simprices = pd.DataFrame(simarray, columns=colnames, index=rownames)
    #output    
    return simprices

#definition of input parameters for ptice simulation
price = 342.75
ndays = 30
nreps = 10000
plong = 0.47
pshort = 0.49
maglong = 1.1
magshort = 0.9

#testing the function        
x = monte_carlo_price_sim(price, ndays, nreps, plong, pshort, maglong, magshort)
'''
for i in range(ndays):
    print x.ix[i].std()
    print x.ix[i].mean()
    print x.ix[i].median()
'''    
import mibian

def callSpread(underPrice, Strike1, Strike2, interestRate, days, impVol1, impVol2):
        leg1 = mibian.BS([underPrice, Strike1, interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, interestRate, days], volatility = impVol2)
        return abs(leg1.callPrice - leg2.callPrice)
        
print "now"        
y = callSpread(x.ix[0].mean(), 345, 350, 0.5, 5, 16, 17)
print y
print "sim"
for i in range(5):
    y = callSpread(x.ix[i].mean(), 345, 350, 0.5, 5-i, 16, 17)
    print y