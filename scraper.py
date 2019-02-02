import bs4 as bs
import urllib.request
from selenium import webdriver

driver = webdriver.Safari()
driver.get('https://www.sj.se/sv/hem.html#/tidtabell/Uppsala%2520C/Link%25C3%25B6ping%2520C/enkel/avgang/20190209-0500/avgang/20190210-1300/SU-22--false///0//')

res = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()

soup = bs.BeautifulSoup(res,'lxml')


table = soup.find('div', {'class':'timetable__table'})
price = soup.find_all('span', {'class':'sj-price ng-scope'})
#.text.replace("\n","").strip()

for p in price:
    print(p.text.replace("\n","").strip())


#prices = soup.find_all('div', {'class':'...'})
#for price in prices:
#    print(price.text.replace("\n","").strip())



##############################




#print(table.text)
#prices=table.find_all('div', {'class':'timetable__table-rows'})

#for p in prices:
#    print(p)
#print(s.text)
#print(soup.title.string)

#print(soup.p)

#print(soup.find_all("p")) # finds all paragraph tags

#for paragraph in soup.find_all("p"):
#    print(paragraph.text)


#print(soup.get_text())

#for url in soup.find_all("a"):
#    print(url.get("href"))

#for url in soup.find_all('span'):
#    print(url)
