# BillCollector

Let BillCollector collect your bills from different personalized web portals.

Invoices and documents that are regularly stored by service providers in the respective online account are automatically retrieved by BillCollector and stored locally in a download folder. The workflow really makes sense when the files are consumed in the download folder of Paperless ngx or a similar document management system (DMS).

BillCollector uses

- Vaultwarden as a vault for the access data for the online accounts
- Selenium (for Python) to automate the browser control
- Chrome for testing and Chromedriver as the browser front end of the service provider's online portal

Chrome is operated headless, so that BillCollector can do its job on a Raspberry PI or a NAS headless integrated into the cron-scheduler on a regular basis, e.g. retrieving the newest document twice a month.

Following diagram summarizes the complete BillCollector Ecosystem

![BillCollector Ecosystem](/doc/BillCollector.svg)

## Overview of the Prerequisites

Following services are needed to be in place for BillCollector:

- Docker environment
- Vaultwarden (docker image: vaultwarden/server:latest)
- ... with Bitwarden API (<https://bitwarden.com/help/vault-management-api/>) in one docker stack
- Secure https access is mandatory for account management and usage of Vaultwarden. Therefore, addtionally needed:
  - nginxproxymanager with Let's Encrypt (docker image: jc21 nginx-proxy-manager:latest)
  - Duckdns account & config -> redirect to local IP address

## Installation

### Docker Environment

It is assumed that you have a docker environment up and running. There are different options you can choose from: Docker Desktop on a Linux or Windows machine or for your Mac, docker on the command line of your NAS or your Raspberry Pi. Plenty ressources on the internet will support you getting that done. A natural good starting point is the [Docker Getting Started](https://docs.docker.com/get-started/).

I have it running on on my self-built Mini-ITX Intel Pentium J5040 NAS hardware equipped with the Debian Linux based NAS operating system  [openmediavault](https://www.openmediavault.org/) (OMV) and the [omv-extras](https://wiki.omv-extras.org/doku.php?id=omv7:docker_in_omv) installed.

### Vault of Secrets

BillCollector uses the selfhosted [Vaultwarden](https://github.com/dani-garcia/vaultwarden) password manager.

Why Vaultwarden? The simple reason is that it is a resource-light-weight alternative to Bitwarden and compatible with the Bitwarden Vault Mangement API integrated in the [Bitwarden CLI](https://github.com/tangowithfoxtrot/bw-docker) allowing to retrieve secret login data programmatically.

On [Vaultwarden Docker](http://solg.fritz.box:3030/stefan/Vaultwarden.git) you'll get the Vaultwarden and the Bitwarden CLI as a `Dockerfile` and a `docker-compose.yml`. Follow the installation guide over there.

### Enabling DNS and HTTPS with Let's Encrypt certs

Vaultwarden only allows secure HTTPS access by default. Suppose you want to run an instance of Vaultwarden that can only be accessed from your local network by name instead of IP adress and you want your instance to be HTTPS-enabled with certs signed by a widely accepted Certificate Authority (CA) instead of managing your own private CA.

Currently the simplest option is offered by [Duck DNS](https://www.duckdns.org) as a free Domain Name Service (DNS) in combination with the locally dockerized [Nginx Proxy Manager](https://nginxproxymanager.com/) (NPM) enabling address forwarding to your Vaultwarden instance including free SSL using the [Let's Encrypt](https://letsencrypt.org/) CA.

The cool things about DuckDNS is not only that it is free of charge, but that it also allows wildcard domains and local IP address names. For the latter, however, DNS rebind protection must also be set up in your router.

The only downside of Duck DNS is, that you cannot freely choose your domainname because it will follow the name scheme [https://\<your subdomain\>.duckdns.org](duckdns.org).

Steps to follow:

1. If you don't already have an account, create one at <https://www.duckdns.org/>. Define a subdomain name either used as a wildcard domain or just a single domain name for your Vaultwarden instance (e.g., my-vw.duckdns.org) and set its IP to your vaultwarden host's private IP (e.g., 192.168.1.100). Make note of your account's token (a string in UUID format). NPM will need this token to solve the DNS challenge.

    ![MyDuckDNS](/doc/Screenshot%202025-02-27%20234458.jpg)

2. Configure the DNS Rebind Protection in your router: For a Fritz!Box routers go to `/Heimnetz/Netzwerk/Netzwerkeinstellungen/DNS-Rebind-Schutz` and enter the hostname you configured in Duck DNS [\<your subdomain\>.duckdns.org](duckdns.org).

3. Check the setup of your domainname was successful.
On your Windows machine `<WIN>R cmd` and enter `nslookup <your subdomain\>.duckdns.org`. The response should look similar as follows:

    ![nslookup](/doc/Screenshot%202025-02-28%20002726.jpg)

    Alternatively on your Linux machine use a tool like `dig` to check Duck DNS is resolving your domainname.

4. Now we are ready to install and configure the Nginx Proxy Manager.....
