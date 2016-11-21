#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 10:20:51 2016

@author: anton
"""
import mibian

class Strategy(object):
    
    interestRate = 0.5
    
    def __init__(self, underPrice, Strike1, Strike2, Strike3, Strike4, days, impVol1, impVol2, impVol3, impVol4):
        self.underPrice = underPrice
        self.Strike1 = Strike1
        self.Strike2 = Strike2
        self.Strike3 = Strike3
        self.Strike4 = Strike4
        self.days = days
        self.impVol1 = impVol1
        self.impVol2 = impVol2
        self.impVol3 = impVol3
        self.impVol4 = impVol4

class volStrategy(Strategy):
    
    def __init__(self, stype):
        self.ftype = stype

    def straddle(underPrice, Strike, days, impVol):
        leg = mibian.BS([underPrice, Strike, Strategy.interestRate, days], volatility = impVol)
        return leg.callPrice + leg.putPrice

    def strangle(underPrice, Strike1, Strike2, days, impVol1, impVol2):
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        if Strike1 >= Strike2:
            return leg1.callPrice + leg2.putPrice
        else:
            return leg1.putPrice + leg2.callPrice

class statStrategy(Strategy):
    
    def __init__(self, stype):
        self.ftype = stype
    
    def leverage():
        return self - (Strategy.Strike1 - Strategy.Strike2)               
        
class spread(statStrategy):
    
    def __init__(self, ftype):
        self.ftype = ftype
        
    def callSpread(underPrice, Strike1, Strike2, days, impVol1, impVol2):
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        return abs(leg1.callPrice - leg2.callPrice)
    
    def putSpread(underPrice, Strike1, Strike2, days, impVol1, impVol2):
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        return abs(leg1.putPrice - leg2.putPrice)

class fly(statStrategy):

    def __init__(self, ftype):
        self.ftype = ftype       
            
    def atmFly(underPrice, Strike1, Strike2, Strike3, days, impVol1, impVol2, impVol3):
        
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        leg3 = mibian.BS([underPrice, Strike3, Strategy.interestRate, days], volatility = impVol3)
        
        if Strike1 >= Strike3:
            return leg1.callPrice + leg3.putPrice - (leg2.callPrice + leg2.putPrice)
        else:
            return leg1.putPrice + leg3.callPrice - (leg2.callPrice + leg2.putPrice)
        
    def callFly(underPrice, Strike1, Strike2, Strike3, days, impVol1, impVol2, impVol3):
    
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        leg3 = mibian.BS([underPrice, Strike3, Strategy.interestRate, days], volatility = impVol3)
        
        return leg1.callPrice + leg3.callPrice - 2*leg2.callPrice
    
    def putFly(underPrice, Strike1, Strike2, Strike3, days, impVol1, impVol2, impVol3):
    
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        leg3 = mibian.BS([underPrice, Strike3, Strategy.interestRate, days], volatility = impVol3)
        
        return leg1.putPrice + leg3.putPrice - 2*leg2.putPrice       
    

class condor(statStrategy):
    
    def __init__(self, ftype):
        self.ftype = ftype       
            
    def atmCondor(underPrice, Strike1, Strike2, Strike3, Strike4, 
             days, impVol1, impVol2, impVol3, impVol4):
        
        return volStrategy.strangle(underPrice, Strike1, Strike4, days, impVol1,
                                    impVol4) - volStrategy.strangle(underPrice, Strike2, Strike3, 
                                                                    days, impVol2, impVol3) 
        
    def callCondor(underPrice, Strike1, Strike2, Strike3, Strike4, 
                   days, impVol1, impVol2, impVol3, impVol4):
    
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        leg3 = mibian.BS([underPrice, Strike3, Strategy.interestRate, days], volatility = impVol3)
        leg4 = mibian.BS([underPrice, Strike4, Strategy.interestRate, days], volatility = impVol4)
        
        return leg1.callPrice + leg3.callPrice - leg2.callPrice - leg4.callPrice
    
    def putCondor(underPrice, Strike1, Strike2, Strike3, Strike4, 
                  days, impVol1, impVol2, impVol3, impVol4):
    
        leg1 = mibian.BS([underPrice, Strike1, Strategy.interestRate, days], volatility = impVol1)
        leg2 = mibian.BS([underPrice, Strike2, Strategy.interestRate, days], volatility = impVol2)
        leg3 = mibian.BS([underPrice, Strike3, Strategy.interestRate, days], volatility = impVol3)
        leg4 = mibian.BS([underPrice, Strike4, Strategy.interestRate, days], volatility = impVol4)
        
        return leg1.putPrice + leg3.putPrice - leg2.putPrice - leg4.putPrice