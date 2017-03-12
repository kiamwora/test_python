# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 12:32:03 2017

@author: kiamw
"""

import requests
import json
import datetime
import feedparser
import pymysql

#=====Feed news
fd_aapl = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=AAPL')
fd_goog = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=GOOG')
fd_amzn = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=AMZN')

store_fd_aapl = []
for i in range(0,len(fd_aapl['entries'])):
    today = datetime.datetime.strptime(fd_aapl['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_aapl['entries'][i]["date"] = today.strftime('%d/%m/%Y')
    store_fd_aapl.append(fd_aapl['entries'][i])

store_fd_goog = []
for i in range(0,len(fd_goog['entries'])):
    today = datetime.datetime.strptime(fd_goog['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_goog['entries'][i]['date'] = today.strftime('%d/%m/%Y')
    store_fd_goog.append(fd_goog['entries'][i])

store_fd_amzn = []
for i in range(0,len(fd_amzn['entries'])):
    today = datetime.datetime.strptime(fd_amzn['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_amzn['entries'][i]['date'] = today.strftime('%d/%m/%Y')
    store_fd_amzn.append(fd_amzn['entries'][i])


#=====setup url for call api web service
url_all = 'http://www.xignite.com/xGlobalHistorical.json/GetGlobalHistoricalQuotes?IdentifierType=Symbol&Identifiers=AAPL,GOOG,AMZN&AdjustmentMethod=None&AsOfDate='
response = requests.get(url_all + today.strftime('%m/%d/%Y'), headers={'Authorization' : 'TOK:D19818E34FC2442E9478D3E673549DB9'})
data_test = response.json()
print(data_test) #ALL

get_days = -1
store_json = []
today = datetime.date.today()
i = 0
while i < get_days :    
    today = today + datetime.timedelta(days=-1)
    if today.weekday() < 5 :
        response = requests.get(url_all + today.strftime('%m/%d/%Y'), headers={'Authorization' : 'TOK:D19818E34FC2442E9478D3E673549DB9'})
        data = response.json()
        if data[0]['Date'] == None or data[0]['Date'] == '' :
            break;
        if datetime.datetime.strptime(data[0]['Date'],'%m/%d/%Y').strftime('%m/%d/%Y') == today.strftime('%m/%d/%Y') :
            for j in range(0,len(data)) :
                data[j]['Date'] = datetime.datetime.strptime(data[j]['Date'],'%m/%d/%Y').strftime('%d/%m/%Y')
                store_json.append(data[j])
            i = i + 1
            
#=====insert DB
store_list = []
list_row = ['','','','','','','','']
for i in range(0,len(store_json)):
    list_row = ['','','','','','','','']
    count_match = 0
    if store_json[i]['Security']['Symbol'] == 'AAPL' :
        j = 0
        for j in range(0,len(store_fd_aapl)):
            list_row = ['','','','','','','','']
            if store_fd_aapl[j]['date'] == store_json[i]['Date'] and count_match == 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = store_json[i]['Last']
                list_row[3] = store_json[i]['Volume']
                list_row[4] = store_fd_aapl[j]['id']
                list_row[5] = datetime.datetime.strptime(store_fd_aapl[j]['date'],'%d/%m/%Y')
                list_row[6] = store_fd_aapl[j]['title']
                list_row[7] = store_fd_aapl[j]['description'][0:store_fd_aapl[j]['description'].find('<img',0)]
                store_list.append(list_row)
                count_match = count_match + 1
            elif store_fd_aapl[j]['date'] == store_json[i]['Date'] and count_match != 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = 0
                list_row[3] = 0
                list_row[4] = store_fd_aapl[j]['id']
                list_row[5] = datetime.datetime.strptime(store_fd_aapl[j]['date'],'%d/%m/%Y')
                list_row[6] = store_fd_aapl[j]['title']
                list_row[7] = store_fd_aapl[j]['description'][0:store_fd_aapl[j]['description'].find('<img',0)]
                store_list.append(list_row)
        if count_match == 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = store_json[i]['Last']
                list_row[3] = store_json[i]['Volume']
                list_row[4] = ''
                list_row[5] = ''
                list_row[6] = ''
                list_row[7] = ''
                store_list.append(list_row)
    if store_json[i]['Security']['Symbol'] == 'GOOG' :
        j = 0
        for j in range(0,len(store_fd_goog)):
            list_row = ['','','','','','','','']
            if store_fd_goog[j]['date'] == store_json[i]['Date'] and count_match == 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = store_json[i]['Last']
                list_row[3] = store_json[i]['Volume']
                list_row[4] = store_fd_goog[j]['id']
                list_row[5] = datetime.datetime.strptime(store_fd_goog[j]['date'],'%d/%m/%Y')
                list_row[6] = store_fd_goog[j]['title']
                list_row[7] = store_fd_goog[j]['description'][0:store_fd_goog[j]['description'].find('<img',0)]
                store_list.append(list_row)
                count_match = count_match + 1
            elif store_fd_goog[j]['date'] == store_json[i]['Date'] and count_match != 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = 0
                list_row[3] = 0
                list_row[4] = store_fd_goog[j]['id']
                list_row[5] = datetime.datetime.strptime(store_fd_goog[j]['date'],'%d/%m/%Y')
                list_row[6] = store_fd_goog[j]['title']
                list_row[7] = store_fd_goog[j]['description'][0:store_fd_goog[j]['description'].find('<img',0)]
                store_list.append(list_row)
        if count_match == 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = store_json[i]['Last']
                list_row[3] = store_json[i]['Volume']
                list_row[4] = ''
                list_row[5] = ''
                list_row[6] = ''
                list_row[7] = ''
                store_list.append(list_row)
    if store_json[i]['Security']['Symbol'] == 'AMZN' :
        j = 0
        for j in range(0,len(store_fd_amzn)):
            list_row = ['','','','','','','','']
            if store_fd_amzn[j]['date'] == store_json[i]['Date'] and count_match == 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = store_json[i]['Last']
                list_row[3] = store_json[i]['Volume']
                list_row[4] = store_fd_amzn[j]['id']
                list_row[5] = datetime.datetime.strptime(store_fd_amzn[j]['date'],'%d/%m/%Y')
                list_row[6] = store_fd_amzn[j]['title']
                list_row[7] = store_fd_amzn[j]['description'][0:store_fd_amzn[j]['description'].find('<img',0)]
                store_list.append(list_row)
                count_match = count_match + 1
            elif store_fd_amzn[j]["date"] == store_json[i]["Date"] and count_match != 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = 0
                list_row[3] = 0
                list_row[4] = store_fd_amzn[j]['id']
                list_row[5] = datetime.datetime.strptime(store_fd_amzn[j]['date'],'%d/%m/%Y')
                list_row[6] = store_fd_amzn[j]['title']
                list_row[7] = store_fd_amzn[j]['description'][0:store_fd_amzn[j]['description'].find('<img',0)]
                store_list.append(list_row)
        if count_match == 0 :
                list_row[0] = datetime.datetime.strptime(store_json[i]['Date'],'%d/%m/%Y')
                list_row[1] = store_json[i]['Security']['Symbol']
                list_row[2] = store_json[i]['Last']
                list_row[3] = store_json[i]['Volume']
                list_row[4] = ''
                list_row[5] = ''
                list_row[6] = ''
                list_row[7] = ''
                store_list.append(list_row)

"""
/*
DB = MySQL
schema name = db_python
user db name = db_python_user
user db password = password
*/

CREATE TABLE `stocks_n_news` (
  `close_date` date NOT NULL,
  `stock_name` varchar(45) NOT NULL,
  `closed_price` float DEFAULT NULL,
  `closed_volume` float DEFAULT NULL,
  `news_id` varchar(50) NULL,
  `stock_name` varchar(50) DEFAULT NULL,
  `news_date` date DEFAULT NULL,
  `news_title` longtext,
  `news_desc` longtext,
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""
db = pymysql.connect(host='localhost',          # your host, usually localhost
                     user='db_python_user',     # your username
                     passwd='password',         # your password
                     db='db_python')            # name of the data base

cur = db.cursor()

insert_str = 'INSERT INTO db_python.stocks_n_news (close_date,stock_name,closed_price,closed_volume,news_id,stock_name,news_date,news_title,news_desc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
cur.executemany(insert_str,store_list)
#cur.execute('delete from db_python.stocks_n_news')
cur.execute('commit')

#cur.execute('SELECT * FROM stocks_n_news')
#for row in cur.fetchall():
#    print(row[0])
db.close()
