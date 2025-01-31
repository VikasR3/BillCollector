# Retrieval of Documents from Web Services

import os
import sys
import re
from nslookup import Nslookup
import time
import logging
import logging.handlers
import requests
import json
from flatten_json import flatten
 
def log_setup(logfile):
    script = os.path.basename(__file__)
    log_handler = logging.handlers.WatchedFileHandler(logfile)
    formatter = logging.Formatter(
        f'%(asctime)s {script} [%(process)d]: %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.localtime  
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

def extract_ip(string):
    # Regex für IP-Adressen
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    match = ip_pattern.search(string)
    if match:
        return match.group()
    return None

def is_local_ip(ip):
    # Lokale IP-Bereiche
    local_ip_ranges = [
        re.compile(r'^10\.'),  # 10.0.0.0 - 10.255.255.255
        re.compile(r'^172\.(1[6-9]|2[0-9]|3[0-1])\.'),  # 172.16.0.0 - 172.31.255.255
        re.compile(r'^192\.168\.'),  # 192.168.0.0 - 192.168.255.255
    ]
    for pattern in local_ip_ranges:
        if pattern.match(ip):
            return True
    return False

# Check DNS for domain is directing to local IP
def is_domain_local_ip(domain):
    dns_query = Nslookup()
    try:
        ips_record = dns_query.dns_lookup(domain)
    except:
        print("DNS Exception...")
        exit(1)
    print(ips_record.answer)
    ip = extract_ip(' '.join(ips_record.answer))
    if ip:
        print(f"Gefundene IP-Adresse: {ip}")
        if is_local_ip(ip):
            print("Es handelt sich um eine lokale IP-Adresse.")
            return ip
        else:
            print("Es handelt sich nicht um eine lokale IP-Adresse.")
            return False
    else:
        print("Keine IP-Adresse erhalten.")
        return False

# Get web content
def get_json(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Überprüft, ob die Anfrage erfolgreich war (Statuscode 200)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Anfrage: {e}")
        return None

# Check Bitwarden API status
def bitwarden_api_check_status(url):
    content = get_json(f"{url}/status")
    print(content)
    if not is_json_property_value(content, "success", True): return False, None
    else: 
        if not is_json_property_value(content, "data_template_status", "unlocked"): return True, "locked"
        return True, "unlocked"
    

def is_json_property_value(content, prop, val):
    data = flatten(json.loads(content))
    result=data.get(prop)
    if (result) == val: return True
    else: return False

def post_json(url, payload):
    response = requests.post(url, json=payload)
    if response.status_code == 201 or response.status_code == 200:
        print("Erfolgreich gepostet!")
        return json.dumps(response.json())
    else:
        print(f"Fehler: {response.status_code}")
        print(response.text)
        return False

def get_json_property_value(content, prop):
    data = flatten(json.loads(content))
    result=data.get(prop)
    return result


sys.stdout = sys.__stdout__

logfile = "./WebRetriDoc.log"
vault_domain = "vault.solg.duckdns.org"
bw_api_url = "http://solg.fritz.box:8087"
credentials = {"password": "+49307874573"}

#print = logging.info   # comment out if looging into file is required instead of stdout

log_setup(logfile)

## --- Main ---

# Check if <domain> is resolvable and directs to a local IP address
ip = is_domain_local_ip(vault_domain) 
if not ip: sys.exit(1)
else: print(f"{vault_domain} is resolvable and directs to local IP {ip}")

# Check if Bitarden API at <bw_api_url> responds with success=true
ret, status = bitwarden_api_check_status(bw_api_url)
if not ret: sys.exit(1) 
else: print(status)

# Sync database
ret = post_json(f"{bw_api_url}/sync", credentials)
if not ret: sys.exit(1) 
if not is_json_property_value(ret, "success", True): sys.exit(1)
else: print("Vault is sync'd successfully.")

# Unlock database
ret = post_json(f"{bw_api_url}/unlock", credentials)
if not ret: sys.exit(1) 
if not is_json_property_value(ret, "success", True): sys.exit(1)
else: print("Vault is unlocked successfully.")

#################
# Loop over Web Services (to be done)
servicename = "KabelDeutschland"

# Retrieve credentials
ret = get_json(f"{bw_api_url}/object/item/{servicename}")
username = get_json_property_value(ret, "data_login_username")
passsword = get_json_property_value(ret, "data_login_password")
uri = get_json_property_value(ret, "data_login_uris_0_uri")

# Download Documents
from mytest import Main
Main(uri, username, passsword)
#
#################

# Lock database
ret = post_json(f"{bw_api_url}/lock", credentials)
if not ret: sys.exit(1) 
if not is_json_property_value(ret, "success", True): sys.exit(1)
else: print("Vault is locked successfully.")





