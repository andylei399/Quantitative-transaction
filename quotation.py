# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 16:22:42 2022

@author: admin
"""
####easyquotation must running @base3.9 
import easyquotation

class quotation:
    def __init__(self):
        self.quotation  =easyquotation.use('sina') #  config_file


    def get_price(self, st='127007'):
        code=[st]
        a = self.quotation.stocks(code)
        print(a)
        bid = []
        ask = []
        for i in range(len(code)):
            c = code[i]
            bid1 = a[c]['bid1']
            ask1 = a[c]['ask1']
            bid.append(bid1)
            ask.append(ask1)

        return [ask[0],bid[0]]


    
        
a = quotation()    
b =a.get_price()
print(b)