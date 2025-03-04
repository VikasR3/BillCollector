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
def TryClick(bcs, Locator, Element: str, Timeout: int = 60, Grace = False):
    while Timeout > 0:
        try:
             bcs.drv.find_element(Locator, Element).click()
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            if bcs.dbg == True: SaveWebPage(bcs.drv)
            return True
    if bcs.dbg == True: SaveWebPage(bcs.drv)
    if Grace == False: raise RuntimeError(f"Element loading timeout") 
    else: return False

# Try to click shadow element which needs time to be ready
def TryClickShadow(bcs, Locator, ElementA: str, ElementB: str, ElementC: str, Timeout: int = 5):
    try:
        shadow_host = WebDriverWait(bcs.drv, Timeout).until(EC.presence_of_element_located((Locator, ElementA)))
        shadow_root = bcs.drv.execute_script('return arguments[0].shadowRoot', shadow_host)
        WebDriverWait(shadow_root, Timeout).until(EC.presence_of_element_located((Locator, ElementB)))
        cookie_button = shadow_root.find_element(Locator, ElementC)
        bcs.drv.execute_script("arguments[0].click();", cookie_button)
    except: 
        if bcs.dbg == True: SaveWebPage(bcs.drv)
        raise RuntimeError(f"Shadow Element loading failed")
    else:
        if bcs.dbg == True: SaveWebPage(bcs.drv)
        return True

# Try to send keys to element which needs time to be ready
def TrySendKeys(bcs, Locator, Element: str, Key, Timeout: int = 60, Grace = False):
    while Timeout > 0:
        try:
             bcs.drv.find_element(Locator, Element).send_keys(Key)
        except: 
            time.sleep(1)
            Timeout -= 1
        else:
            if bcs.dbg == True: SaveWebPage(bcs.drv)
            return True
    if bcs.dbg == True: SaveWebPage(bcs.drv)
    if Grace == False: raise RuntimeError(f"Sending Key to Element timeout")
    else: return False

# Try to download file from element which needs time to be ready
# Checks download folder for new downloaded file and returns the name of the downloaded file
def TryDownload(bcs, Locator, Element: str, Timeout: int = 60):
    prev_file = latest_download_file(bcs.dld)
    TryClick(bcs,Locator, Element, Timeout)
    time.sleep(5)
    return is_download_finished(bcs.dld, prev_file)
    
def latest_download_file(download_dir):
      os.chdir(download_dir)
      files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
      if len(files) > 0: latest_f = files[-1]
      else: latest_f = None
      return latest_f

def is_download_finished(download_dir, previous_file):
    current_file = latest_download_file(download_dir)
    if current_file != previous_file:
        return current_file
    else:
        return None

# Initialize browser and return driver object
# parameterize browser: in debug mode = headless, default download folder, force download by always open pdf externally, ...
def InitBrowser(bcs):
    # browser and webdriver configuration
    homedir = os.path.dirname(os.path.realpath(__file__))
    chrome_options = Options()
    if bcs.dbg == False: chrome_options.add_argument("--headless") # Ensure GUI is off in production
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable_dev-shm-usage")
    chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
    prefs = {'download.default_directory' : bcs.dld, "download.prompt_for_download": False, "download.directory_upgrade": True, "plugins.always_open_pdf_externally": True}
    chrome_options.add_experimental_option('prefs', prefs)
    
    webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    return driver

# Save web page source for debugging
def SaveWebPage(driver):
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("Saved HTML source for debugging.")

# Service variables
class service_vars:
    def __init__(self, usr, pwd, otp, dbg, dld, drv=None):
        self.drv = drv
        self.usr = usr
        self.pwd = pwd
        self.otp = otp
        self.dbg = dbg
        self.dld = dld

# Retrieve file from service
def RetrieveFromService(service, url, user, pwd, otp, test):
    
    bcs = service_vars(user, pwd, otp, test, f"{os.path.dirname(os.path.realpath(__file__))}/Downloads")
    if not os.path.exists(bcs.dld):
        os.makedirs(bcs.dld)
    bcs.drv = InitBrowser(bcs)
    bcs.drv.get(url)
    if bcs.dbg == True: SaveWebPage(bcs.drv)

    fname = "bc_retrieve__" + service.lower().replace(" ", "_")
    try:
        retrieve = globals()[fname]
        file_downloaded = retrieve(bcs)
        if file_downloaded != None: print(f"Service {service} finished with file {file_downloaded} for {bcs.usr} downloaded.")
        else: print(f"Service {service} for {bcs.usr} finished without a file downloaded.")
        ret = True
    except:
        print(f"Service {service} for {bcs.usr} not successfully finished.")
        ret = False
    else:
        bcs.drv.quit()
        return ret    

