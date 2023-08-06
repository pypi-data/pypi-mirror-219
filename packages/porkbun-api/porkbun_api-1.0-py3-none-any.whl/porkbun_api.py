import requests as req

APIKEY = ""
SECRETAPIKEY = ""

PINGURI = "https://porkbun.com/api/json/v3/ping"
V4ONLYPINGURI = "https://api-ipv4.porkbun.com/api/json/v3/ping"

NSUPDATEURI = "https://porkbun.com/api/json/v3/domain/updateNS/{domain}"

CREATEURI = "https://porkbun.com/api/json/v3/dns/create/{domain}"

READURI = "https://porkbun.com/api/json/v3/dns/retrieveByNameType/{domain}/{type}/{subdomain}"

UPDATEURI = "https://porkbun.com/api/json/v3/dns/editByNameType/{domain}/{type}/{subdomain}"

DELETEURI = "https://porkbun.com/api/json/v3/dns/deleteByNameType/{domain}/{type}/{subdomain}"

ALLOWEDTYPES = ["A", "MX", "CNAME", "ALIAS", "TXT", "NS", "AAAA", "SRV", "TLSA", "CAA"]

## internal functions
def checkError(request):
    if request.json()["status"] == "ERROR":
        message = request.json()["message"]
        return message

class PorkbunError(Exception):
    ...

def defaultKeysIfNone(api, secret):
    keylist = (api, secret)
    if not any(keylist):
        return (APIKEY, SECRETAPIKEY)
    elif all(keylist):
        return keylist
    return ("", "")
##

def ping(apikey:str = "", secretapikey:str = "", ipv4only:bool = True):
    apikey, secretapikey = defaultKeysIfNone(apikey, secretapikey)
    pingrequest = req.post(V4ONLYPINGURI if ipv4only else PINGURI, json = {"secretapikey" : secretapikey, "apikey" : apikey})
    pingrequest.raise_for_status()
    if msg := checkError(pingrequest):
        raise PorkbunError(msg)
    return pingrequest.json()["yourIp"]

def nsupdate(domain:str, nslist:list, apikey:str = "", secretapikey:str = ""):
    apikey, secretapikey = defaultKeysIfNone(apikey, secretapikey)
    nsurequest = req.post(NSUPDATEURI.format(domain = domain), json = {"secretapikey" : secretapikey, "apikey" : apikey, "ns": nslist})
    nsurequest.raise_for_status()
    if msg := checkError(nsurequest):
        raise PorkbunError(msg)

def create(domain:str, rtype:str, content:str, apikey:str = "", secretapikey:str = "", subdomain:str = "",  ttl:int = 600):
    if rtype not in ALLOWEDTYPES:
        return
    apikey, secretapikey = defaultKeysIfNone(apikey, secretapikey)
    crequest = req.post(CREATEURI.format(domain = domain), json = {"secretapikey" : secretapikey, "apikey" : apikey, "type" : rtype, "name" : subdomain, "ttl" : ttl, "content" : content})
    crequest.raise_for_status()
    if msg := checkError(crequest):
        raise PorkbunError(msg)

def read(domain:str, rtype:str, subdomain:str = "", apikey:str = "", secretapikey:str = ""):
    apikey, secretapikey = defaultKeysIfNone(apikey, secretapikey)
    rrequest = req.post(READURI.format(domain = domain, type = rtype, subdomain = subdomain), json = {"secretapikey" : secretapikey, "apikey" : apikey})
    rrequest.raise_for_status()
    if msg := checkError(rrequest):
        raise PorkbunError(msg)
    return rrequest.json()["records"]

def update(domain:str, rtype:str, content:str, subdomain:str = "", apikey:str = "", secretapikey:str = "", ttl:int = 600):
    apikey, secretapikey = defaultKeysIfNone(apikey, secretapikey)
    urequest = req.post(UPDATEURI.format(domain = domain, type = rtype, subdomain = subdomain), json = {"secretapikey" : secretapikey, "apikey" : apikey, "content" : content, "ttl" : ttl})
    urequest.raise_for_status()
    if msg := checkError(urequest):
        raise PorkbunError(msg)

def delete(domain:str, rtype:str, subdomain:str = "", apikey:str = "", secretapikey:str = ""):
    apikey, secretapikey = defaultKeysIfNone(apikey, secretapikey)
    drequest = req.post(DELETEURI.format(domain = domain, type = rtype, subdomain = subdomain), json = {"secretapikey" : secretapikey, "apikey" : apikey})
    drequest.raise_for_status()
    if msg := checkError(drequest):
        raise PorkbunError(msg)

def ddns_update(domain:str, ip:str = "", subdomain:str = "", apikey:str = "", secretapikey:str = "", ipv4only:bool = True):
    apikey, secretapikey = defaultKeysIfNone(apikey, secretapikey)
    if ip:
        ipaddr = ip
    else:
        ipaddr = ping(apikey = apikey, secretapikey = secretapikey, ipv4only = False if not ipv4only else True)
    update(domain, "A" if ipv4only or ":" not in ip else "AAAA", subdomain, ipaddr, apikey = apikey, secretapikey = secretapikey)
