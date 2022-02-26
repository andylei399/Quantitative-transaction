# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 19:58:21 2021

@author: admin
"""
#from jisilu_lib import jisilu_lib
from qmt_basic_lib import qmt_basic_lib


# max_stock_nums=10 ###
# M=15####
# prem_cof=100  ##
# bprice_cof=1  ###
# pos_file='pos.csv'  ####
# stratgy_name='A'  ####
# max_capital = 1000000  ##
# ContextInfo='leizhijie'  ###
# accID='006354'   #####
# Mode= 0  ### 0: prem/dlow , 1:increase_diff 
# turn= 1  ## 1 : 1h , 2: 2h , 24:1day turn, it can used outside .....


class qmt_lib:
    def __init__(self,bond_nums,threshold,prem_coef,price_coef,record_file,stratgy_name,max_capital,Info,accID,Mode,lookup_csv,recordfile,accountfile):
        self.max_stock_nums=bond_nums ###
        self.M             =threshold ####
        self.prem_cof      =prem_coef  ##
        self.bprice_cof    =price_coef  ###
        self.pos_file      =record_file ####
        self.stratgy_name  =stratgy_name ####
        self.max_capital   =max_capital  ##
        self.ContextInfo   =Info  ###
        self.accID         =accID #####
        self.Mode          =Mode  ### 0: prem/dlow , 1:increase_diff 
        self.lookup_csv    =lookup_csv 
        self.u0            ='no data'
        self.p0            ='no positions'
        self.recordfile    =recordfile 
        self.accountfile   =accountfile
        self.print1(self.recordfile)
        
        self.record = []
        self.pos =[]

    def print1(self,df):  ###this can pointer print to log file
        import sys
        log = open('log.txt','w')
        sys.stdout = log
        print(df)

    def write_record(self):
        newpos = self.newpos_df.copy()
        record = self.new_record_df.copy()
        
        newpos.to_csv(self.pos_file  ,encoding='gbk')
        record.to_csv(self.recordfile,encoding='gbk')
                
        #import pandas as pd
        #pd.set_option('display.max_rows',None)   
        print("final pos file")
        print(newpos)        
        # print('newpos')
        # print(newpos.df)
        print('final record file')
        print(record)

    def get_lookup_df(self):
        self.u0 = qmt_basic_lib(file=self.lookup_csv,drop=1)
        self.u0.get_market('stock_id')
        self.u0.get_market('bond_id')
        self.u0.cal_dlow(self.prem_cof,self.bprice_cof)
        self.u0.set_rank('new_dlow')     
        self.u0.add_column('postions')
        bd = self.u0.get_column('bond_id')
        for i in bd:
            self.u0.write_pixel(i,'postions',0)
        
    def get_pos_df(self):
        self.p0 = qmt_basic_lib(file=self.pos_file)  ##def check_position(df1,pos_file): add to 
        print("posfile:")
        print(self.p0.df)
        self.p0.get_market('stock_id')
        self.p0.get_market('bond_id')        
        self.p0.pos_filter()        
        self.p0.get_cash(self.accountfile)
        bd = self.p0.get_column('bond_id')
        acc=0
        for i in bd:
            p =self.p0.get_pixel(i, 'bond_id_price')
            n = self.p0.get_pixel(i, 'postions')
            acc = acc+ p*n
        self.p0.capital = acc 
        
    def get_expect_df(self):
        money = self.p0.cash + self.p0.capital
        ave = money / self.max_stock_nums
        bd = self.lowestN_df['bond_id']
        for i in bd:
            num = ave / self.u0.get_pixel(i, 'bond_id_price')
            self.lowestN_df['postions'][i] =int(num)

            
    def get_sub_df(self):
        bd1 = self.lowestN_df.copy()
        bd2 = self.pos_df.copy()
        bd1_drop = ['bond_nm' , 'convert_price'  ,  'bond_id'  , 'stock_id' , 'stock_id_price','bond_id_price'  ,'new_dlow' , 'new_dlow_rank' ]
        bd1.drop(bd1_drop,axis=1,inplace=True)
        bd2_drop = ['stratgy_name','bond_nm','stock_id','convert_price','bond_id','stock_id_price','bond_id_price']
        bd2.drop(bd2_drop,axis=1,inplace=True)
        
        sub_df = bd1 - bd2
        item = sub_df.index
        for i in item:
            if (i not in bd1.index) and (i in bd2.index):
                sub_df['postions'][i] = 0 - bd2['postions'][i]
            if (i  in bd1.index) and (i not in bd2.index):
                sub_df['postions'][i] =  bd1['postions'][i]                
                
        self.buy_df  = sub_df.copy()
        self.sell_df = sub_df.copy()       
        
        for i in self.buy_df.index:
            p = self.buy_df['postions'][i]
            if p<=0:
                print('drop i=%s' % i)
                self.buy_df.drop([i],axis=0,inplace=True)
        
        for i in self.sell_df.index:
            p = self.sell_df['postions'][i]
            if p>=0:
                print('drop i=%s' % i)
                self.sell_df.drop([i],axis=0,inplace=True)
            else:
                #M_df = self.lowestM_df.index
                inside=0
                for j in self.lowestM_df.index:
                    if j==i:
                        inside=1
                        break
                if inside==1:
                    print('drop i=%s' % i)
                    self.sell_df.drop([i],axis=0,inplace=True)       

                
        print('sell df')
        print(self.sell_df)
        print('buy df')
        print(self.buy_df)

    def order_LOTS(self,code,lots,context,accid):
        print("pos_df11")
        print(self.pos_df)
        
        if lots>0:
            print("BUY,code=%s,lots=%06d,price=%.05f,context=%s,accid=%s\n" % (code,lots,0,context,accid ))
            bd_nm = self.lowestM_df['bond_nm'][code]
        else:
            print("Sell,code=%s,lots=%06d,price=%.05f,context=%s,accid=%s\n" % (code,lots,0,context,accid ))  
            bd_nm = self.pos_df['bond_nm'][code]

        #bd_nm = self.lowestM_df['bond_nm'][code]
        print("bd_nm=%s" % (bd_nm))
        if lots<0:
            bd_price = self.pos_df['bond_id_price'][code]
        else:
            bd_price = self.lowestN_df['bond_id_price'][code] 
            
        record1=['A',bd_nm,code,bd_price,lots]
        # = ['stratgy_name','bond_nm','bond_id','bond_price','lots']
        self.record.append(record1)
        #self.add_record(code, record1)
        
        
        ######update pos
    def setup_record_df(self):
        import pandas as pd
        data = self.record
        head=['stratgy_name','bond_nm','bond_id','bond_price','lots'] #['BOND_ID','stratgy_name',	'bond_nm','postions','stock_id'	,'convert_price','bond_id']
        df1 = pd.DataFrame(data,columns=head)
        df1.set_index('bond_id',inplace=True)
        df1.columns.name='COLUMN_NAME'
        df1.index.name='bond_id' 
        self.new_record_df = df1.copy()

    def test_exist(self,df,rowname,colunname):
        index1 = df.index
        column1 = df.columns 
        if (rowname in index1) and (colunname in column1):
            return True
        else:
            return False
        
        
           

    def setup_new_pos_df(self):
        newpos_df = self.pos_df.copy()
        print("new_record_df")
        print(self.new_record_df)
        for i in self.new_record_df.index:
            bd_nm = self.new_record_df['bond_nm'][i]
            bd_p  = self.new_record_df['bond_price'][i]
            lots =  self.new_record_df['lots'][i]
            
            if self.test_exist(self.lowestN_df,i,'stock_id'):
                stock_id = self.lowestN_df['stock_id'][i]
            else:
                stock_id = self.pos_df['stock_id'][i]
                
            if self.test_exist(self.lowestN_df,i,'convert_price'):
                cov_p = self.lowestN_df['convert_price'][i]
            else:
                cov_p = self.pos_df['convert_price'][i]
                
            #stock_id = self.lowestN_df['stock_id'][i]
            #cov_p    = self.lowestN_df['convert_price'][i]
            
            inside=0
            for j in self.pos_df.index:
                if i==j:
                    inside=1
                    
            if inside==1:
                postion = self.pos_df['postions'][i] + self.new_record_df['lots'][i]
                if postion>0:
                    newpos_df['postions'][i] = postion
                else:
                    newpos_df.drop([i],axis=0,inplace=True)
            else:
                newpos_df.loc[i] = ['A',bd_nm,lots,stock_id,cov_p,i]
                
        
        self.newpos_df = newpos_df

        
    def op_send_order(self):
        ##sell
        for i in self.sell_df.index:
            lots = self.sell_df['postions'][i]
            p=self.pos_df['bond_id_price'][i]
            self.order_LOTS(i,lots,self.ContextInfo, self.accID)
            self.p0.cash = self.p0.cash + p *(-lots)
            self.p0.capital = self.p0.capital + p *lots
        ##buy
        for i in self.buy_df.index:
            lots = self.buy_df['postions'][i]
            p=self.lowestN_df['bond_id_price'][i]
            val = p * lots            
            if (val<self.p0.cash):            
                self.order_LOTS(i,lots,self.ContextInfo, self.accID)    
                self.p0.cash = self.p0.cash - val
                self.p0.capital = self.p0.capital + val
            
    def run(self):
        self.get_lookup_df()
        self.get_pos_df()
        N= self.max_stock_nums 
        self.lowestN_df = self.u0.df_filter('new_dlow_rank',N)
        self.lowestM_df = self.u0.df_filter('new_dlow_rank',self.M)
        print("lowestM")
        print(self.lowestM_df)
        print("lowestN")
        print(self.lowestN_df)
        self.pos_df     = self.p0.df
        
        
        self.get_expect_df()
        self.get_sub_df()
        self.op_send_order()
        self.setup_record_df()
        self.setup_new_pos_df()
        self.write_record()
        self.p0.write_cash(self.accountfile)
        
        
        
        
        

        
        # self.p0 = qmt_basic_lib(file=self.pos_file)  ##def check_position(df1,pos_file): add to 
        # print("posfile:")
        # print(self.p0.df)
        # # self.p0.check_position(self.u0, 'new_dlow_M')
        # # print("checked posfile")
        # print(self.p0.df)
        # self.p0.pos_filter()
        # f1='account.csv'
        # self.p0.get_cash(f1)
        
        # N = self.max_stock_nums - self.p0.hold_cnt
        # for i in self.p0.df['bond_id']:
        #     lap = self.p0.df['overlap'][i]
        #     if lap==True:
        #         self.u0.drop_row(i)
        #         print("drop u0 i=%s" %(i))
        # print("max num=%d,hold_cnt=%d,N=%d" %(self.max_stock_nums,self.p0.hold_cnt,N))
        # print("u0.df after drop")
        # print(self.u0.df)
        
        # self.u0.get_minN('new_dlow',N,'new_dlow_N') 
        # m=self.u0.df['new_dlow_N']==True
        # df3 = self.u0.df[m]
        
        # for i in df3['bond_id']:
        #     bond_nm      =self.u0.get_pixel(i, 'bond_nm')
        #     postions     =0 
        #     stock_id     =self.u0.get_pixel(i, 'stock_id')
        #     convert_price=self.u0.get_pixel(i, 'convert_price')
        #     bond_id      =self.u0.get_pixel(i, 'bond_id')
        #     hold         =False  
        #     overlap      =False   
        #     row=[self.stratgy_name,bond_nm, postions, stock_id,convert_price, bond_id, hold, overlap]             
        #     self.p0.write_row(i,row)
            
        # self.p0.get_market('bond_id')
        # self.p0.get_market('stock_id')   
        # self.p0.cal_target_lots2(self.max_capital,self.max_stock_nums)
        # self.p0.write_cash(f1)
        # print("before send order")
        # print(self.p0.df)
        # self.p0.order_send(self.ContextInfo, self.accID)
        # self.write_record()
        
        
        
        






