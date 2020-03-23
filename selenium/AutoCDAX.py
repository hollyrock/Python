# CDAX Site automation via Chrome
# Site: https://hpcdax.crm.dynamics.com/main.aspx
# Python Select Interpretor - You need to select 32bit Python interpretor dur to Slenium driver.exe is compiled in 32 bit.

from selenium import webdriver
import time

# Some definition 
cdaxfile = "./cdaxcase.txt"
logfile = "./auto.log"
case_list = []

driver = webdriver.Chrome("./chromedriver")
driver.get("https://hpcdax.crm.dynamics.com/main.aspx")

# Wait for 15S until loading completed
time.sleep(60)

# load case# from txt file
with open(cdaxfile, "rt") as textfile:
    for case_number in textfile:
        case_list.append(case_number)
print(case_list)

# Switch iFrame
driver.switch_to.frame("contentIFrame0")

# Fill case id into Transaction ID form
userID = driver.find_element_by_xpath("//*[@id='caseIdtxtid']")
userID.send_keys('5029549558')

# Click Search button
driver.find_element_by_xpath('//*[@id="searchButtonId"]').click()
