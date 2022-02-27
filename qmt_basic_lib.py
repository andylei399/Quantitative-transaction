# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 20:39:07 2021

@author: admin
"""

import pandas as pd
import numpy as np


class qmt_basic_lib:
    def __init__(self,debug=0,file='aaaa.csv',drop=0):
        print("init qmt_basic_lib begin")
#        head=['BOND_ID','stratgy_name',	'bond_nm','postions','stock_id'	,'convert_price','bond_id']
#        if (debug==1):
#            data0=['111001.SH','A','山玻转债',np.NAN,'605006.SH',1.1,'111001.SH']
#            data1=['113632.SH','A','鹤21转债',np.NAN,'603733.SH',2.1,'113632.SH']
#            data=[data0,data1]
#            df1 = pd.DataFrame(data,columns=head)
#            df1.set_index('BOND_ID',inplace=True)
#            df1.columns.name='COLUMN_NAME'
#            df1.index.name='BOND_ID'  ###it is must ,otherwise the csv to df will has more columns
#        
#            #print(df1)
#            self.df = df1.copy()
#        else:
#            #data=[]
#            self.csv2df(file)
#            for i in ['bond_price','prem','put_convert_price','force_redeem_price','last_time','dblow','stock_nm','stock_price']:
#                if(drop):
#                    self.drop_column(i)
loc[]            

    def df_filter(self,columname,N=0):
            if N==0:
                b=self.df[columname]==True
            else:
                b=self.df[columname]<=N                
            return self.df[b]

    def csv2df(self,file): ### the csv file must be stored in df
        df1 = pd.read_csv(file,encoding='gbk')
        df1.set_index('BOND_ID',inplace=True)
        df1.columns.name='COLUMN_NAME'
        df1.index.name='BOND_ID'  ###it is must ,otherwise the csv to df will has more columns
        self.df=df1.copy()

    def df2csv(self,file):  ### the df must has the index ...
        self.df.to_csv(file,encoding='gbk')
        

    def drop_row(self,rowname):
        self.df.drop([rowname],axis=0,inplace=True)
 
    def drop_column(self,columnname):
        self.df.drop([columnname],axis=1,inplace=True)
        
    def add_column(self,columnname='CA'):        
        len1 = len(self.df.index)
        tmp=[]
        for i in range(len1):
            tmp.append(np.nan)
            
        self.df[columnname]=tmp

    def add_row(self,rowname='CA'):
        len1 = len(self.df.columns)
        tmp=[]
        for i in range(len1):
            tmp.append(np.nan)
            
        self.df.loc[rowname] = tmp     
        
#    def print1(self,df):
#        import sys
#        log = open('log.txt','w')
#        sys.stdout = log
#        print(df)
        

    def copy(self,inst):
        self.df=inst.df.copy()
        self.hold_cnt = inst.hold_cnt
        
    def get_pixel(self,rowname,columnname):
        return self.df[columnname][rowname]
        
    def get_row(self,rowname):
        return self.df.loc[rowname].copy()

    def get_column(self,columnname):
        return self.df[columnname].copy()
    
    def write_pixel(self,rowname,columnname,dat=np.nan):
        self.df[columnname][rowname] = dat
        
    def write_row(self,rowname,rowvalue=np.nan):
        self.df.loc[rowname] = rowvalue

    def write_column(self,columnname, columnvalue=np.nan):
        self.df[columnname] = columnvalue
        
    def get_minN(self,columnname,N,newname):
        tmp = self.get_column(columnname).copy()
        symbols=tmp.nsmallest(N).index
        tmp[:]=False #np.nan
        tmp[symbols]=True
        self.df[newname] = tmp
        
    def get_maxN(self,columnname,N,newname):
        tmp = self.get_column(columnname).copy()
        symbols=tmp.nlargest(N).index
        tmp[:]=False #np.nan
        tmp[symbols]=True
        self.df[newname] = tmp

    def set_rank(self,columname):
        ranks= self.df[columname].rank(method='first',ascending=True)
        newname = columname+'_rank'
        self.df[newname] = ranks

#    def displayall(self):
#        #pd.set_option('display.max_columns',30)
#        #pd.set_option('display.width', 200)
#        #pd.set_option('display.max_rows',None)   
#        print("display option")

#    def get_cash(self,file):
#        self.cash_df = pd.read_csv(file,encoding='gbk')
#        self.cash_df.set_index('AAA',inplace=True)
#        self.cash_df.columns.name='COLUMN_NAME'
#        self.cash_df.index.name='AAA' 
#        
#        a =self.cash_df['cash']
#        b =self.cash_df['max_value']
#        c=self.cash_df['capital']
#        self.cash     = a[0] #cash_df['cash']
#        self.max_value= b[0] #cash_df['max_value']     
#        self.capital  = c[0]



#    def write_cash(self,file):
#        self.cash_df['cash'][0] = self.cash
#        self.cash_df['max_value'][0] = self.max_value 
#        self.cash_df['capital'][0] = self.capital 
#        self.cash_df.to_csv(file,encoding='gbk')
        
#    def get_market(self,columnname,QMT=0,period ='realtime',count=-1):  ##period='realtime'/'1d'/'1h' ,count=-1表示当前，count=1~N表示向前取的个数
#        import random
#        code1 = self.df[columnname]
#        code2=[]
#        for i in code1:
#            code2.append(i)
#        price=[]
#        cnt=1
#        if QMT:
#            print("QMT is running")
#            #price = ContextInfo.get_market_data(['close'], stock_code =code2 , skip_paused = False, period =period,count) 
#            #code_price=columnname + "_price"
#            #self.df[code_price] = price
#        else:
#            for i in self.df['bond_id']:
#                p = cnt #float(random.randint(5,200))
#                price.append(p )
#                cnt=cnt + 1
#            code_price=columnname + "_price"
#            self.df[code_price] = price
 
#    def cal_dlow(self, prem_cof,bprice_cof):
#        sprice = self.df['stock_id_price']
#        bprice = self.df['bond_id_price']
#        cprice = self.df['convert_price']
#        
#        stock_num = 100 / cprice
#        value = sprice * stock_num
#        prem = bprice / value - 1
#        dlow = prem*prem_cof + bprice * bprice_cof
#        self.df['new_dlow'] = dlow

#    def cal_increase(self):
#        stock_1d = self.get_market('stock_id',period='1d',count=1)
#        bond_1d  = self.get_market('bond_id',period='1d',count=1)
#        self.write_column('stock_1d_price',stock_1d)
#        self.write_column('bond_1d_price',bond_1d)
#        stock_inc =self.df['stock_id_price'] / self.df['stock_1d_price'] -1 
#        bond_inc =self.df['bond_id_price']  / self.df['bond_1d_price'] -1 
#        self.write_column('stock_inc',stock_inc)
#        self.write_column('bond_inc',bond_inc)
        


    
#    def check_position(self,qmt_basic_lib_inst,columname):
#        self.df['hold']=self.df['postions']>0
#        self.hold_cnt = 0
#        print('hold')
#        self.displayall()
#        print(self.df_filter('hold'))
#        print('new ')
#        print(qmt_basic_lib_inst.df_filter(columname))
#
#        overlap=[]
#        for i in self.df['bond_id']:
#            a = qmt_basic_lib_inst.get_pixel(i, columname)
#            b= self.get_pixel(i, 'hold')
#            if (a==True) and (b ==True):
#                overlap.append(True)
#                self.hold_cnt = self.hold_cnt + 1
#            else:
#                overlap.append(False)
#            
#        self.df['overlap'] = overlap

    
#    def cal_target_lots(self,max_capital,max_stock_nums):
#        
#        a=0
#        b=0
#        self.add_column('op_lots')
#        self.add_column('op')  
#        
#        for i in self.df['bond_id']:
#            hold    = self.get_pixel(i, 'hold')
#            overlap = self.get_pixel(i, 'overlap')    
#            price = self.get_pixel(i, 'bond_id_price')
#            pos  =self.get_pixel(i, 'postions')
#            if (hold==True ) and (overlap==True):
#                a= a + price * pos
#                self.write_pixel(i, 'op',False)
#                self.write_pixel(i, 'op_lots',0 )
#                
#            if (hold==True ) and (overlap==False):
#                b =b + price *pos
#                self.write_pixel(i, 'op',True)
#                aa = 0 - self.get_pixel(i,'postions')
#                self.write_pixel(i, 'op_lots',aa )                
#
#        sub1 = max_stock_nums - self.hold_cnt
#        capital = self.cash + b*0.99
#        if(capital+a>self.max_value):
#            capital = self.max_value - a
#            
#        if sub1==0:
#            ave = (capital+a) / self.hold_cnt
#        else:
#            ave = capital / sub1 
#        
#        for i in self.df['bond_id']:
#            hold    = self.get_pixel(i, 'hold')
#            overlap = self.get_pixel(i, 'overlap')    
#            price = self.get_pixel(i, 'bond_id_price')
#           
#            if (hold==False) :
#                aa = ave / price/10 #self.get_pixel(i, 'postions') 
#                bb = int(aa) * 10
#                self.write_pixel(i, 'op',True)
#                self.write_pixel(i, 'op_lots',bb )  
#        
#
#    def cal_target_lots2(self,max_capital,max_stock_nums):
#        
#        a=0
#        b=0
#        self.add_column('op_lots')
#        self.add_column('op')  
#        
#        for i in self.df['bond_id']:
#            hold    = self.get_pixel(i, 'hold')
#            overlap = self.get_pixel(i, 'overlap')    
#            price   = self.get_pixel(i, 'bond_id_price')
#            pos     = self.get_pixel(i, 'postions')
#            if (hold==True ) and (overlap==True):
#                a= a + price * pos
#                
#            if (hold==True ) and (overlap==False):
#                b =b + price *pos
#       
#
#        capital = self.cash + b*0.99 + a *0.99
#        if(capital>self.max_value*0.99):
#            capital = self.max_value*0.99
#        self.capital = capital
#        
#        self.cash = self.max_value - self.capital
#        ave = capital/ max_stock_nums 
#
#     
#        for i in self.df['bond_id']:
#            hold    = self.get_pixel(i, 'hold')
#            overlap = self.get_pixel(i, 'overlap')    
#            price   = self.get_pixel(i, 'bond_id_price')
#           
#            if (hold==False) :###买入
#                bb = int(ave / price) #self.get_pixel(i, 'postions') 
#                self.write_pixel(i, 'op',True)
#                self.write_pixel(i, 'op_lots',bb )  
#                
#            if (hold==True ) and (overlap==True): ###买入或者卖出
#                c1 = self.get_pixel(i,'postions')
#                bb = int(ave / price - c1) #self.get_pixel(i, 'postions') 
#                
#                if(abs(bb)> 0.2*c1):
#                    self.write_pixel(i, 'op',True)
#                    self.write_pixel(i, 'op_lots',bb )  
#
#            if (hold==True ) and (overlap==False):###卖出
#                self.write_pixel(i, 'op',True)
#                aa = 0 - self.get_pixel(i,'postions')
#                self.write_pixel(i, 'op_lots',aa )  
                

#    def order_LOTS(self,code,lots,price,context,accid):
#        if lots>0:
#            print("BUY,code=%s,lots=%06d,price=%.05f,context=%s,accid=%s\n" % (code,lots,price,context,accid ))
#        else:
#            print("Sell,code=%s,lots=%06d,price=%.05f,context=%s,accid=%s\n" % (code,lots,price,context,accid ))  
#    
#
#    def order_send(self,ContextInfo,accID):  #
#        for i in self.df['bond_id']:
#            op = self.get_pixel(i, 'op')
#            price1 = self.get_pixel(i, 'bond_id_price')
#            if op==True:
#                lots = self.get_pixel(i, 'op_lots')
#                self.order_LOTS(i,lots,price1,ContextInfo,accID)
#                #a1 = self.get_pixel(i,'postions')
#                #b1 = a1 + lots
#                #self.write_pixel(i,'postions',b1)
#
#  
#
#    def get_all_order_id(self):
#        print("return all order ID")
#        
#    def get_order_value(self,order_id):      
#        print("return all order ID")
#        
#    def get_all_order_value(self):
#        ID= self.get_all_order_id()
#        va=[]
#        for i in ID:
#            v= self.get_order_value(i)
#            va.append(v)
#        return va        
