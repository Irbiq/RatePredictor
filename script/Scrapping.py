from bs4 import BeautifulSoup
import lxml
import requests
import json
from Currency import Currency, Decimal
from DbManager import DbManager

url_banks = 'https://banki24.by/minsk/kurs/usd'
url_nb ='http://www.nbrb.by/API/ExRates/Rates/145'

r_b = requests.get(url_banks)
r_nb = requests.get(url_nb)

#print(nb_cur_rate)

banks_html = r_b.text

soup = BeautifulSoup(banks_html)
s = soup.find('tbody')
soup = BeautifulSoup(str(s))
s1 = soup.find_all('tr',class_='')
#exch_list contain exch rates of all active banks
exch_list = []
for i,v in enumerate(s1):
    data = v.text.strip().split('\n')
    cur = Currency(data[0],data[1].replace(',','.'),data[2].replace(',','.'))
    exch_list.append(cur)

#nb_cur_rate contains national bank exch rate
nb_cur_rate = Decimal(json.loads(r_nb.text)['Cur_OfficialRate'])

#print(nb_cur_rate)
#print(exch_list)

dbm = DbManager()
dbm.insert_exchs(exch_list)
dbm.insert_exchs_nb_single(nb_cur_rate)
'''END'''