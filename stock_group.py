#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:56:35 2020

@author: Johnny Tsai
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

url = 'https://tw.stock.yahoo.com/q/q'


headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4122.7 Mobile Safari/537.36'}


stock_ids = ['1707', '2105','4906', '0050', '2330']
#stock_ids = ['6269', '3105', '4906', '0050', '2330']

df_index = ['股票代號', '成交', '漲跌','張數', '昨收', '開盤', '最高', '最低']

#YAHOO['股票代號', '時間', '成交', '買進', '賣出', '漲跌','張數', '昨收', '開盤', '最高', '最低']

stock_name = []
stock_price = []
stock_change = []

for stock_id in stock_ids:
    payload = {
            's': stock_id
    }
    response = requests.get(url, params=payload, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table')
    table = tables[2]
    tds = table.find_all('td')
    stock_name.append(tds[0].text.strip().replace('加到投資組合', ''))
    stock_price.append(tds[2].text.strip())
    stock_change.append(tds[5].text.strip())
    time.sleep(1)

df = pd.DataFrame()

df['stock_name'] = stock_name
df['stock_price'] = stock_price
df['stock_change'] = stock_change

print(df)

#LINE NOTIFY

def lineNotifyMessage(token, msg):
   headers = {
       "Authorization": "Bearer " + token, 
   }
	
   payload = {'message': msg}
   r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
   return r.status_code
	
message = '\n' + df.iloc[0,0] + '：' + df.iloc[0,1] + ' ; ' + df.iloc[0,2] \
        + '\n' + df.iloc[1,0] + '：' + df.iloc[1,1] + ' ; ' + df.iloc[1,2] \
        + '\n' + df.iloc[2,0] + '：' + df.iloc[2,1] + ' ; ' + df.iloc[2,2] \
        + '\n' + df.iloc[3,0] + '：' + df.iloc[3,1] + ' ; ' + df.iloc[3,2] \
        + '\n' + df.iloc[4,0] + '：' + df.iloc[4,1] + ' ; ' + df.iloc[4,2]   
            
token = 'yfOAGBNnJXNoT57I9MM2aY9YgRKv9z1faDU1bbS2Ror'

lineNotifyMessage(token, message)