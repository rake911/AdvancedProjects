# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 14:02:28 2016

@author: anton
"""

import numpy as np
import scipy.stats as ss
'''
#Black and Scholes
def d1(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r + 0.5*sigma**2) * T)/(sigma * np.sqrt(T))
 
def d2(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r - 0.5*sigma**2) * T)/(sigma * np.sqrt(T))
 
def BlackScholes(type,S0, K, r, sigma, T):
    if type=="C":
        return S0 * ss.norm.cdf(d1(S0, K, r, sigma, T)) - K * np.exp(-r * T) * ss.norm.cdf(d2(S0, K, r, sigma, T))
    else:
        return K * np.exp(-r * T) * ss.norm.cdf(-d2(S0, K, r, sigma, T)) - S0 * ss.norm.cdf(-d1(S0, K, r, sigma, T))
'''
S0 = 342.5
K = 350
r= 0.005
sigma = 0.178
T = 9
Otype='C'



def d1e(S0, K, r, sigma, T):
    return (np.log(S0/K) + (r + 0.5*sigma**2) * T)/(sigma * np.sqrt(T))
 
def d2e(S0, K, r, sigma, T):
    return d1e(S0, K, r, sigma, T) - (sigma * np.sqrt(T))
 
def BlackScholesE(typeo,S0, K, r, sigma, T):
    if typeo=="C":
        return S0 * ss.norm.cdf(d1e(S0, K, r, sigma, T/365)) - K * np.exp(-r * T/365) * ss.norm.cdf(d1e(S0, K, r, sigma, T/365)-sigma*np.sqrt(T/365))
    elif typeo=="P":
        return K * np.exp(-r * T/365) * ss.norm.cdf(-d2e(S0, K, r, sigma, T/365)) - S0 * ss.norm.cdf(-d1e(S0, K, r, sigma, T/365))
    else:
        print "TypeO Error"
        
c_BS = BlackScholesE(Otype,S0, K, r, sigma, T)

print "S0\tstock price at time 0:", S0
print "K\tstrike price:", K
print "c_BS\tBlack-Scholes price:", c_BS