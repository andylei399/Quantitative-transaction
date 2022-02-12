# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:59:36 2022

@author: 39939
"""

import easytrader
import time
import re
import random
import datetime
from dateutil.parser import parse
import pandas as pd
import random
import shutil
import os
import datetime
import pandas as pd
#import easyquotation
import sys
from quotation import quotation


update_tamp=[]
update_first=[]

update1_tamp=[]
update1_first=[]

class trade_uint:
    def __init__(self,max_time_diff=120,config_file='xq.json',total_assets=100000,strag_name='ZH141959',filename="test1.txt",workmode_en=1,init_en=0,tampfile="tamp.txt"):
        self.config_file  =config_file
        self.total_assets =total_assets
        self.strag_name   =strag_name
        self.filename     =filename
        self.max_time_diff=max_time_diff
        self.workmode_en       =workmode_en
        self.init_en =init_en
        self.tampfile =tampfile
        self.tamp = self.read_timetamp()
        
        self.quo = quotation()
        
    # def get_readl_price(self,code):
    #     quotation = easyquotation.use('sina')
    #     quotation.market_snapshot(prefix=True)
    #     p= quotation.stocks([code,code])  # can get 多个stock行情
    #     #print(p)
    #     return p
    

        
    def exist_tamp(self,t1):
        exist = 0
        for i in range(len(self.tamp)):
            #print("input tamp=%d,stored tamp = %d" % (t1,self.tamp[i]) )
            if (self.tamp[i]==t1):
                exist = 1
                break
        return exist

    def is_bond(self,symbol):
        code = int(symbol)
        if(code>=110000) and (code<130000) and (code <117000) and (code >117999):
            bond = 1
        else:
            bond = 0
        return bond

    def is_first(self,tamp):
        global update_tamp
        global update_first
        first1 = 1
        for i in range(len(update_tamp)):
            t1 = update_tamp[i]
            v1 = update_first[i]
            if(t1==tamp):
                first1 =0
                break
        if(first1):
            update_first.append(1)
            update_tamp.append(tamp)
            
        return first1



    def is_first_timeover(self,tamp):
        global update1_tamp
        global update1_first
        first1 = 1
        for i in range(len(update1_tamp)):
            t1 = update1_tamp[i]
            v1 = update1_first[i]
            if(t1==tamp):
                first1 =0
                break
        if(first1):
            update1_first.append(1)
            update1_tamp.append(tamp)
            
        return first1


    def print_stock(self,strag_name,total_assets,config_file):
        xq_user = easytrader.use('xq')
        xq_user.prepare(config_file) #('xq.json') #jsonæä»¶ç´æ¥ç¨è§£éå¨çæå³å¯
        a=xq_user._get_portfolio_info(strag_name) #(self)
        list1 = []
        b=a['sell_rebalancing']['rebalancing_histories']
        strag_name1= a['name']
        
        #print(b)
    
        for i in range(len(b)):
            stock_name = b[i]['stock_name']
            stock_symbol = b[i]['stock_symbol']
            price = b[i]['price']
            #b1=b[i]['target_weight']
            #b0=b[i]['prev_weight_adjusted']
            b1_z = 0
            b0_z = 0
            
            pattern = re.compile(r'\d+')   # æ¥æ¾æ°å­
            stock_symbol2 = pattern.findall(stock_symbol)            
            bond =self.is_bond(stock_symbol2[0])
            if bond==1:
                unit1=10
            else:
                unit1=100
                
            if (b[i]['target_weight']==None):
                b1_z = 1
            if (b[i]['prev_weight_adjusted']==None):
                b0_z = 1                
            
            if (b1_z):
                b1 = 0
            else:
                b1 = b[i]['target_weight']
                
            if(b0_z):
                b0 = 0
            else:
                b0 = b[i]['prev_weight_adjusted']

            
            # p  = self.get_readl_price(stock_symbol2[0])
            # print("real price !!!!!!!!!!!")
            # print(p)
            # print("\n\n")
            # st = [stock_symbol2[0]]
            # print(st)
            # p0 = self.quo.get_price(st,1)
            # print("the price is :")
            # print(p0)

            if (price==None):
                price1 = self.quo.get_price(stock_symbol2[0])
                print("%s AAAAAAï¼price is none @ %s " % (stock_name,self.get_now()))
                #continue            
                if (b1-b0 >0):
                    price = price1[0]
                else:
                    price = price1[1]
            
            shares = (b1 - b0) * total_assets / 100 / price 
            lots = ((int)(shares / unit1 )) * unit1  ###TODO
            updated_at = b[i]['updated_at']
            
            

            b111 = self.timediff(updated_at)
            ##如果是12点更新的，是否会出现max time 超过，但它还是一笔正常交易的情况 ??/? 如果处理？
            if(b111>self.max_time_diff and self.workmode_en==1):  ## å¦ææ¯å¾æ©çä¿¡æ¯ï¼å°±ä¸æ´æ°
                #if (self.is_first(updated_at)):
                if(self.is_first_timeover(updated_at)):
                    print("%s @ %s ,>=max_time_diff éªçä¿¡æ¯è¿æ§ï¼è·³åºæ§è¡" % (stock_name,self.get_now()))
                continue     
            exist = self.exist_tamp(updated_at) 
            if (exist==1):
                #print("å·²ç»æ§è¡è¿ï¼è·³åºæ¬æ¬¡æ§è¡")
                if (self.is_first(updated_at)):
                    print("the strag %s : tamp is exist ,ignore @ %s" %(strag_name1,self.get_now() ))
                continue                        
            self.write_timetamp(updated_at)
    
            if (lots>0):
                a=[23,1,14,price,stock_symbol2[0],lots,strag_name1,stock_name,updated_at]
                list1.append(a)
            elif (lots<0):
                lots2 = -lots
                a=[24,1,14,price,stock_symbol2[0],lots2,strag_name1,stock_name,updated_at]      
                list1.append(a)
                
        return list1

    def get_init_stock(self,strag_name,total_assets,config_file):
        xq_user = easytrader.use('xq')
        xq_user.prepare(config_file) #('xq.json') #jsonæä»¶ç´æ¥ç¨è§£éå¨çæå³å¯
        a=xq_user._get_portfolio_info(strag_name) #(self)
        list1 = []
        b=a['view_rebalancing']['holdings']
        strag_name1= a['name']

        
        
        for i in range(len(b)):
            stock_name = b[i]['stock_name']
            stock_symbol = b[i]['stock_symbol']
#            volume = b[i]['volume']   ### get current price .....
            weight = b[i]['weight']
            updated_at = b[i]['updated_at']
            
            pattern = re.compile(r'\d+')   # æ¥æ¾æ°å­
            stock_symbol2 = pattern.findall(stock_symbol)            
            bond =self.is_bond(stock_symbol2[0])
            if bond==1:
                unit1=10
            else:
                unit1=100

            # if (volume==0):
            #     print("%s volume is 0 @ %s" % (stock_name,self.get_now()))
            #     continue
            if (weight==0):
                print("%s weight is none % s" %  (stock_name,self.get_now()))
                continue

            #price1 = (weight / 100 / volume)   ##more high in order sucess            
            #price2 = int(price1 * 100)         
            #price = price2 / 100 
            
            price1 = self.quo.get_price(stock_symbol2[0])
            price = price1[1]
            
            

            b1 = b[i]['weight']           
            shares = (b1 - 0) * total_assets / 100 / price 
            lots = ((int)(shares / unit1 )) * unit1

    
            if (lots>0):
                a=[23,1,14,price,stock_symbol2[0],lots,strag_name1,stock_name,updated_at]
                list1.append(a)
            elif (lots<0):
                lots2 = -lots
                a=[24,1,14,price,stock_symbol2[0],lots2,strag_name1,stock_name,updated_at]      
                list1.append(a)
            else:
                print("%s error order shares <100 , shares=%d, lots=%d @ %s" % (stock_name,shares,lots,self.get_now()))
                
        return list1    
    
    def print_2_txt(self,filename,list1):
        f = open(filename, 'a')
        for i in range(len(list1)):
            txt = list1[i]
            len1 = len(txt) -3
            updated_at =txt[-1]
            stock      = txt[-2]
            strag_name1 = txt[-3]
            
            
            time1 = self.time_strftime1(updated_at)
            
            print("%s : send order at %s ,the order is :(stock=%s @ %s)  " % (strag_name1,self.get_now(),stock,time1))
            print(txt)
            for j in range(len1):
                str1 = txt[j]
                if j == (len1-1):
                    comma = "\n"
                else:
                    comma = ","
                str2 = str(str1) + comma
                f.write(str2)
        f.close()
    
    def time_strftime1(self,time_stamp):
        local_time = time.localtime(time_stamp / 1000)
        return time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    
    def get_now(self):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dt        
    
    def timediff(self,updated_at):
        dt =self.get_now() #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time1 = self.time_strftime1(updated_at)

        a = parse(dt)
        b = parse(time1)
        c = (a-b).total_seconds()
        return c

    def run(self):
        if(self.init_en):
            list1 = self.get_init_stock(strag_name=self.strag_name,total_assets=self.total_assets,config_file=self.config_file)
        else:
            list1 = self.print_stock(strag_name=self.strag_name,total_assets=self.total_assets,config_file=self.config_file)
        self.print_2_txt(self.filename, list1)



    def write_timetamp(self,t1):
        f = open(self.tampfile, 'a')
        str2 = str(t1)+"\n"
        f.write(str2)
        f.close()
        time1 = self.time_strftime1(t1)
        print("write tamp =%s (time is %s)" % (str2,time1))
        
    def read_timetamp(self):
        f = open(self.tampfile, 'r')
        text_lines = f.readlines()
        f.close()

        
        pattern = re.compile(r'\d+')   # æ¥æ¾æ°å­
        t2 = []
        for i in range(len(text_lines)):
            ln = text_lines[i]
            t1 = pattern.findall(ln)
            t2.append(int(t1[0]) )
        
        return t2

class trade_top:
    def __init__(self,max_time_diff=120,filename="test1.txt",cmd_file="command.csv",workmode_en=1 , workdir ="C:\\Users",init_en=0,tampfile="tamp.txt" ):
        self.filename     =workdir + "\\" + filename
        self.max_time_diff=max_time_diff
        self.workmode_en  =workmode_en
        self.cmd_file     =workdir + "\\" + cmd_file
        self.market       = 'cn'
        self.init_en      = init_en
        self.tampfile =tampfile #'.txt'
        self.workdir = workdir
        self.config_file=[]
        self.total_assets=[]
        self.strag_name=[]
        self.gen_config_file()
       

    def csv2df(self,file):  # the csv file must be stored in df
        df1 = pd.read_csv(file, encoding='gbk')
        df = df1.copy()
        return df
    
    
    def gen_json(self,strag_name,cookies,market,filename):
        tmp="{\n"
        tmp=tmp+"  \"cookies\": \"" + cookies + "\",\n"
        tmp=tmp+"  \"portfolio_code\": \"" + strag_name + "\",\n"
        tmp=tmp+"  \"portfolio_market\": \"" + market + "\"\n}\n"    
        f = open(filename, 'w')
        f.write(tmp)
        f.close()    
        
    
    def gen_config_file(self):
        df = self.csv2df(self.cmd_file)
        rows = df.shape[0]
       
        for i in range(rows):
            strag_name1 = df['strag_name'][i]
            strag_enable=df['strag_enable'][i]
            total_assets1=df['total_assets'][i]
            cookies=df['cookies'][i]    
            new_strag=df['new_strag'][i]
            init_en = self.init_en==1  and new_strag==1 and strag_enable==1
            en = 0 
            
            if (self.init_en):
                en = init_en
            else:
                en = strag_enable==1
 
            
            filename =self.workdir + "\\" + "xq"+str(i)+".json"
            self.gen_json(strag_name1,cookies,self.market,filename)
        
            if(en):    
                self.config_file.append(filename)
                self.total_assets.append(total_assets1)
                self.strag_name.append(strag_name1)
            else:
                print("ignore this strag:%s" % (strag_name1) )
            

    def run(self):
        for i in range(len(self.config_file)):
            cf = self.config_file[i]
            ta = self.total_assets[i]
            sn = self.strag_name[i]     

            xqjson =self.gen_xqjson(cf)
            second1 = random.randint(15,30)
            time.sleep(second1)
            
            trade_uint_u0 =trade_uint(workmode_en=self.workmode_en,max_time_diff=self.max_time_diff,filename=self.filename,config_file=xqjson,total_assets=ta,strag_name=sn,init_en=self.init_en,tampfile=self.tampfile)
            trade_uint_u0.run()

    def gen_xqjson(self,file1):

        xqjson =self.workdir + "\\" + "xq.json"  # os.path.join('.', 'xq.json')
        if (os.path.isfile(xqjson)):
            os.remove(xqjson)
        shutil.copy(file1,xqjson)
        #if (os.path.isfile(xqjson)):
            #print("copy xq.json success")
        return xqjson
    
        
class trade_wrapper():
    def __init__(self,max_time_diff=120,filename="test1.txt",cmd_file="command.csv",workmode_en=1 , workdir ="D:\\testfile1",init_en=0,tampfile="tamp.txt",sleeptime=10,clear=0,tologfile=0 ):
            
        self.max_time_diff =600 #max_time_diff     #120 # df['max_time_diff'][0] ####ææ¬æ¡
        self.filename      =filename          #'test1.txt' # df['filename'][0]  ####ææ¬æ¡
        self.cmd_file      =cmd_file          #'command.csv' # df['cmd_file'][0]  ####ææ¬æ¡
        self.workdir       =workdir           #'D:\\testfile1' # df['workdir'][0]  ####ææ¬æ¡
        self.sleeptime     =sleeptime         #10# df['sleeptime'][0]  ####ææ¬æ¡
        self.tampfile      =tampfile          #'tamp.txt' # df['tampfile'][0]   ####ææ¬æ¡
        self.init_en       =init_en           #0 # df['init_en'][0]  ##éæ©æ¡ ## init or follower
        self.workmode_en   =workmode_en       #0 # df['workmode_en'][0] # éæ©æ¡ï¼è°è¯ or work
        self.clear         =clear
        self.tologfile     =tologfile


    def worktime(self):

        h =datetime.datetime.now().hour
        m = datetime.datetime.now().minute
        s = datetime.datetime.now().second
        en = 0
        t1 = (h*3600) + (m*60) + s
        e0 =  (9*3600) + (15*60) 
        e1 =  (11*3600) + (30*60) 
        e2 =  (13*3600) + (0*60) 
        e3 =  (15*3600) + (0*60) 
        
        if (t1>=e0 and t1<e1):
            en =1
        elif (t1>=e2 and t1<e3):
            en = 1
        else:
            en = 0
        return en

    def set_global_print(self):
        if(self.clear==1):
            f = open('log.txt', 'w')
            f.write("")
            f.close()  
        sys.stdout = open('log.txt','a+')
        print("Hello Python!")
        print("We are printing to file.")


    def read_from_csv(self,file="config.csv"):    

        df = pd.read_csv(file, encoding='gbk')
        self.max_time_diff =600# df['max_time_diff'][0] ####ææ¬æ¡
        self.filename      = df['filename'][0]  ####ææ¬æ¡
        self.cmd_file      = df['cmd_file'][0]  ####ææ¬æ¡
        self.workdir       = df['workdir'][0]  ####ææ¬æ¡
        self.sleeptime     = df['sleeptime'][0]  ####ææ¬æ¡
        self.tampfile      = df['tampfile'][0]   ####ææ¬æ¡
        self.init_en       = df['init_en'][0]  ##éæ©æ¡ ## init or follower
        self.workmode_en   = df['workmode_en'][0] # éæ©æ¡ï¼è°è¯ or work
        self.clear         = df['clear'][0] 
        self.tologfile     = df['tologfile'][0] 
        
    def get_now(self):
        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dt   
    

    def process(self):   
        if(self.tologfile):              
            self.set_global_print();

        print(self.max_time_diff ) #=max_time_diff     #120 # df['max_time_diff'][0] ####ææ¬æ¡?
        print(self.filename      ) #=filename          #'test1.txt' # df['filename'][0]  ####ææ¬æ¡?
        print(self.cmd_file      ) #=cmd_file          #'command.csv' # df['cmd_file'][0]  ####ææ¬æ¡?
        print(self.workdir       ) #=workdir           #'D:\\testfile1' # df['workdir'][0]  ####ææ¬æ¡?
        print(self.sleeptime     ) #=sleeptime         #10# df['sleeptime'][0]  ####ææ¬æ¡?
        print(self.tampfile      ) #=tampfile          #'tamp.txt' # df['tampfile'][0]   ####ææ¬æ¡?
        print(self.init_en       ) #=init_en           #0 # df['init_en'][0]  ##éæ©æ¡?## init or follower
        print(self.workmode_en   ) #=workmode_en       #0 # df['workmode_en'][0] # éæ©æ¡ï¼è°è¯ or work        


        tampfile1 =self.workdir + "\\" + self.tampfile
        filename1 =self.workdir + "\\" + self.filename
        if(self.workmode_en==0 or self.clear==1):
            f = open(tampfile1, 'w')
            f.write("")
            f.close()
            f = open(filename1, 'w')
            f.write("")
            f.close()

        trade_uint_u0 =trade_top(workmode_en=self.workmode_en,max_time_diff=self.max_time_diff,cmd_file=self.cmd_file,workdir=self.workdir,filename=self.filename,init_en=self.init_en,tampfile=tampfile1)
   
    
        if (self.init_en==1):###only init
            trade_uint_u0.run() 
        else:   
            cnt = 0
            #st = 10
              
            
            while True:##follow 
                if (self.workmode_en==1):
                    en = self.worktime()
                    #st = 10
                else:
                    en = 1
                    #st = 10 #self.sleeptime
                   
                if (en==1):        
                    trade_uint_u0.run()
                    

                #xqjson =self.gen_xqjson(cf)
                second1 = random.randint(1,5)
                time.sleep(second1)
                
                #time.sleep(st)    
                if(cnt%30==0) or (self.workmode_en==0):
                    print("running %s ,working=%d" %(self.get_now(),en))
                cnt = cnt + 1
            
#if (debug_mode==1):
#    process()
#    
    
u0=trade_wrapper(workmode_en=0)
u0.process()
#你好






#run()


#u0 = trade_gui()
#u0.run()


  

