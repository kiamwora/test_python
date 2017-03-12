# -*- coding: utf-8 -*-
import requests
import json
import csv
import datetime
import feedparser

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

get_days = 30
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
#=====export csv file
with open('stock_news.csv' , 'w' , newline='', encoding='utf-8') as csvfile:
    fieldnames = ['closed_date', 'stock_name' , 'closed_price' , 'closed_volume','news_id' , 'news_date' , 'news_title' , 'news_desc']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    i = 0
    for i in range(0,len(store_json)):
        count_match = 0
        if store_json[i]['Security']['Symbol'] == 'AAPL' :
            j = 0
            for j in range(0,len(store_fd_aapl)):
                if store_fd_aapl[j]['date'] == store_json[i]['Date'] and count_match == 0 :
                    writer.writerow({
                        'closed_date': store_json[i]['Date']
                        ,'stock_name': store_json[i]['Security']['Symbol']
                        ,'closed_price': store_json[i]['Last']
                        ,'closed_volume': store_json[i]['Volume']
                        ,'news_id': store_fd_aapl[j]['id']
                        ,'news_date': store_fd_aapl[j]['date']
                        ,'news_title': store_fd_aapl[j]['title']
                        ,'news_desc': store_fd_aapl[j]['description'][0:store_fd_aapl[j]['description'].find('<img',0)]
                        })
                    count_match = count_match + 1
                elif store_fd_aapl[j]['date'] == store_json[i]['Date'] and count_match != 0 :
                    writer.writerow({
                        'closed_date': store_json[i]['Date']
                        ,'stock_name': store_json[i]['Security']['Symbol']
                        ,'closed_price': 0
                        ,'closed_volume': 0
                        ,'news_id': store_fd_aapl[j]['id']
                        ,'news_date': store_fd_aapl[j]['date']
                        ,'news_title': store_fd_aapl[j]['title']
                        ,'news_desc': store_fd_aapl[j]['description'][0:store_fd_aapl[j]['description'].find('<img',0)]
                        })
            if count_match == 0 :
                    writer.writerow({
                        'closed_date': store_json[i]["Date"]
                        ,'stock_name': store_json[i]["Security"]["Symbol"]
                        ,'closed_price': store_json[i]["Last"]
                        ,'closed_volume': store_json[i]["Volume"]
                        ,'news_id': ''
                        ,'news_date': ''
                        ,'news_title': ''
                        ,'news_desc': ''
                        })                
        if store_json[i]['Security']['Symbol'] == 'GOOG' :
            j = 0
            for j in range(0,len(store_fd_goog)):
                if store_fd_goog[j]['date'] == store_json[i]['Date'] and count_match == 0 :
                    writer.writerow({
                        'closed_date': store_json[i]['Date']
                        ,'stock_name': store_json[i]['Security']['Symbol']
                        ,'closed_price': store_json[i]['Last']
                        ,'closed_volume': store_json[i]['Volume']
                        ,'news_id': store_fd_goog[j]['id']
                        ,'news_date': store_fd_goog[j]['date']
                        ,'news_title': store_fd_goog[j]['title']
                        ,'news_desc': store_fd_goog[j]['description'][0:store_fd_goog[j]['description'].find('<img',0)]
                        })
                    count_match = count_match + 1
                elif store_fd_goog[j]['date'] == store_json[i]['Date'] and count_match != 0 :
                    writer.writerow({
                        'closed_date': store_json[i]['Date']
                        ,'stock_name': store_json[i]['Security']['Symbol']
                        ,'closed_price': 0
                        ,'closed_volume': 0
                        ,'news_id': store_fd_goog[j]['id']
                        ,'news_date': store_fd_goog[j]['date']
                        ,'news_title': store_fd_goog[j]['title']
                        ,'news_desc': store_fd_goog[j]['description'][0:store_fd_goog[j]['description'].find('<img',0)]
                        })               
            if count_match == 0 :
                    writer.writerow({
                        'closed_date': store_json[i]["Date"]
                        ,'stock_name': store_json[i]["Security"]["Symbol"]
                        ,'closed_price': store_json[i]["Last"]
                        ,'closed_volume': store_json[i]["Volume"]
                        ,'news_id': ''
                        ,'news_date': ''
                        ,'news_title': ''
                        ,'news_desc': ''
                        })                
        if store_json[i]['Security']['Symbol'] == 'AMZN' :
            j = 0
            for j in range(0,len(store_fd_amzn)):
                if store_fd_amzn[j]['date'] == store_json[i]['Date'] and count_match == 0 :
                    writer.writerow({
                        'closed_date': store_json[i]['Date']
                        ,'stock_name': store_json[i]['Security']['Symbol']
                        ,'closed_price': store_json[i]['Last']
                        ,'closed_volume': store_json[i]['Volume']
                        ,'news_id': store_fd_amzn[j]['id']
                        ,'news_date': store_fd_amzn[j]['date']
                        ,'news_title': store_fd_amzn[j]['title']
                        ,'news_desc': store_fd_amzn[j]['description'][0:store_fd_amzn[j]['description'].find('<img',0)]
                        })
                    count_match = count_match + 1
                elif store_fd_amzn[j]["date"] == store_json[i]["Date"] and count_match != 0 :
                    writer.writerow({
                        'closed_date': store_json[i]['Date']
                        ,'stock_name': store_json[i]['Security']['Symbol']
                        ,'closed_price': 0
                        ,'closed_volume': 0
                        ,'news_id': store_fd_amzn[j]['id']
                        ,'news_date': store_fd_amzn[j]['date']
                        ,'news_title': store_fd_amzn[j]['title']
                        ,'news_desc': store_fd_amzn[j]['description'][0:store_fd_amzn[j]['description'].find('<img',0)]
                        })               
            if count_match == 0 :
                    writer.writerow({
                        'closed_date': store_json[i]["Date"]
                        ,'stock_name': store_json[i]["Security"]["Symbol"]
                        ,'closed_price': store_json[i]["Last"]
                        ,'closed_volume': store_json[i]["Volume"]
                        ,'news_id': ''
                        ,'news_date': ''
                        ,'news_title': ''
                        ,'news_desc': ''
                        })                
        
    csvfile.close()
    