#
# Services
#
def bc_retrieve__nuernberger(bcs):
    TryClick(bcs, By.ID, "consent_prompt_submit", 5, True)
    TrySendKeys(bcs,By.ID, "form_initialLogin_step2:j_idt156:username",bcs.usr)
    TrySendKeys(bcs,By.ID, "form_initialLogin_step2:j_idt171:pwd",bcs.pwd)
    TryClick(bcs,By.ID, "form_initialLogin_step2:loginSubmit")
    TryClick(bcs,By.CSS_SELECTOR, ".hidden-xs > .fake-btn")
    TryClick(bcs,By.XPATH, "(//tr[@data-cy='brief'])[2]")
    fname = TryDownload(bcs, By.XPATH, "(//div[@data-cy='download'])[2]")
    TryClick(bcs,By.XPATH, "(//tr[@data-cy='brief'])[1]")
    fname = TryDownload(bcs, By.XPATH, "(//div[@data-cy='download'])[1]")
    return fname

def bc_retrieve__lichtblick(bcs):
    TryClickShadow(bcs, By.CSS_SELECTOR, "#usercentrics-cmp-ui", "#uc-main-dialog", "#accept")
    TryClick(bcs,By.XPATH, "//a[@href='/konto/']")
    TrySendKeys(bcs,By.ID, "email", bcs.usr)
    TrySendKeys(bcs,By.ID, "password", bcs.pwd)
    TryClick(bcs,By.ID, "next")
    TryClick(bcs,By.LINK_TEXT, "Posteingang")
    fname = TryDownload(bcs,By.XPATH, "//button[span[text()='Download']]")
    return fname

def bc_retrieve__kabeldeutschland(bcs):
    TryClick(bcs,By.ID, "dip-consent-summary-accept-all")
    TryClick(bcs,By.CSS_SELECTOR, ".fm-field-container > #txtUsername")
    TrySendKeys(bcs, By.CSS_SELECTOR, ".fm-field-container > #txtUsername", bcs.usr)
    TrySendKeys(bcs, By.CSS_SELECTOR, ".fm-field-container > #txtPassword", bcs.pwd)
    TrySendKeys(bcs, By.CSS_SELECTOR, ".fm-field-container > #txtPassword", Keys.ENTER)
    fname = TryDownload(bcs,By.CSS_SELECTOR, ".btn:nth-child(1) > .title", 300)
    return fname

def bc_retrieve__buhl(bcs):
    TryClickShadow(bcs, By.CSS_SELECTOR, "#usercentrics-root", "#uc-center-container", "button[data-testid='uc-accept-all-button']")
    TrySendKeys(bcs, By.ID, "eml-user-login", bcs.usr)
    TrySendKeys(bcs, By.ID, "psw-user-login", bcs.pwd)
    TryClick(bcs,By.ID, "form-login-submit")
    TryClick(bcs,By.ID, "select-rechnung")
    fname = TryDownload(bcs,By.XPATH, '//div[@class="documents-document-box-entries"]/a[1]')
    return fname

def bc_retrieve__datev_televic(bcs):
    TryClick(bcs,By.CSS_SELECTOR, "[data-test-id=\"login-button\"]")
    TryClick(bcs,By.CSS_SELECTOR, "[data-test-id=\"totp-login-button\"]")
    TryClick(bcs,By.ID, "username")
    TrySendKeys(bcs, By.ID, "username", bcs.usr)
    TrySendKeys(bcs, By.ID, "password", bcs.pwd)
    TryClick(bcs,By.ID, "login")
    time.sleep(1)
    TrySendKeys(bcs, By.ID, "enterverificationcode", bcs.otp)
    TrySendKeys(bcs, By.ID, "enterverificationcode", Keys.ENTER)
    TryClick(bcs,By.CSS_SELECTOR, "[data-test-id=\"load-documents-button\"]")
    TryClick(bcs,By.ID, "mat-mdc-checkbox-2-input")
    fname=TryDownload(bcs,By.CSS_SELECTOR, "[data-test-id=\"download-button\"]")
    return fname

def bc_retrieve__winsim(bcs):
    TrySendKeys(bcs, By.ID, "UserLoginType_alias", bcs.usr)
    TrySendKeys(bcs, By.ID, "UserLoginType_password", bcs.pwd)
    TryClick(bcs, By.CSS_SELECTOR, ".p-site-login-form-wrapper .c-button")
    TryClick(bcs, By.ID, "c-overlay", 5, True)
    TryClick(bcs, By.CSS_SELECTOR,"[data-dismiss=\"modal\"]", 5, True)
    TryClick(bcs, By.ID, "consent_wall_optin")
    TryClick(bcs, By.XPATH, "(//a[contains(@href, '/mytariff/invoice/showAll')])[2]")
    TryClick(bcs, By.CSS_SELECTOR, "div:nth-child(1) > .c-panel-v1 > .c-panel-v1-headline")
    fname=TryDownload(bcs, By.LINK_TEXT, "Rechnung")
    return fname
