# test_python

1. execute "only_feed_news.py" for get news from feed and export to csv file.
2. execute "only_get_stocks_price.py" for get stocks closed price in previous 30 days and export to csv file.
3. execute "feed_news_plus_stocks_price.py" for get news and stocks closed price in previous 30 days and export both to csv file.
4. execute "only_insert_news.py" for get news from feed and insert to table "news" in database.
5. execute "only_insert_stick.py" for get stocks closed price in previous 30 days and insert to table "stocks" in database.
6. execute "insert_stocks_news.py" for get news and stocks closed price in previous 30 days and insert to table "stocks_n_news" in database.
7. run_python.bat for setup window schedule task to automate run script get data.

* result_only_feed_news.csv is result from item 1
* result_only_get_price_stocks.csv is result from item 2
* result_feed_news_plus_get_stocks_price.csv is result from item 3

*** if you try to execute get stocks price 1st time you cannot get any data because this API has not map your IP address with API service. In 1st time you will get message like below , please send this IP address to me for map IP with API service. (because I use this API service in tril version)


***** message sample : [{'Security': None, 'Date': '', 'Last': 0.0, 'Open': 0.0, 'High': 0.0, 'Low': 0.0, 'Volume': 0.0, 'LastClose': 0.0, 'ChangeFromOpen': 0.0, 'PercentChangeFromOpen': 0.0, 'ChangeFromLastClose': 0.0, 'PercentChangeFromLastClose': 0.0, 'SplitRatio': 1.0, 'CummulativeCashDividend': 0.0, 'CummulativeStockDividendRatio': 1.0, 'Currency': 'USD', 'AdjustmentMethodUsed': 'All', 'DataConfidence': 'Valid', 'Outcome': 'RegistrationError', 'Message': 'XigniteGlobalHistorical: Maximum number of unregistered requests exceeded. Consider registering or subscribing to expand usage. Your request was authenticated using  your IP address (27.145.43.50). Please visit http://www.xignite.com/registration-help for more information.', 'Identity': 'IP', 'Delay': 0.0}]
