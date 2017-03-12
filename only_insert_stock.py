# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 12:15:06 2017

@author: kiamw
"""

import requests
import json
import datetime
import pymysql

url_all = 'http://www.xignite.com/xGlobalHistorical.json/GetGlobalHistoricalQuotes?IdentifierType=Symbol&Identifiers=AAPL,GOOG,AMZN&AdjustmentMethod=None&AsOfDate='

get_days = 30
store_json = []
today = datetime.date.today()
i = 0
while i < get_days :    
    today = today + datetime.timedelta(days=-1)
    if today.weekday() < 5 :
        response = requests.get(url_all + today.strftime('%m/%d/%Y'), headers={'Authorization' : 'TOK:D19818E34FC2442E9478D3E673549DB9'})
        data = response.json()
        if data[0]["Date"] == None or data[0]["Date"] == '' :
            break;
        if datetime.datetime.strptime(data[0]["Date"],'%m/%d/%Y').strftime('%m/%d/%Y') == today.strftime('%m/%d/%Y') :
            for j in range(0,len(data)) :
                data[j]["Date"] = datetime.datetime.strptime(data[j]["Date"],'%m/%d/%Y').strftime('%d/%m/%Y')
                store_json.append(data[j])
            i = i + 1

store_list = []
list_row = ['','','','']
for i in range(0,len(store_json)):
    list_row = ['','','','']
    list_row[0] = datetime.datetime.strptime(store_json[i]["Date"],'%d/%m/%Y')
    list_row[1] = store_json[i]["Security"]["Symbol"]
    list_row[2] = store_json[i]["Last"]
    list_row[3] = store_json[i]["Volume"]
    store_list.append(list_row)

"""
/*
DB = MySQL
schema name = db_python
user db name = db_python_user
user db password = password
*/

CREATE TABLE `stocks` (
  `close_date` date NOT NULL,
  `stock_name` varchar(45) NOT NULL,
  `closed_price` float DEFAULT NULL,
  `closed_volume` float DEFAULT NULL,
  PRIMARY KEY (`close_date`,`stock_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""
db = pymysql.connect(host='localhost',          # your host, usually localhost
                     user='db_python_user',     # your username
                     passwd='password',         # your password
                     db='db_python')            # name of the data base

cur = db.cursor()

insert_str = 'INSERT INTO db_python.stocks (close_date,stock_name,closed_price,closed_volume) VALUES (%s,%s,%s,%s)'
cur.executemany(insert_str,store_list)
#cur.execute('delete from db_python.stocks')
cur.execute('commit')

#cur.execute('SELECT * FROM stocks')
#for row in cur.fetchall():
#    print(row[0])
db.close()
