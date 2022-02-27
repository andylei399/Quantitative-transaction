# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 12:45:59 2021

@author: 39939
"""


class jisilu_lib:
    def __init__(self,file):
        self.gen_lookup(file)
        print("Load jisilu web")


    def get_dat(self):
        import json
#        import requests
#        import csv
#        import re
#        from lxml import etree
        
    # #headers = {
    # #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
    # headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'}
    ###it must login first, then use Mouse get ....
    # #newUrl ="https://www.jisilu.cn/data/cbnew/cb_list/?___jsl=LST___t=1584777951900"
    # newUrl = "https://xueqiu.com/hq#exchange=CN&industry=4_0&firstName=4"
    # from requests.auth import HTTPBasicAuth
    # #from requests.oauoauthlib 
    # auth2 =HTTPBasicAuth('13611945147','112233llkkMMNN')
    # #最简单的爬虫请求.也可以加上headers字段，防止部分网址的反爬虫机制
    # #auth = ('13611945147','112233llkkMMNN')
    # response = requests.get(newUrl,auth=auth2,headers=headers,timeout=20)
    # #当爬取的界面需要用户名密码登录时候，构建的请求需要包含auth字段
    # print(response.status_code)
    # data = response.content.decode("utf-8")
        with open('./aaa1.json','r',encoding='utf8')as fp:
            json_data = json.load(fp)
            print('这是读取到文件数据的数据类型：', type(json_data))
        dat = json_data #json.loads(json_data)

  
    # 所有数据
        data = []
        cnt=0
        for one in dat['rows']:
            cnt=cnt+1
            if(cnt==50):
                break
            
        # 每一条数据
            dat1 = []
            # 转债id
            #id = one["id"]
            dat_cell = one["cell"]
            # 是否赎回
            is_shui = dat_cell['force_redeem']
            #print(one)
            #print("\n")
            if is_shui == None:
                # 转债名称
                bond_nm = dat_cell['bond_nm']
                bond_id = dat_cell['bond_id']
                price = dat_cell['price']
            #increase_rt=dat_cell['increase_rt']
            # 溢价率
                premium_rt = dat_cell['premium_rt']
            # 回售触发价
                put_convert_price = dat_cell['put_convert_price']
            # 强赎触发价
                force_redeem_price = dat_cell['force_redeem_price']
            # 剩余时间
                last_time = dat_cell['year_left']
                convert_price = dat_cell['convert_price']
            #turnover_rt=dat_cell['turnover_rt']
            # 双低
                dblow = dat_cell['dblow']
            ##################################################
            # Stock info
                stock_nm= dat_cell['stock_nm']
                stock_id = dat_cell['stock_id']
                sprice=dat_cell['sprice']
            #sincrease_rt=dat_cell['sincrease_rt']
    
                dat1.append(bond_nm)
                dat1.append(bond_id)
                dat1.append(price)
                #dat1.append(increase_rt)
                dat1.append(premium_rt)
                dat1.append(put_convert_price)
                dat1.append(force_redeem_price)
                dat1.append(last_time)
                dat1.append(convert_price)
            #dat1.append(turnover_rt)
                dat1.append(dblow)
                dat1.append(stock_nm)
                dat1.append(stock_id)
                dat1.append(sprice)
            #dat1.append(sincrease_rt)
            #print(dat1)
                data.append(dat1)
            
            else:
                continue
        return data
        
    def gen_lookup(self,lookup_file):
        import pandas as pd
        pd.set_option('display.max_columns',60)
        pd.set_option('display.max_rows',10)    
        data = self.get_dat()
        file2="lookup_temp.csv" #"aaa3.csv"   
        head=['bond_nm','bond_id1','bond_price','prem','put_convert_price','force_redeem_price','last_time','convert_price','dblow','stock_nm','stock_id1','stock_price']            
        df1 = pd.DataFrame(data,columns=head)      

        df1.to_csv(file2,encoding='gbk')
        df2 = pd.read_csv(file2,encoding='gbk')
        c =df2['bond_id1'] > 117999
        d= df2['bond_id1'] < 117000    
        df1 = df1[c+d]
        
        b1=self.int2char(df2['bond_id1'])
        df1['BOND_ID'] = b1
        df1.set_index('BOND_ID',inplace=True)

        df1['bond_id'] = b1
        df1.columns.name='PARA'
        df1.index.name='BOND_ID'  ###it is must ,otherwise the csv to df will has more columns
    
        si = df1['stock_id1']
        df1['stock_id'] = self.char_modify(si)
        del df1['stock_id1']
        del df1['bond_id1']
        df1.to_csv(lookup_file,encoding='gbk')


    def int2char(self,data):
        a=[]
        for i in data:
            if(i<120000):
                s='.SH'
            else:
                s='.SZ'
            tmp = '%d' % i
            c=str(tmp) + str(s)
            a.append(c)
        return a


    def char_modify(self,data):
        b=[]
        for i in data:
            c=i[0:2]
            a=i[2:8]
            d=c.upper()
            e=a+'.'+d
            b.append(e)
        return b    

    
#u0 = jisilu_lib()

