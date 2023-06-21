import csv
import webbrowser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
import time
import pymysql
import datetime
import dotenv
import os
import sys
import unidecode

dotenv.load_dotenv()

chromepath = r"C:\Users\yuvvi\Downloads\chromedriver_win32\chromedriver"

options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

options.add_argument("--start-maximized")

chrome_driver = chromepath

driver = webdriver.Chrome(options=options,service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

today = datetime.datetime.now()

#daysago = int(sys.argv[1])

threedaysago = "0" + str(today.month) + "/" + str(today.day-3) + "/" + str(today.year)
 
"06/15/2023"
# Create a connection object
#conn = pymysql.connect(
#  host='localhost',
#  user='admin',
#  password='p1',
#  database='test'
#)

# Create a connection object
conn = pymysql.connect(
  host=os.getenv("HOST"),
  user=os.getenv("USER"),
  password=os.getenv("PASSWORD"),
  database=os.getenv("DATABASE")
)
cur = conn.cursor()

#Select trans.addshipoption, customer.email , customer.fname, customer.lname from trans inner join customer on trans.customer= customer.id where trans.transdate like '06/16/2023' and trans.tracking like '%US'
query = "Select trans.addshipoption, customer.email, customer.fname, customer.lname from trans inner join customer on trans.customer = customer.id where trans.transdate like '" + threedaysago + "' and trans.tracking like '%US'"

cur.execute(query)

results = cur.fetchall()

print(results)

rows = len(results)


i = 0   
while i < rows:
  
    resultrow = results[i]
    fnamelname = resultrow[2] + " " + resultrow[3].strip()
    driver.get('https://tools.usps.com/go/TrackConfirmAction_input?strOrigTrackNum=' + str(resultrow[0]))

    time.sleep(3)

    dropdown = driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/div/div/div/div/div[2]/div/div/div/div[1]/div[1]/h4/a")
    dropdown.click()

    time.sleep(3)

    checkbox = driver.find_element(By.ID, "emailAll_1")
    driver.execute_script("arguments[0].click();", checkbox)

    time.sleep(6)

    outputString = unidecode.unidecode(fnamelname)
    inputFirstlast = driver.find_element(By.ID, "emailUpdate_name1_1")
    inputFirstlast.send_keys(outputString)

    time.sleep(7)

    inputEmail = driver.find_element(By.ID, "emailUpdate_email1_1")
    inputEmail.send_keys(resultrow[1])

    time.sleep(3)

    termsandconditions = driver.find_element(By.ID, "agreedTextUpdates_1")
    driver.execute_script("arguments[0].click();", termsandconditions)

    time.sleep(3)

    getupdates = driver.find_element(By.ID, "teuButton_1")
    #driver.execute_script("arguments[0].click();", getupdates)

    time.sleep(4)

    i = i + 1

#if i == rows:
    #driver.quit()



  

