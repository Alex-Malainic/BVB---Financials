import requests
from bs4 import BeautifulSoup
import pandas as pd


#getting all company names available from bvb

url_file = "https://bvb.ro/FinancialInstruments/Markets/SharesListForDownload.ashx"
resp = requests.get(url_file)
with open('companylist.csv', 'wb') as f:
    f.write(resp.content)
compdf = pd.read_csv('companylist.csv', sep = ";")
url = list((compdf.iloc[:,0]))

#web scraping for data
df = pd.DataFrame()
for p in url:
    link = 'https://www.bvb.ro/FinancialInstruments/Details/FinancialInstrumentsDetails.aspx?s=' + p
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    indic = soup.find("table", {"id": "ctl00_body_ctl02_IndicatorsControl_dvIndicators"}) #getting the Indicators table
    prices = list(indic.find_all('tr')) #transformed the table into a List that can be manipulated


    n = 0
    bet={}

    for i in prices:
        values = str(i).split("<b>")[1].split("</b>")[0].replace(",", "")
        indicators = str(i).split("</td>")[0].split("td")[1].split(">")[1].replace(".","")
        bet[indicators] = values
    df = df.append(bet, ignore_index=True)

df.index = url
df.to_csv("Companies.csv")

