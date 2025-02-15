# Download file from web service
import time
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait

# Try to click element which needs time to be ready
def TryCssClick(Driver: webdriver, element: str, Timeout: int = 10):
    while Timeout > 0:
        try:
             Driver.find_element(By.CSS_SELECTOR, element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Element loading timeout") 

def TryIdClick(Driver: webdriver, element: str, Timeout: int = 10):
    while Timeout > 0:
        try:
             Driver.find_element(By.ID, element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Element loading timeout") 

def TryXpathClick(Driver: webdriver, element: str, Timeout: int = 10):
    while Timeout > 0:
        try:
             Driver.find_element(By.XPATH, element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Element loading timeout") 

def TryClassClick(Driver: webdriver, element: str, Timeout: int = 10):
    while Timeout > 0:
        try:
             Driver.find_element(By.CLASS_NAME, element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Element loading timeout") 


def InitBrowser(test):
    # browser and webdriver configuration
    homedir = os.path.expanduser(".")
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable_dev-shm-usage")
    chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
    prefs = {'download.default_directory' : './download', "download.prompt_for_download": False, "download.directory_upgrade": True, "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option('prefs', prefs)
    
    webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    return driver

def SaveWebPage(driver):
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("Quelltext der Seite gespeichert.")

def RetrieveFromService(service, url, user, pwd, otp, test):
    drv = InitBrowser(test)
    drv.get(url)
    
    #if test == True: SaveWebPage(drv)

    fname = "wrd_retrieve__" + service.lower().replace(" ", "_")
    try:
        retrieve = globals()[fname]
        retrieve(drv, user, pwd, otp)
        print(f"Service {service} finished.")
        ret = True
    except:
        print(f"Service {service} not successfully finished.")
        ret = False
    else:
        drv.quit()
        return ret    
    
    

#
# Services
#
def wrd_retrieve__kabeldeutschland(driver, user, pwd, totp):
    TryIdClick(driver,"dip-consent-summary-accept-all")
    TryCssClick(driver, ".fm-field-container > #txtUsername")
    driver.find_element(By.CSS_SELECTOR, ".fm-field-container > #txtUsername").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, ".fm-field-container > #txtPassword").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, ".fm-field-container > #txtPassword").send_keys(Keys.ENTER)
    TryCssClick(driver,".btn:nth-child(1) > .title")
    time.sleep(5)

def wrd_retrieve__buhl(driver, user, pwd, totp):
    shadow_host = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#usercentrics-root")))
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
    WebDriverWait(shadow_root, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#uc-center-container")))
    cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
    driver.execute_script("arguments[0].click();", cookie_button)
    driver.find_element(By.ID, "eml-user-login").send_keys(user)
    driver.find_element(By.ID, "psw-user-login").send_keys(pwd)
    TryIdClick(driver,"form-login-submit")
    TryIdClick(driver,"select-rechnung")
    TryXpathClick(driver,'//div[@class="documents-document-box-entries"]/a[1]')
    time.sleep(5)

def wrd_retrieve__datev_televic(driver, user, pwd, totp):
    TryCssClick(driver,"[data-test-id=\"login-button\"]")
    TryCssClick(driver,"[data-test-id=\"totp-login-button\"]")
    TryIdClick(driver,"username")
    driver.find_element(By.ID, "username").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(pwd)
    TryIdClick(driver,"login")
    time.sleep(1)
    driver.find_element(By.ID, "enterverificationcode").send_keys(totp)
    driver.find_element(By.ID, "enterverificationcode").send_keys(Keys.ENTER)
    TryCssClick(driver,"[data-test-id=\"load-documents-button\"]")
    TryIdClick(driver,"mat-mdc-checkbox-2-input")
    TryCssClick(driver,"[data-test-id=\"download-button\"]")
    time.sleep(5)

def wrd_retrieve__winsim_stefan(driver, user, pwd, totp):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button").click()
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    driver.find_element(By.ID, "consent_wall_optin").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link").click()
    driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Rechnung").click()
    time.sleep(5)

def wrd_retrieve__winsim_auto(driver, user, pwd, totp):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button").click()
    tmp = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "c-overlay")))
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    driver.find_element(By.ID, "consent_wall_optin").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link").click()
    driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Rechnung").click()
    time.sleep(5)

def wrd_retrieve__winsim_brigitte(driver, user, pwd, totp):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button").click()
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    driver.find_element(By.ID, "consent_wall_optin").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link").click()
    driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Rechnung").click()
    time.sleep(5)

def wrd_retrieve__winsim_eva(driver, user, pwd, totp):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button").click()
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    driver.find_element(By.ID, "consent_wall_optin").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link").click()
    driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Rechnung").click()
    time.sleep(5)

def wrd_retrieve__winsim_anna(driver, user, pwd, totp):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    driver.find_element(By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button").click()
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    driver.find_element(By.ID, "consent_wall_optin").click()
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link").click()
    driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline").click()
    time.sleep(3)
    driver.find_element(By.LINK_TEXT, "Rechnung").click()
    time.sleep(5)
