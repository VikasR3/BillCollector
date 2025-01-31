# Download file from web service
import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.wait import WebDriverWait

# Try to click element which needs time to be ready
def TryCssClick(Driver: webdriver, element: str, Timeout: int = 300):
    while Timeout > 0:
        try:
             Driver.find_element(By.CSS_SELECTOR, element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Element loading timeout") 

def TryIdClick(Driver: webdriver, element: str, Timeout: int = 300):
    while Timeout > 0:
        try:
             Driver.find_element(By.ID, element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Element loading timeout") 

def InitBrowser():
    # browser and webdriver configuration
    homedir = os.path.expanduser(".")
    chrome_options = Options()
    #chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
    prefs = {'download.default_directory' : '/tmp/download'}
    chrome_options.add_experimental_option('prefs', prefs)
    webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    return driver


##
# VODAFONE
##
def DownloadDoc(url, driver, user, pwd):

    driver.get(url)

    TryIdClick(driver,"dip-consent-summary-accept-all")

    TryCssClick(driver, ".fm-field-container > #txtUsername")
    driver.find_element(By.CSS_SELECTOR, ".fm-field-container > #txtUsername").send_keys(user)
    TryCssClick(driver, ".fm-field-container > #txtPassword")
    driver.find_element(By.CSS_SELECTOR, ".fm-field-container > #txtPassword").send_keys(pwd)
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, ".fm-field-container > #txtPassword").send_keys(Keys.ENTER)
    TryCssClick(driver,".btn:nth-child(1) > .title")

    time.sleep(5)
    print("job finished")
    driver.quit()


#url = "https://www.vodafone.de/meinvodafone/account/login"
#user = "StefanSchmittMalin"
#pwd = ".K77j08uni!"

def Main(url, user, pwd):
    drv = InitBrowser()
    DownloadDoc(url, drv, user, pwd)


### collection

#IMyWebElement = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'Rechnung')]")))
#MyWebElement = FindElem(driver,"//*[contains(text(),'Rechnung')]")


#driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(1) > .title").click()
#driver.find_element(By.CSS_SELECTOR, ".ws10-hybrid-table__row-desktop:nth-child(1) .ws10-hybrid-table__icon-holder:nth-child(1) > .ws10-hybrid-table__icon").click()




#driver.get("https://www.buhl.de/")
#driver.find_element(By.CSS_SELECTOR, ".default > .account-text").click()
#driver.find_element(By.ID, "eml-user-login").send_keys("s-c-h-m-i-t-t@web.de")
#driver.find_element(By.ID, "psw-user-login").send_keys(".w77j08uni!")
#driver.find_element(By.ID, "form-login-submit").click()
#driver.find_element(By.CSS_SELECTOR, ".schnellzugriffe-box:nth-child(3) span").click()
#driver.find_element(By.ID, "select-rechnung").click()
#driver.find_element(By.CSS_SELECTOR, ".documents-document-box:nth-child(1) .nodeco:nth-child(1) .documents-document-box-entry-text-title").click()
