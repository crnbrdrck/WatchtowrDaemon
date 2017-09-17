urldest = []


for i in range(1,3):
    url = "http://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page="
    url += str(i)
    url += '&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=6&cvssscoremax=0&year=2017&month=0&cweid=0&order=1&trc=4602&sha=38dbef734272cfc67f0305b1f371200bd95ad078'
    urldest.append(url)

finalList = urldest
finalList.extend(['https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-66/Apache-Http-Server.html', 'https://www.cvedetails.com/vulnerability-list/vendor_id-185/product_id-316/Mysql-Mysql.html'])
