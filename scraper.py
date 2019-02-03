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
time = soup.find_all("div", {'class':'timetable__time-info timetable__time-info--small guttered--quarter-vertically ng-binding'})
#.text.replace("\n","").strip()

time_list = []
for t in time:
    time_list.append(t.text.replace("\n","").strip())
print (time_list)

price_list = []
for p in price:
    price_list.append(p.text.replace("\n","").strip())

print(price_list)
length = (len(price_list)-1)/2
print(length)

#for p in price:
#    for t in time:
#        print(t.text.replace("\n","").strip())
#        print(p.text.replace("\n","").strip())



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
