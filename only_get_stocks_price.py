# -*- coding: utf-8 -*-
import requests
import json
import csv
import datetime

#=====setup url for call api web service
#url = 'http://www.xignite.com/xGlobalHistorical.json/GetGlobalHistoricalQuote?IdentifierType=Symbol&Identifier=AAPL&AdjustmentMethod=None&AsOfDate=03/07/2017'
#url_aapl = 'http://www.xignite.com/xGlobalHistorical.json/GetGlobalHistoricalQuote?IdentifierType=Symbol&Identifier=AAPL&AdjustmentMethod=None&AsOfDate='
#url_goog = 'http://www.xignite.com/xGlobalHistorical.json/GetGlobalHistoricalQuote?IdentifierType=Symbol&Identifier=GOOG&AdjustmentMethod=None&AsOfDate='
#url_amzn = 'http://www.xignite.com/xGlobalHistorical.json/GetGlobalHistoricalQuote?IdentifierType=Symbol&Identifier=AMZN&AdjustmentMethod=None&AsOfDate='
#print(url + today.strftime('%m/%d/%Y'))
url_all = 'http://www.xignite.com/xGlobalHistorical.json/GetGlobalHistoricalQuotes?IdentifierType=Symbol&Identifiers=AAPL,GOOG,AMZN&AdjustmentMethod=None&AsOfDate='

#today = datetime.date.today()
#today = today + datetime.timedelta(days=-1)
#=====for call api web service
#response = requests.get(url_aapl + today.strftime('%m/%d/%Y'), headers={'Authorization' : 'TOK:55FDF5CFAE02494B816DCD4E792A1E3F'})
#response = requests.get(url_goog + today.strftime('%m/%d/%Y'), headers={'Authorization' : 'TOK:55FDF5CFAE02494B816DCD4E792A1E3F'})
#response = requests.get(url_amzn + today.strftime('%m/%d/%Y'), headers={'Authorization' : 'TOK:55FDF5CFAE02494B816DCD4E792A1E3F'})
response = requests.get(url_all + today.strftime('%m/%d/%Y'), headers={'Authorization' : 'TOK:D19818E34FC2442E9478D3E673549DB9'})
data_test = response.json()
print(data_test) #ALL
#print(data) #ALL
#print('=========')
#print(data[0]) #AAPL
#print('=========')
#print(data[1]) #GOOG
#print('=========')
#print(data[2]) #AMZN
#print('=========')
#print(len(data))
#print(data[2]["Security"]["Symbol"]) #AMZN

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

with open('stock.csv' , 'w' , newline='', encoding='utf-8') as csvfile:
    fieldnames = ['closed_date', 'stock_name' , 'closed_price' , 'closed_volume']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(0,len(store_json)):
        writer.writerow({
                        'closed_date': store_json[i]["Date"]
                        ,'stock_name': store_json[i]["Security"]["Symbol"]
                        ,'closed_price': store_json[i]["Last"]
                        ,'closed_volume': store_json[i]["Volume"]
                        })
    csvfile.close()
    