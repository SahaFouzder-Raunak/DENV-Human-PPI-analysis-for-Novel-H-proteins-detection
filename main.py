from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd


result_data = pd.read_csv("test_proteins_19k.csv")
column_list = ["PCP_PC",	"PCP_NC",	"PCP_NE",	"PCP_PO",	"PCP_NP",	"PCP_AL",	"PCP_CY",	"PCP_AR",	"PCP_AC",	"PCP_BS",
               	"PCP_NE_pH",	"PCP_HB",	"PCP_HL",	"PCP_NT",	"PCP_HX",	"PCP_SC",	"PCP_TN",	"PCP_SM",	"PCP_LR"]
for idx in column_list:
  result_data.insert(len(result_data.columns), idx, None)

driver = webdriver.Firefox()
driver.get("https://webs.iiitd.edu.in/raghava/pfeature/physio.php")

# checking negatively charged
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)")
elem.click()
# checking neutral charged
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3) > input:nth-child(1)")
elem.click()
# checking aliphaticity
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(3) > input:nth-child(1)")
elem.click()
# checking acidity
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(3) > input:nth-child(1)")
elem.click()
# checking neutral ph
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > input:nth-child(1)")
elem.click()
# checking neutral
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(2) > input:nth-child(1)")
elem.click()
# checking hydroxylic
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(6) > td:nth-child(3) > input:nth-child(1)")
elem.click()
# checking tiny
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(7) > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(2) > input:nth-child(1)")
elem.click()

for rowidx, row in result_data.iterrows():
  # clicking on the uniprod id option
  elem = driver.find_element(By.CSS_SELECTOR, ".background > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(1) > input:nth-child(1)")
  elem.click()

  # entering the uniprod id
  elem = driver.find_element(By.CSS_SELECTOR, ".background > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(1) > input:nth-child(4)")
  elem.clear()
  elem.send_keys(row['uniprod_id'])


  # clicking submit
  elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(8) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)")
  elem.click()

  # waiting for page to load
  wait = WebDriverWait(driver, 60)
  element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tablesaw')))

  # getting the values
  ids = driver.find_elements(By.CSS_SELECTOR, ".tablesaw > tbody:nth-child(2) > tr:nth-child(1) > td")
  values = driver.find_elements(By.CSS_SELECTOR, ".tablesaw > tbody:nth-child(2) > tr:nth-child(2) > td")
  try:
    for index, idx in enumerate(ids[1:]):
       result_data[idx.text][rowidx] = values[index+1].text
  except TimeoutException:
    driver.implicitly_wait(20)
    for index, idx in enumerate(ids[1:]):
       result_data[idx.text][rowidx] = values[index+1].text
  except:
    print(row["uniprod_id"])
  driver.back()


driver.close()

result_data.to_csv("test_proteins_19k.csv")