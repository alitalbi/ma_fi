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


#chrome_options.add_argument("--headless")  # Run Chrome in headless mode
print("1")
service = Service(r"C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # Replace with the path to your ChromeDriver executable
print("2")
driver = webdriver.Chrome(service=service, options=chrome_options)
print("3")
# Open the website
print("opening chrome ... ")
driver.get("https://www.casablanca-bourse.com/bourseweb/en/Negociation-History.aspx?Cat=24&IdLink=225")
print("Chrome opened")
# Execute JavaScript code to count the number of options
num_options = driver.execute_script("return document.getElementById('HistoriqueNegociation1_HistValeur1_DDValeur').options.length;") - 1 #the first is "choose an instrument" so we take it off

stocks_name = driver.execute_script("var select = document.getElementById('HistoriqueNegociation1_HistValeur1_DDValeur');"
                                     "var texts = [];"
                                     "for (var i = 0; i < select.options.length; i++) {"
                                     "    texts.push(select.options[i].text.trim());"
                                     "}"
                                     "return texts;")[1:]

print("Number of options:", num_options)
print("Option values:", stocks_name)
driver.execute_script("document.getElementById('HistoriqueNegociation1_HistValeur1_DDuree').selectedIndex = 5;")
#for elem in range(1,num_options):
# Choose the period
for elem in range(0,num_options):

    # Choose the instrument
    driver.execute_script("document.getElementById('HistoriqueNegociation1_HistValeur1_DDValeur').selectedIndex = "+str(elem+1)+";")
    time.sleep(4)
    # Click on the "Validate" button
    driver.execute_script("document.getElementById('HistoriqueNegociation1_HistValeur1_ImageButton1').click();")
    time.sleep(5)
    # Wait for the desired table to be visible

    # Wait until the desired table is present
    desired_table = driver.execute_script(
        "return document.evaluate(\"//table[.//tr[td[contains(., 'Session')]]]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;")
    time.sleep(5)

    # Extract the table content
    table_content = driver.execute_script("return arguments[0].outerHTML;", desired_table)

    # Extract the rows
    unstructured_data = pd.read_html(table_content)[0]
    # Find the index of the row with the text "Session"
    session_index = unstructured_data[unstructured_data[1] == 'Session'].index[0]

    # Filter the DataFrame
    filtered_df = unstructured_data.iloc[session_index : session_index + 753,1:16:2]

    # Reset the index of the filtered DataFrame
    filtered_df.reset_index(drop=True,inplace=True)
    filtered_df.columns = filtered_df.iloc[0,:]
    filtered_df.drop([0,1],inplace=True)
    filtered_df.reset_index(drop=True,inplace=True)
    filtered_df.to_csv(stocks_name[elem]+".csv")
    time.sleep(5)
driver.quit()
