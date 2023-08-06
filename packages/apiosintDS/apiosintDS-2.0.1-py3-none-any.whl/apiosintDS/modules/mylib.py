import sys
import os
import requests
import validators
import json
from datetime import datetime
import re
from stix2 import parse
import pytz

italyTZ = pytz.timezone("Europe/Rome")

class stixreport():
    def __init__(self, item, cache, cachedir, clearcache, logger):
        self.logger = logger
        self.item = item
        self.report = item+".json"
        self.urls = {"master_url": "https://raw.githubusercontent.com/davidonzo/Threat-Intel/master/stix2/",
                     "slave_url": "https://osint.digitalside.it/Threat-Intel/stix2/"}
        self.cache = cache
        if isinstance(cachedir, str):
            self.cachedir = cachedir+"/"
        else:
            self.cachedir = False
        self.clearcache = clearcache

        ### !!! ### o_O
        self.template = {"url": [], "ip": [], "domain": [], "hash": []}
        self.checkdate = italyTZ.localize(datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))
        self.getStix = parse(self.getCache())


    def getListDate(self, reportContent):
        ret = False
        for obj in reportContent["objects"]:
            if obj["type"] == "report":
                ret = obj["published"]
        
        return italyTZ.localize(datetime.strptime(ret, '%Y-%m-%d %H:%M:%S'))
    
    """
    def getListItems(self, context, hashes=False):
        if hashes:
            context = json.loads(context)
            listitems = context["lookup"]
        else:
            listitems = context[11:]
        return listitems
    """
    
    def getCache(self):
        cached = {}
        if self.cache:
            cachedfile = self.cachedir+cached[entity]["file"]
            if os.path.exists(cachedfile):
                if self.clearcache:
                    dwreport = self.downloadReport()
                else:
                    cacheHandler = open(cachedfile, 'r')
                    content = cacheHandler.read()
                    cacheHandler.close()
                    dwreport = json.dumps(content)
                
                reportDate = self.getListDate(dwlist, dwreport)
                diffdate = ((self.checkdate-listdate).total_seconds())/3600
                
                if diffdate < 4:
                    logger.info("Report "+self.report+" loaded from cache")
                else:
                    dwreport = self.downloadReport()
            else:
                dwreport = self.downloadReport()
            
            return dwreport

    def saveCache(self, entity, content):
        try:
            cachefile = open(self.cachedir+self.report, "w")
            cachefile.write(content)
            cachefile.close()
        except IOError as e:
            self.logger.error(e)
            self.logger.error("Unable save list! Make sure you have write permission on file "+self.cachedir+self.report)
            self.logger.error("Retry without -c, --cache option.")
            exit(1)

    def downloadReport(self):
        ret = False
        
        reportURL = self.urls['master_url']+self.report
        r = requests.get(reportURL)
        if r.status_code != 200:
            reportURL = self.urls['slave_url']+self.report
            self.logger.warning("Error downloading {} from GitHub repository.".format(self.report))
            self.logger.warning("Returned HTTP status code is {}:".format(r.status_code))
            self.logger.warning("Try downloading file from osint.digitalside.it")
            r = requests.get(ret["url"])
            if r.status_code != 200:
                self.logger.warning("Error downloading {} both from GitHub repository and OSINT.digitalside.it".format(self.report))
                self.logger.warning("Returned HTTP status code is {}:".format(r.status_code))
                self.logger.error(self.status_error(self.report))
                return ret
            return ret
        
        stixreport = r.json
        
        if len(text) == 0:
            self.logger.error("The downloaded list seems to be empty!\n")
            self.logger.error(self.status_error(self.report))
            return ret
        
        if self.cache:
            self.saveCache(self, text)
        return stixreport

    def status_error(self):
        error="Check the following urls using your prefered browser:\n"
        error+="- https://raw.githubusercontent.com/davidonzo/Threat-Intel/master/stix2/"+self.report+"\n"
        error+="- https://osint.digitalside.it/Threat-Intel/stix2/"+self.report+"\n"
        error+="\n"
        error+="Are you able to view the desired IoC list? If not, please, report this opening an issue on Threat-Intel GitHub repository:\n"
        error+="- https://github.com/davidonzo/Threat-Intel/issues\n"
        error+="\n"
        error+="Aren't you familiar with GitHub? No worries. You can send a PGP signed and encrypted email to info@digitalside.it\n"
        error+="PGP key ID: 30B31BDA\n"
        error+="PGP fingerprint: 0B4C F801 E8FF E9A3 A602  D2C7 9C36 93B2 30B3 1BDA\n"
        error+="\n"
        error+="Aren't you familiar with PGP? Be worried... maybe you should not use this script ;-)\n"
        return error
