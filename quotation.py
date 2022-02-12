# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 16:22:42 2022

@author: admin
"""

import easyquotation

class quotation:
    def __init__(self):
        self.quotation  =easyquotation.use('sina') #  config_file

    # def get_price(self, code=['127007', '110064'], is_ask=1):
    #     a = self.quotation.stocks(code)
    #     bid = []
    #     ask = []
    #     for i in range(len(code)):
    #         c = code[i]
    #         bid1 = a[c]['bid1']
    #         ask1 = a[c]['ask1']
    #         bid.append(bid1)
    #         ask.append(ask1)

    #     if(is_ask):
    #         return ask
    #     else:
    #         return bid


    def get_price(self, st='127007'):
        code=[st]
        a = self.quotation.stocks(code)
        bid = []
        ask = []
        for i in range(len(code)):
            c = code[i]
            bid1 = a[c]['bid1']
            ask1 = a[c]['ask1']
            bid.append(bid1)
            ask.append(ask1)

        #if(is_ask):
        return [ask[0],bid[0]]
        #else:
        #    return bid[0]

# a = quotation()
# st =   ['127007', '110064']      
# aaa = a.get_price(st,1)
# print(aaa)
        
        
    