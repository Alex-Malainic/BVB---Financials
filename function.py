import requests
from bs4 import BeautifulSoup
import pandas as pd

url = ("ALR", "TLV", "BRD","BVB","TEL","COTE","DIGI","FP","M","SNP","WINE","SNN","SNG","TGN","SFG","TRP")
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
