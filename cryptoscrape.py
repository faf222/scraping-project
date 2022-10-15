#imports
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import time

#make page requests and convert to beautiful soup
page = requests.get('https://coinmarketcap.com/')
soup = BeautifulSoup(page.content, 'html.parser')

#isolate the areas where the desired data is being stored
crypto_names = soup.select("td div a div div p")
crypto_prices = soup.select('td div a span')

#seperate names from acronyms
for index, name in enumerate(crypto_names):
    if index % 2 == 1:
        crypto_names[index] = None
    else:
        crypto_names[index] = name.getText()
names = []

#shorten list / remove blank patches
for index, item in enumerate(crypto_names):
    if crypto_names[index] == None:
        pass
    else:
        names.append(crypto_names[index])

#clean up the list of prices
for index, price in enumerate(crypto_prices):
    crypto_prices[index] = round(float(price.getText().strip("$").replace(',','')), 2)

#open text file containing previous scan through
f = open('CryptoInfo.txt', 'r')
f.readline()

#saving all the previous information to a new list and then calcualting the differences in value
changes = []
for p in range(len(crypto_prices)):
    j = f.readline()
    i = str(j)
    q = re.search(r'\d*\.\d\d', i)
    changes.append(float(q.group(0)))
for index, other in enumerate(changes):
    changes[index] = round(crypto_prices[index] - changes[index], 2)

#create table
graph = pd.DataFrame({
    'Names:': names,
    'Values:': crypto_prices,
    'Recent Change:': changes
})

#paste new graph into text file storing up to date information
f = open('CryptoInfo.txt', 'w')
f.write(str(graph))

#save the change in value to a log text file and record the date and time
g = open('ChangesInfo.txt', 'a')
g.write(str(changes) + ' ')
g.write(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '\n')