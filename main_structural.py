from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd


result_data = pd.read_csv("mixture_8.csv")
column_list = ["PCP_SS_HE",	"PCP_SS_ST",	"PCP_SS_CO",	"PCP_SA_BU",	"PCP_SA_EX",	"PCP_SA_IN"]
for idx in column_list:
  result_data.insert(len(result_data.columns), idx, None)

driver = webdriver.Firefox()
driver.get("https://webs.iiitd.edu.in/raghava/pfeature/physico_str.php")

# checking secondary structure strands
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(2) > input:nth-child(1)")
elem.click()
# checking secondary structure coil
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(3) > input:nth-child(1)")
elem.click()
# checking solvent accesibility exposed
elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(4) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > input:nth-child(1)")
elem.click()

# clicking on the uniprod id option
elem = driver.find_element(By.CSS_SELECTOR, ".background > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(1) > input:nth-child(1)")
elem.click()

for rowidx, row in result_data.iterrows():
  # entering the uniprod id
  elem = driver.find_element(By.CSS_SELECTOR, ".background > tbody:nth-child(1) > tr:nth-child(7) > td:nth-child(1) > input:nth-child(4)")
  elem.clear()
  elem.send_keys(row['uniprod_id'])


  # clicking submit
  elem = driver.find_element(By.CSS_SELECTOR, "main.hoc > div:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)")
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

result_data.to_csv("mixture_8.csv")