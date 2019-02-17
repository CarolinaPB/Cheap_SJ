import bs4 as bs
import urllib.request
from selenium import webdriver
import time
import numpy as np
import re


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
            h1 = hours[:4]
            h2 = hours[7:]
            if int(h1) <= 1300 and int(h1)>=700:
                arr[i][0] = h1
                arr[i][1] = h2

        elif trip == "arrival":
            h1 = hours[:4]
            h2 = hours[7:]
            if int(h2) >= 1700:
                arr[i][0] = h1
                arr[i][1] = h2


        arr[i][2] = travel_t[i].replace(" h", "").replace(":","")

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
            price=int(price)
        except:
            price=None

        arr[i][4] = price


    #remove rows with None
    mask = np.any(np.equal(arr, None), axis=1)
    arr = (arr[~mask])

    return(arr)

def find_top_cheapest(departure_table, arrival_table, destination):
    nrows=len(departure_table)*len(arrival_table)
    arr = np.empty((nrows, 4), dtype=object)

    n=0
    for dept_el in departure_table:
        for arrv_el in arrival_table:
            arr[n][0] = destination
            arr[n][1] = dept_el
            arr[n][2] = arrv_el
            arr[n][3] = dept_el[4]+arrv_el[4] #total price
            n+=1

    ind = np.argsort(arr[:,-1])
    arr_sorted_by_price = arr[ind]


    #### gets top 5 results (or less if there are less results available)
    if nrows >= 5:
        final_array = arr_sorted_by_price[:5][:]
    else:
        final_array = arr_sorted_by_price

    return (final_array)

def scraper(driver, destination):

    time.sleep(5)

    html = driver.page_source
    soup = bs.BeautifulSoup(html, "lxml")

    departure_table = create_table(soup, "guttered--double-bottom guttered--mobile-bottom ng-isolate-scope", "departure")
    #print(departure_table)
    #print()
    arrival_table = (create_table(soup,"timetable-inbound guttered--double-bottom guttered--mobile-bottom ng-scope ng-isolate-scope", "arrival"))
    #print(arrival_table)
    top_table = find_top_cheapest(departure_table, arrival_table, destination)
    #print(top_table)
    #driver.quit()
    return(top_table)

def ordered_by_price(arr):
    to_sort = arr[1:][:]
    ind = np.argsort(to_sort[:,-1])
    sorted_total_array = to_sort[ind]
    return(sorted_total_array)

def get_top_results(arr,travel_time):
    travel_time = travel_time.replace(":","")
    travel_time= int(travel_time)
    nrows = len(arr)
    rows_to_remove=[]
    for i in range(nrows):
        dept_travel_time= int(arr[i][1][2])
        arr_travel_time = int(arr[i][2][2])
        if travel_time<dept_travel_time and travel_time<arr_travel_time :
            rows_to_remove.append(i)
    filtered_arr = np.delete(arr,rows_to_remove,axis=0)
    return (filtered_arr)

def show_results(arr,start_point, travel_time):
    by_price = ordered_by_price(arr)
    top = get_top_results(by_price,travel_time)
    print(top)
    file_name = "output_"+start_point+"_"+travel_time+".txt"
    with open(file_name,"w") as file:
        file.write("Maximum travel time: "+travel_time+"\n")
        nrows=len(top)
        for i in range(nrows):
            file.write("Destination: "+top[i][0]+"\n")
            file.write("Travel hours: ")
            file.write(top[i][1][0]+"-"+top[i][1][1]+"\n")
            file.write("Travel time: "+top[i][1][2]+"\n")
            file.write("\n")
