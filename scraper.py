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
    ncols = 4
    for t in time_schedule:
        nrows+=1

    table_information = np.empty((nrows, ncols), dtype=object)

    for t in range(len(time_schedule)):
        hours = time_schedule[t].text.replace("\n","").strip()
        hours = hours.replace(":", "")

        table_information[t][0] = hours[:4]
        table_information[t][1] = hours[7:]

    print(table_information)

    #driver.quit()
