import re
import time

import bs4 as bs
import numpy as np


def create_table(soup, table_class, trip):
    '''
    Creates a table with hour of departure, of arrival to destination, travel time, number of transfers and price
    If any of the rows has a null value, that row is removed from the table (for example, if one of the trips doesn't have a price available)
    '''

    page_table = soup.find("div", {"class": table_class})
    travel_hours = page_table.find_all("div", "timetable__time-info timetable__time-info--small guttered--quarter-vertically ng-binding")

    prices = page_table.find_all('div', {'class': 'timetable-cell timetable-cell__right-cell timetable-cell__unexpanded timetable-cell__unexpanded-class timetable-cell__class ng-isolate-scope'})

    travel_time = page_table.find_all("span", {'class': 'ng-isolate-scope ng-binding'})
    travel_t = []
    for t in range(0, len(travel_time), 2):
        travel_t.append(travel_time[t].text)

    operator = page_table.find_all('div', {'class': 'timetable__extra-info-icon'})

    n_changes = page_table.find_all('span', {'class': 'timetable-cell timetable__extra-info timetable__extra-info--changes ng-binding'})

    nrows = len(travel_hours)
    ncols = 5
    arr = np.empty((nrows, ncols), dtype=object)

    for i in range(nrows):
        hours = travel_hours[i].text.replace("\n", "").strip()
        hours = hours.replace(":", "")

        if trip == "departure":
            h1 = hours[:4]
            h2 = hours[7:]
            if int(h1) <= 1300 and int(h1) >= 700:
                arr[i][0] = h1
                arr[i][1] = h2

        elif trip == "arrival":
            h1 = hours[:4]
            h2 = hours[7:]
            if int(h2) >= 1700:
                arr[i][0] = h1
                arr[i][1] = h2

        arr[i][2] = travel_t[i].replace(" h", "").replace(":", "")

        nc1 = n_changes[i].text.replace("\n", "").strip().replace(" ", "")
        nc2 = re.sub('[^0-9]', '', nc1)  # remove non numeric characters from string
        arr[i][3] = nc2

        price = prices[i].text.replace("\n", "").strip().replace("fr.", "").split(":")[0].replace(" ", "")
        try:
            int(price)
            price = int(price)
        except:
            price = None

        arr[i][4] = price

    # remove rows with None
    mask = np.any(np.equal(arr, None), axis=1)
    arr = (arr[~mask])

    return(arr)


def find_top_cheapest(departure_table, arrival_table, destination):
    '''
    gets the top 5 (or less if less are available) cheapest  for the current location
    '''
    nrows = len(departure_table) * len(arrival_table)
    arr = np.empty((nrows, 4), dtype=object)

    # pairs all the combinations of departures and returns together
    n = 0
    for dept_el in departure_table:
        for arrv_el in arrival_table:
            arr[n][0] = destination
            arr[n][1] = dept_el
            arr[n][2] = arrv_el
            arr[n][3] = dept_el[4] + arrv_el[4]  # total price
            n += 1

    # sorts the array of combinations by total price
    ind = np.argsort(arr[:, -1])
    arr_sorted_by_price = arr[ind]

    # gets top 5 results (or less if there are less results available)
    if nrows >= 5:
        final_array = arr_sorted_by_price[:5][:]
    else:
        final_array = arr_sorted_by_price

    return (final_array)


def scraper(driver, destination):

    time.sleep(1)

    html = driver.page_source
    soup = bs.BeautifulSoup(html, "lxml")
    driver.quit()

    departure_table = create_table(soup, "guttered--double-bottom guttered--mobile-bottom ng-isolate-scope", "departure")

    arrival_table = create_table(soup, "timetable-inbound guttered--double-bottom guttered--mobile-bottom ng-scope ng-isolate-scope", "arrival")

    top_table = find_top_cheapest(departure_table, arrival_table, destination)

    return(top_table)


def ordered_by_price(arr):
    '''
    Orders the array with the information from all the destinations by price (cheapest to most expensive)
    '''
    to_sort = arr[1:][:]
    ind = np.argsort(to_sort[:, -1])
    sorted_total_array = to_sort[ind]
    return(sorted_total_array)


def get_top_results(arr, min_travel, max_travel, nchanges):
    '''
    Filters the results: only keeps the results where the travel time is within the limits imposed by the user and where the number of changes less than the maximum number of changes defined by the user.
    '''
    min_travel = min_travel.replace(":", "")
    min_travel = int(min_travel)
    max_travel = max_travel.replace(":", "")
    max_travel = int(max_travel)
    nrows = len(arr)
    rows_to_remove = []
    rows_to_remove2 = []
    for i in range(nrows):
        dept_travel_time = int(arr[i][1][2])
        arr_travel_time = int(arr[i][2][2])
        if max_travel >= dept_travel_time >= min_travel and max_travel >= arr_travel_time >= min_travel:
            pass
        else:
            rows_to_remove.append(i)
    filtered_arr = np.delete(arr, rows_to_remove, axis=0)

    nrows2 = len(filtered_arr)
    for i in range(nrows2):
        if int(filtered_arr[i][1][3]) <= nchanges and int(filtered_arr[i][2][3]) <= nchanges:
            pass
        else:
            rows_to_remove2.append(i)
    filtered_arr2 = np.delete(filtered_arr, rows_to_remove2, axis=0)

    return (filtered_arr2)


def show_results(arr, start_point, min_travel, max_travel, departure_date, return_date, nstudents, nchanges):
    '''
    Writes the output file
    '''

    by_price = ordered_by_price(arr)
    top = get_top_results(by_price, min_travel, max_travel, nchanges)

    file_name = "WhereToGo_from_" + start_point + ".txt"
    with open(file_name, "w") as file:
        file.write("Travelling from {} to {}\n".format(departure_date, return_date))
        file.write("Starting place: {}\n".format(start_point))
        file.write("Number of students: {}\n".format(nstudents))
        file.write("Minium travel time: " + min_travel + "\n")
        file.write("Maximum travel time: " + max_travel + "\n\n\n")
        nrows = len(top)
        for i in range(nrows):
            file.write("-----------------------\n")
            file.write("          {}            \n".format(top[i][0].upper()))
            file.write("Total price: {} SEK\n".format(top[i][3] * nstudents))
            file.write("Departure:   {}h{}-{}h{}\n".format(top[i][1][0][:2], top[i][1][0][2:], top[i][1][1][:2], top[i][1][1][2:]))
            file.write("Return:      {}h{}-{}h{}\n\n".format(top[i][2][0][:2], top[i][2][0][2:], top[i][2][1][:2], top[i][2][1][2:]))
            file.write("        Departure\n")
            t_time1 = top[i][1][2][-2:]
            t_time2 = top[i][1][2].replace(t_time1, "")
            file.write("Travel time: {}h{}\n".format(t_time2, t_time1))
            file.write("Price:       {} SEK\n".format(top[i][1][4] * nstudents))
            file.write("N tranfers:  {}\n\n".format(top[i][1][3]))
            file.write("         Return\n")
            t_time1 = top[i][2][2][-2:]
            t_time2 = top[i][2][2].replace(t_time1, "")
            file.write("Travel time: {}h{}\n".format(t_time2, t_time1))
            file.write("Price:       {} SEK\n".format(top[i][2][4] * nstudents))
            file.write("N transfers:  {}\n".format(top[i][2][3]))
            file.write("-----------------------")
            file.write("\n\n\n")
