import scrapy
from urls import *
import os
import re
import json
import sys
#
# sys.path.insert(0, '')
# #from db import *

appHashTable = {}

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    count = 0
    def start_requests(self):
        urls = finalList
        toBePath = os.getcwd() + "/go.txt"
        if os.path.isfile('go.txt'):
            with open('newpages.txt',"r") as lines:
                for line in lines:
                    url = "http://www.cvedetails.com/cve/" + line
                    yield scrapy.Request(url=url.strip(), callback=self.parse)
        else:
            for url in urls:
                yield scrapy.Request(url=url, callback=self.getNewPages)

    def getNewPages(self,response):
        self.count += 1
        rows = response.css("tr.srrowns")
        with open('newpages.txt', 'a') as fname:
            for i in rows:
                columns = i.css("td")
                newPageObject = columns[1]
                newPageID = str(newPageObject.css("a::text").extract_first())
                newPageID += '\n'
                fname.write(newPageID)
        if(self.count==2):
            with open('go.txt','a') as f:
                f.write("\n")

    def parse(self,response):
        table = response.css("table#vulnprodstable")
        versionTable = response.css("table#cvssscorestable")
        threatLevel = str(versionTable.css("tr")[0].css("td").css("div.cvssbox::text").extract_first())
        rows = table[0].css("tr")
        for i in range(1,len(rows)-1):
            product = str(rows[i].css("td")[3].css("a::text").extract_first())
            if(product=="Http Server"):
                product = "Apache"
            product = re.sub('[<td>.!\t@#$\n/]', '', product)
            version = str(rows[i].css("td")[4].extract())
            version = re.sub('[<td>!\t@#$\n/]', '', version)
            appHashTable.setdefault(product,[])
            appHashTable[product].append({'version': version, 'threat': threatLevel})
            print("%s: %s, %s", product, version, threatLevel)
        json_data = json.dumps(appHashTable)
        with open("database.json",'w') as data:
            data.write(json_data)
