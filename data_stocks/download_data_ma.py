import random
import requests
import matplotlib.pyplot as plt
import json
import numpy as np
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
# Define your own User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    # Add more User Agents as needed
]

dict_isin_map = {}
def rand_agent() -> str:
    """Select a random User-Agent from USER_AGENTS

    Returns:
        str: User-Agent string
    """
    return random.choice(USER_AGENTS)

def get_request(url: str) -> requests.models.Response:
    """Make a request

    Args:
        url (str): Resource URL

    Returns:
        requests.models.Response: Response object
    """
    headers = {"User-Agent": rand_agent()}
    return requests.get(url, headers=headers)


# Set up Chrome driver
chrome_options = Options()


service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # Replace with the path to your ChromeDriver executable
driver = webdriver.Chrome(service=service, options=chrome_options)


isins_sector_data = pd.read_csv("ISIN_sectors_ma.csv").iloc[:,1:]

for index in range(len(isins_sector_data.Instrument)):
    dict_isin_map[isins_sector_data.Instrument[index]] = {isins_sector_data["ISIN code"][index]}

for k,v in dict_isin_map.items():
    if list(v)[0] == "MA0000012551" or list(v)[0] == "MA0000012593":#prob with leviver and med paper isins
        continue
    url = "https://medias24.com/content/api?method=getStockOHLC&ISIN="+list(v)[0]+"&format=json"
    driver.get(url)
    body_element = driver.find_element(By.TAG_NAME,"body")
    inner_html = body_element.get_attribute('innerHTML').split("{\"result\":")[1].split(",\"message\":\"200 OK\"")[0]

    if "null" in inner_html:
        inner_html = inner_html.replace("null","-1")
    print(inner_html)
    stock_data = pd.DataFrame(eval(inner_html), columns=['Timestamp', '?', 'High', 'Low', 'Price', 'Volume'])
    stock_data["Timestamp"] = stock_data["Timestamp"].apply(lambda x:datetime.fromtimestamp(x/1000))

    stock_data.set_index("Timestamp",inplace=True)
    stock_data.drop("?",axis=1,inplace=True)

    stock_data.to_csv(k+".csv")
print("made it")