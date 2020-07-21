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


stock_id = input('請輸入股號：')

df_index = ['股票代號', '時間', '成交', '買進', '賣出', '漲跌', 
            '張數', '昨收', '開盤', '最高', '最低']


payload = {
            's': stock_id
}

response = requests.get(url, params=payload, headers=headers)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
tables = soup.find_all('table')
table = tables[2]

tds = table.find_all('td')

stock_data = []    
    
for td in tds[:-1]:
    data = td.text.strip().replace('加到投資組合', '')
    stock_data.append(data)
    
df = pd.DataFrame(stock_data, index=df_index)

print(df)
print('-'*20)
time.sleep(3)

stock = df.loc['股票代號',:]
price = df.loc['成交',:]
change = df.loc['漲跌',:]

#---------------------------------------------------------------


def lineNotifyMessage(token, msg):
   headers = {
       "Authorization": "Bearer " + token, 
   }
	
   payload = {'message': msg}
   r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
   return r.status_code
	
message = '\n' + stock + '即時價格：' + price + ' ; ' + change
token = 'wtxiy16rGmEC7iewybsllLPX5re9dpujK8N7PBuj5NM'

lineNotifyMessage(token, message)