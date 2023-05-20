from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import pandas as pd


# Set up Chrome driver
chrome_options = Options()

url = 'https://www.casablanca-bourse.com/bourseweb/en/Listed-Company.aspx?IdLink=245&Cat=7'
print("1")
service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # Replace with the path to your ChromeDriver executable
print("2")
driver = webdriver.Chrome(service=service, options=chrome_options)
print("3")
# Open the website
print("opening chrome ... ")
driver.get(url)

desired_table = driver.execute_script(
        "return document.evaluate(\"//table[.//tr[td[contains(., 'ISIN code')]]]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;")
time.sleep(5)

# Extract the table content
table_content = driver.execute_script("return arguments[0].outerHTML;", desired_table)
data_isin_name = pd.DataFrame(pd.read_html(table_content)[0])
session_index = data_isin_name[data_isin_name[1] == 'ISIN code'].index[0]

# Filter the DataFrame
filtered_df = data_isin_name.iloc[session_index : session_index + 76,1:6:2]

# Reset the index of the filtered DataFrame
filtered_df.reset_index(drop=True,inplace=True)
filtered_df.dropna(inplace=True)
filtered_df.columns = filtered_df.iloc[0,:]
filtered_df.drop([0],inplace=True)
filtered_df.reset_index(drop=True,inplace=True)
filtered_df.to_csv("ISIN_sectors_ma.csv")
print("1")