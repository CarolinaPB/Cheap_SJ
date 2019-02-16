import bs4 as bs
import urllib.request
from selenium import webdriver
import time
import numpy as np


def create_table(soup,table_class, trip):
    '''
    Creates a table with hour of departure, of arrival to destination, travel time, if only SJ or if there are other companies involved and price
    If any of the rows has a null value, that row is removed from the table
    '''
    page_table = soup.find("div", {"class":table_class})
    travel_hours = page_table.find_all("div", "timetable__time-info timetable__time-info--small guttered--quarter-vertically ng-binding")
    prices = page_table.find_all('div', {'class':'timetable-cell timetable-cell__right-cell timetable-cell__unexpanded timetable-cell__unexpanded-class timetable-cell__class ng-isolate-scope'})
    travel_time = page_table.find_all("span",{'class':'ng-isolate-scope ng-binding'})
    travel_t=[]
    for t in range(0,len(travel_time),2):
        travel_t.append(travel_time[t].text)

    operator = page_table.find_all('div', {'class':'timetable__extra-info-icon'})

    nrows = len(travel_hours)
    ncols = 5
    arr = np.empty((nrows, ncols), dtype=object)

    for i in range(nrows):
        hours = travel_hours[i].text.replace("\n","").strip()
        hours = hours.replace(":","")

        if trip == "departure":
            h1 = hours[:5]
            h2 = hours[8:]
            if int(h1) <= 1300 and int(h1)>=700:
                arr[i][0] = h1
                arr[i][1] = h2

        elif trip == "arrival":
            h1 = hours[:5]
            h2 = hours[8:]
            if int(h1) >= 1700:
                arr[i][0] = h1
                arr[i][1] = h2


        arr[i][2] = travel_t[i].replace(" h", "")

        op = operator[i].text.replace("\n","").strip()
        if "+0" in op:
            op = op.replace("+0","")
        arr[i][3] = op

        price = prices[i].text.replace("\n","").strip()
        price = price.replace("fr.","")
        price = price.split(":")[0]
        price = price.replace(" ","")
        try:
            int(price)
        except:
            price=None

        arr[i][4] = price

    #remove rows with None
    mask = np.any(np.equal(arr, None), axis=1)
    arr = (arr[~mask])
    return(arr)

def scraper(driver):
    time.sleep(5)

    html = driver.page_source
    soup = bs.BeautifulSoup(html, "lxml")

    departure_table = create_table(soup, "guttered--double-bottom guttered--mobile-bottom ng-isolate-scope", "departure")
    print(departure_table)
    print()
    arrival_table = (create_table(soup,"timetable-inbound guttered--double-bottom guttered--mobile-bottom ng-scope ng-isolate-scope", "arrival"))
    print(arrival_table)

    driver.quit()

#sorted([list]) sorts even with separator like ":"
