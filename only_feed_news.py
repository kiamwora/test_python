# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 14:33:25 2017

@author: kiamw
"""
import feedparser
import csv
import datetime

today = datetime.date.today()

fd_aapl = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=AAPL')
fd_goog = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=GOOG')
fd_amzn = feedparser.parse('http://articlefeeds.nasdaq.com/nasdaq/symbols?symbol=AMZN')

store_fd_aapl = []
for i in range(0,len(fd_aapl['entries'])):
    today = datetime.datetime.strptime(fd_aapl['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_aapl['entries'][i]["date"] = today.strftime('%d/%m/%Y')
    store_fd_aapl.append(fd_aapl['entries'][i])

#print(store_fd_aapl[29]['date'])

store_fd_goog = []
for i in range(0,len(fd_goog['entries'])):
    today = datetime.datetime.strptime(fd_goog['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_goog['entries'][i]["date"] = today.strftime('%d/%m/%Y')
    store_fd_goog.append(fd_goog['entries'][i])

#print(store_fd_goog[29]['date'])

store_fd_amzn = []
for i in range(0,len(fd_amzn['entries'])):
    today = datetime.datetime.strptime(fd_amzn['entries'][i]["date"],'%Y-%m-%dT%H:%M:%SZ')
    fd_amzn['entries'][i]["date"] = today.strftime('%d/%m/%Y')
    store_fd_amzn.append(fd_amzn['entries'][i])

#print(store_fd_amzn[29]['date'])

with open('news.csv' , 'w' , newline='', encoding='utf-8') as csvfile:
    fieldnames = ['news_id', 'stock_name' , 'news_date' , 'news_title' , 'news_desc']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(0,30):
        writer.writerow({
                        'news_id': store_fd_aapl[i]["id"]
                        ,'stock_name': 'AAPL'
                        ,'news_date': store_fd_aapl[i]["date"]
                        ,'news_title': store_fd_aapl[i]["title"]
                        ,'news_desc': store_fd_aapl[i]["description"][0:store_fd_aapl[i]["description"].find('<img',0)]
                        })
    for i in range(0,30):
        writer.writerow({
                        'news_id': store_fd_goog[i]["id"]
                        ,'stock_name': 'GOOG'
                        ,'news_date': store_fd_goog[i]["date"]
                        ,'news_title': store_fd_goog[i]["title"]
                        ,'news_desc': store_fd_goog[i]["description"][0:store_fd_goog[i]["description"].find('<img',0)]
                        })
    for i in range(0,30):
        writer.writerow({
                        'news_id': store_fd_amzn[i]["id"]
                        ,'stock_name': 'AMZN'
                        ,'news_date': store_fd_amzn[i]["date"]
                        ,'news_title': store_fd_amzn[i]["title"]
                        ,'news_desc': store_fd_amzn[i]["description"][0:store_fd_amzn[i]["description"].find('<img',0)]
                        })
    csvfile.close()

print(len(fd_aapl['entries']))
print(fd_aapl['entries'][0]['id'])
print(fd_aapl['entries'][0]['date'])
print(fd_aapl['entries'][0]['title'])
print(fd_aapl['entries'][0]['description'])
