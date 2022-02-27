# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 12:15:31 2021

@author: 39939
"""

#from jisilu_lib import jisilu_lib
#from qmt_basic_lib import qmt_basic_lib
#from qmt_lib import qmt_lib
#
#lookup_csv = 'lookup.csv' ###
#bond_nums=3 ###
#threshold=5####
#prem_coef=0  ##
#price_coef=1  ###
#record_file='pos.csv'  ####
#stratgy_name='A'  ####
#max_capital = 1000000  ##
#Info='leizhijie'  ###
#accID='006354'   #####
#Mode= 0  ### 0: prem/dlow , 1:increase_diff 
#turn= 1  ## 1 : 1h , 2: 2h , 24:1day turn, it can used outside .....
#recordfile='record.csv'
#accountfile='account.csv'
#
#u0_csv = jisilu_lib(lookup_csv)
#        
#u0 = qmt_lib(bond_nums,threshold,prem_coef,price_coef,record_file,stratgy_name,max_capital,Info,accID,Mode,lookup_csv,recordfile,accountfile  )
#u0.run2()



def read1_csv(file):
    import pandas as pd
    df = pd.read_csv(file)
    a=[]
    len1 = len(df)
    for i in range(len1):
        a.append(df.loc[i][0])
    return a

file1="D:/testfile1/bond_stock_list.csv"   ####CAN not support Chinese path
df1=read1_csv(file1)
print(df1)

