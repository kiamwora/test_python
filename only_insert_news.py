# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 14:51:29 2017

@author: kiamw
"""

#import MySQLdb
import pymysql
import feedparser
import datetime

today = datetime.date.today()
list_row = ['','','','','']

fd_aapl = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=AAPL')
fd_goog = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=GOOG')
fd_amzn = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=AMZN')

store_fd_aapl = []
for i in range(0,len(fd_aapl['entries'])):
    list_row = ['','','','','']
    today = datetime.datetime.strptime(fd_aapl['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_aapl['entries'][i]["date"] = today.strftime('%d/%m/%Y')
    list_row[0] = fd_aapl['entries'][i]['id']
    list_row[1] = 'AAPL'
    list_row[2] = datetime.datetime.strptime(today.strftime('%d/%m/%Y'),'%d/%m/%Y')
    list_row[3] = fd_aapl['entries'][i]['title']
    list_row[4] = fd_aapl['entries'][i]['description'][0:fd_aapl['entries'][i]['description'].find('<img',0)]
    store_fd_aapl.append(list_row)
#print(store_fd_aapl[29])

store_fd_goog = []
for i in range(0,len(fd_aapl['entries'])):
    list_row = ['','','','','']
    today = datetime.datetime.strptime(fd_goog['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_goog['entries'][i]["date"] = today.strftime('%d/%m/%Y')
    list_row[0] = fd_goog['entries'][i]['id']
    list_row[1] = 'GOOG'
    list_row[2] = datetime.datetime.strptime(today.strftime('%d/%m/%Y'),'%d/%m/%Y')
    list_row[3] = fd_goog['entries'][i]['title']
    list_row[4] = fd_goog['entries'][i]['description'][0:fd_goog['entries'][i]['description'].find('<img',0)]
    store_fd_goog.append(list_row)

store_fd_amzn = []
for i in range(0,len(fd_aapl['entries'])):
    list_row = ['','','','','']
    today = datetime.datetime.strptime(fd_amzn['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_amzn['entries'][i]["date"] = today.strftime('%d/%m/%Y')
    list_row[0] = fd_amzn['entries'][i]['id']
    list_row[1] = 'AMZN'
    list_row[2] = datetime.datetime.strptime(today.strftime('%d/%m/%Y'),'%d/%m/%Y')
    list_row[3] = fd_amzn['entries'][i]['title']
    list_row[4] = fd_amzn['entries'][i]['description'][0:fd_amzn['entries'][i]['description'].find('<img',0)]
    store_fd_amzn.append(list_row)

"""
/*
DB = MySQL
schema name = db_python
user db name = db_python_user
user db password = password
*/

CREATE TABLE `news` (
  `news_id` varchar(50) NOT NULL,
  `stock_name` varchar(50) DEFAULT NULL,
  `news_date` date DEFAULT NULL,
  `news_title` longtext,
  `news_desc` longtext,
  PRIMARY KEY (`news_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""
db = pymysql.connect(host='localhost',          # your host, usually localhost
                     user='db_python_user',     # your username
                     passwd='password',         # your password
                     db='db_python')            # name of the data base

cur = db.cursor()

insert_str = 'INSERT INTO db_python.news (news_id,stock_name,news_date,news_title,news_desc) VALUES (%s,%s,%s,%s,%s)'
cur.executemany(insert_str,store_fd_aapl)
cur.executemany(insert_str,store_fd_goog)
cur.executemany(insert_str,store_fd_amzn)
#cur.execute('delete from db_python.news')
cur.execute('commit')

#cur.execute('SELECT * FROM news')
#for row in cur.fetchall():
#    print(row[0])
db.close()
