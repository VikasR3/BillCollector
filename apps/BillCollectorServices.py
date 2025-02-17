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
def TryClick(Driver: webdriver, Locator, Element: str, Timeout: int = 60, Debug = False):
    while Timeout > 0:
        try:
             Driver.find_element(Locator, Element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Element loading timeout") 

# Try to send keys to element which needs time to be ready
def TrySendKeys(Driver: webdriver, Locator, Element: str, Key, Timeout: int = 60, Debug = False):
    while Timeout > 0:
        try:
             Driver.find_element(Locator, Element).send_keys(Key)
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            return
    raise RuntimeError(f"Sending Key to Element timeout") 

def InitBrowser(test):
    # browser and webdriver configuration
    homedir = os.path.dirname(os.path.realpath(__file__))
    chrome_options = Options()
    if test == False: chrome_options.add_argument("--headless") # Ensure GUI is off in production
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable_dev-shm-usage")
    chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
    prefs = {'download.default_directory' : f"{homedir}/Downloads", "download.prompt_for_download": False, "download.directory_upgrade": True, "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option('prefs', prefs)
    
    webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    return driver

def SaveWebPage(driver):
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("Saved HTML source for debugging.")

def RetrieveFromService(service, url, user, pwd, otp, test):
    drv = InitBrowser(test)
    drv.get(url)
    
    #if test == True: SaveWebPage(drv)

    fname = "bc_retrieve__" + service.lower().replace(" ", "_")
    try:
        retrieve = globals()[fname]
        retrieve(drv, user, pwd, otp, test)
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
def bc_retrieve__kabeldeutschland(driver, user, pwd, totp, test):
    TryClick(driver,By.ID, "dip-consent-summary-accept-all", Debug=test)
    TryClick(driver,By.CSS_SELECTOR, ".fm-field-container > #txtUsername", Debug=test)
    TrySendKeys(driver, By.CSS_SELECTOR, ".fm-field-container > #txtUsername", user, Debug=test)
    TrySendKeys(driver, By.CSS_SELECTOR, ".fm-field-container > #txtPassword", pwd, Debug=test)
    TrySendKeys(driver, By.CSS_SELECTOR, ".fm-field-container > #txtPassword", Keys.ENTER, Debug=test)
    TryClick(driver,By.CSS_SELECTOR, ".btn:nth-child(1) > .title", 300, Debug=test)
    time.sleep(5)

def bc_retrieve__buhl(driver, user, pwd, totp, test):
    shadow_host = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#usercentrics-root")))
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
    WebDriverWait(shadow_root, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#uc-center-container")))
    cookie_button = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
    driver.execute_script("arguments[0].click();", cookie_button)
    TrySendKeys(driver, By.ID, "eml-user-login", user, Debug=test)
    TrySendKeys(driver, By.ID, "psw-user-login", pwd, Debug=test)
    TryClick(driver,By.ID, "form-login-submit")
    TryClick(driver,By.ID, "select-rechnung")
    TryClick(driver,By.XPATH, '//div[@class="documents-document-box-entries"]/a[1]')
    time.sleep(5)

def bc_retrieve__datev_televic(driver, user, pwd, totp, test):
    TryClick(driver,By.CSS_SELECTOR, "[data-test-id=\"login-button\"]")
    TryClick(driver,By.CSS_SELECTOR, "[data-test-id=\"totp-login-button\"]")
    TryClick(driver,By.ID, "username")
    TrySendKeys(driver, By.ID, "username", user, Debug=test)
    TrySendKeys(driver, By.ID, "password", pwd, Debug=test)
    TryClick(driver,By.ID, "login")
    time.sleep(1)
    TrySendKeys(driver, By.ID, "enterverificationcode", totp, Debug=test)
    TrySendKeys(driver, By.ID, "enterverificationcode", Keys.ENTER, Debug=test)
    TryClick(driver,By.CSS_SELECTOR, "[data-test-id=\"load-documents-button\"]")
    TryClick(driver,By.ID, "mat-mdc-checkbox-2-input")
    TryClick(driver,By.CSS_SELECTOR, "[data-test-id=\"download-button\"]")
    time.sleep(5)

def bc_retrieve__winsim_stefan(driver, user, pwd, totp, test):
    TrySendKeys(driver, By.ID, "UserLoginType_alias", user, Debug=test)
    TrySendKeys(driver, By.ID, "UserLoginType_password", pwd, Debug=test)
    TryClick(driver, By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button", Debug=test)
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    TryClick(driver, By.ID, "consent_wall_optin", Debug=test)
    time.sleep(3)
    TryClick(driver, By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link", Debug=test)
    TryClick(driver, By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline", Debug=test)
    time.sleep(3)
    TryClick(driver, By.LINK_TEXT, "Rechnung", Debug=test)
    time.sleep(5)

def bc_retrieve__winsim_auto(driver, user, pwd, totp, test):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    TryClick(driver, By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button")
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    TryClick(driver, By.ID, "consent_wall_optin")
    time.sleep(3)
    TryClick(driver, By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link")
    TryClick(driver, By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline")
    time.sleep(3)
    TryClick(driver, By.LINK_TEXT, "Rechnung")
    time.sleep(5)

def bc_retrieve__winsim_brigitte(driver, user, pwd, totp, test):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    TryClick(driver, By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button")
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    TryClick(driver, By.ID, "consent_wall_optin")
    time.sleep(3)
    TryClick(driver, By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link")
    TryClick(driver, By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline")
    time.sleep(3)
    TryClick(driver, By.LINK_TEXT, "Rechnung")
    time.sleep(5)

def bc_retrieve__winsim_eva(driver, user, pwd, totp, test):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    TryClick(driver, By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button")
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    TryClick(driver, By.ID, "consent_wall_optin")
    time.sleep(3)
    TryClick(driver, By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link")
    TryClick(driver, By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline")
    time.sleep(3)
    TryClick(driver, By.LINK_TEXT, "Rechnung")
    time.sleep(5)

def bc_retrieve__winsim_anna(driver, user, pwd, totp, test):
    driver.find_element(By.ID, "UserLoginType_alias").send_keys(user)
    driver.find_element(By.ID, "UserLoginType_password").send_keys(pwd)
    TryClick(driver, By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button")
    #driver.find_element(By.ID, "c-overlay").click()
    #TryCssClick(driver,"[data-dismiss=\"modal\"]")
    time.sleep(3)
    TryClick(driver, By.ID, "consent_wall_optin")
    time.sleep(3)
    TryClick(driver, By.CSS_SELECTOR, ".cute-6-phone:nth-child(5) .c-link")
    TryClick(driver, By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline")
    time.sleep(3)
    TryClick(driver, By.LINK_TEXT, "Rechnung")
    time.sleep(5)
