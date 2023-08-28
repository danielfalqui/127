#automação de navegadores
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# analisar ou separar texto como HTML e, executar ações nele
from bs4 import BeautifulSoup


#Manipular tempo
import time

#Permite exportar os dados que coletamos em um arquivo CSV
import pandas as pd


#Instalar gerenciador de driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# URL dos Exoplanetas da NASA
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"


# Webdriver
browser = webdriver.Chrome()
browser.get(START_URL)

time.sleep(10)

scraped_data = []

def scrape():
    #objeto beautful soup
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    #localize a tabela
    bright_star_table = soup.find("table", attrs={"class", "wikitable"})

    #localize o body
    table_body = bright_star_table.find("tbody")

    #localize tr
    table_rows = table_body.find_all("tr")

    #obtendo os dados de td
    for row in table_rows:
        table_cols = row.find_all("td")
        temp_list = []

        for col_data in  table_cols:
            data = col_data.text.strip()
            temp_list.append(data)

        scraped_data.append(temp_list)

    
scrape()

#importe os dados para csv

stars_data = []

for i in range(0,len(scraped_data)):
    Star_names = scraped_data[i][1]
    Distance = scraped_data[i][3]
    Mass = scraped_data[i][5]
    Radius = scraped_data[i][6]
    Lum = scraped_data[i][7]

    required_data = [Star_names,Distance,Mass,Radius,Lum]
    stars_data.append(required_data)

print(stars_data)

#defina o cabeçalho

headers = ['Star_names','Distance','Mass','Radius','Luminosity']

stars_df_1 = pd.DataFrame(stars_data,columns=headers)

stars_df_1.to_csv('scraped_data.csv', index=True,index_label='id')