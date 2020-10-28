## fetch live stock price and store in CSV file

import sys
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import date
from datetime import datetime
import nsetools
from nsetools import Nse


def fetch_NSE_stock_price(stock_code):
    
    stock_url  = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol='+str(stock_code)
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
    response = requests.get(stock_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    data_array = soup.find(id='responseDiv').getText().strip().split(":")
    for item in data_array:
        if 'lastPrice' in item:
            index = data_array.index(item)+1
            latestPrice=data_array[index].split('"')[1]
            return (float(latestPrice.replace(',','')))
    
n=input("Enter stock code:")
fetch_NSE_stock_price(n)

t_iteration=int(input("Number of observations:"))
d_sleep=int(input("Time interval(in seconds):"))

data_file=open(n+"_NSE_stock.csv",'w');

iteration=0
while iteration<t_iteration:
    c_date = date.today().strftime("%B %d, %Y")
    c_time = datetime.now().strftime("%H:%M:%S")
    current_stock_price = fetch_NSE_stock_price(n)
    print (n + ',' + c_date + ','  + c_time + ',' + str(current_stock_price) )
    print(c_time + ',' + str(current_stock_price), file=data_file)
    time.sleep(d_sleep)
    iteration = iteration + 1

data_file.close()


import matplotlib.pyplot as plt
import csv
import numpy as np

x=[]
y=[]

with open(n+"_NSE_stock.csv", 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(row[0])
        y.append(float(row[1]))


plt.plot(x,y, marker='o')

plt.title('Data from the CSV File: Stock Price v/s Time')

plt.xlabel('Time')
plt.ylabel('Stock Price')

plt.show()
data = np.genfromtxt("SBIN_NSE_stock.csv", delimiter=",", names=["x", "y"])
plt.plot(data['x'], data['y'])

    
