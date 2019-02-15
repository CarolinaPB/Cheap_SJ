import bs4 as bs
import urllib.request
from selenium import webdriver
import time
import numpy as np

def scraper(driver):
    time.sleep(5)

    html = driver.page_source
    soup = bs.BeautifulSoup(html, "lxml")


    time_schedule = soup.find_all("div", {'class':'timetable__time-info timetable__time-info--small guttered--quarter-vertically ng-binding'})
    nrows =0
    ncols = 5
    for t in time_schedule:
        nrows+=1

    table_information = np.empty((nrows, ncols), dtype=object)

    prices = soup.find_all('div', {'class':'timetable-cell timetable-cell__right-cell timetable-cell__unexpanded timetable-cell__unexpanded-class timetable-cell__class ng-isolate-scope'})
    operator = soup.find_all('div', {'class':'timetable__extra-info-icon'})

    travel_time = soup.find_all("span",{'class':'ng-isolate-scope ng-binding'})

    travel_t=[]
    for t in range(0,len(travel_time),2):
        travel_t.append(travel_time[t].text)
        #print(travel_t[t])
    h1=[]
    h2=[]
    for t in range(len(time_schedule)):
        hours = time_schedule[t].text.replace("\n","").strip()
        hours = hours.replace(":", "")
        h1.append(hours[:4])
        #h2.append(hours[7:])

    t=1
    while h1[t-1]<=h1[t]:
        print(h1[t-1]+"=<"+h1[t])
        t+=1
    for t in range(len(time_schedule)):
        hours = time_schedule[t].text.replace("\n","").strip()
        hours = hours.replace(":", "")

        table_information[t][0] = hours[:4]
        table_information[t][1] = hours[7:]

        price = prices[t].text.replace("\n","").strip()
        price = price.replace("fr.","")
        price = price.split(":")[0]
        price = price.replace(" ","")
        try:
            int(price)
        except:
            price=None

        table_information[t][4] = price

        op = operator[t].text.replace("\n","").strip()
        if "+0" in op:
            op = op.replace("+0","")
        table_information[t][3] = op

        table_information[t][2] = travel_t[t].replace(" h", "")

    print(table_information)
    print()
    #remove rows with None
    #mask = np.any(np.equal(table_information, None), axis=1)
    #print(table_information[~mask])
    #print()
    #driver.quit()

#sorted([list]) sorts even with separator like ":"


#guttered--double-bottom guttered--mobile-bottom ng-isolate-scope
