from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options ##
import bs4 as bs
import urllib.request
import argparse
from scraper import scraper, ordered_by_price, get_top_results, show_results
import time
import numpy as np
from location_list import dest

CHROME_PATH = "/usr/bin/google-chrome" ##
CROMEDRIVER_PATH ="/Users/Carolina/Web_scraper/chromedriver"##

total_array = np.array(("Destination","dept_info","arr_info","Price"), dtype=object)

#destinations=dest

destinations = ['Låktatjåkka', 'Björkliden']


parser = argparse.ArgumentParser(description = "Get arguments")
parser.add_argument("-f", "--from", type=str, help ="Starting point", default="Uppsala")
parser.add_argument("-mintt","--mintravelt", type=str, help="Minimum travel time hh:mm", default="03:00")
parser.add_argument("-maxtt","--maxtravelt", type=str, help="Maximum travel time hh:mm",default="05:00")
parser.add_argument("-a1", "--age1", type=int, help="Age of passenger 1",default=22)
parser.add_argument("-a2", "--age2", type=int, help="Age of passenger 2",default=24)
parser.add_argument("-dd", "--deptdate", type=str, help="Departure day dd/mm", default="10/03")
parser.add_argument("-rd", "--retdate", type=str, help="Return day dd/mm",default="10/04")

p_args = parser.parse_args()

#print(p_args.age1)

starting_location = "Uppsala"
for dest in destinations:
    if dest != starting_location:
        driver = webdriver.Safari()
        #driver = webdriver.Chrome("/Users/Carolina/Web_scraper/chromedriver")
        #driver = webdriver.Firefox()
        driver.get('https://www.sj.se/sv/hem.html#/')
        #driver.maximize_window() # TODO: remove


        from_location= driver.find_element_by_id("booking-departure")
        from_location.send_keys(starting_location)

        destination_location = driver.find_element_by_id("booking-arrival")
        #dest = destinations[10]
        destination_location.send_keys(dest)
        #destination_location.send_keys("Stockholm")
        destination_location.send_keys(Keys.RETURN)

        for i in range(10):
            try:
                driver.find_element_by_xpath(
                    ".//*[contains(text(), 'Återresa')]"
                ).click()
                break
            except NoSuchElementException as e:
                print('retry in 1s.')
                time.sleep(1)
        else:
            raise e


        res = driver.execute_script("return document.documentElement.outerHTML")
        soup = bs.BeautifulSoup(res,'lxml')

        departure_date = "10/03"
        return_date = "20/04"

        #### gets ids for the two date tables
        tables = driver.find_elements_by_class_name("picker__table")
        tables_id =[]
        for t in tables:
            tables_id.append(t.get_attribute("id"))

        month_header_id = []
        for el in tables_id:
            month_header_id.append(el.replace("table", "root"))

        ## correct month
        table_month1 = driver.find_elements_by_xpath('//*[@id="'+month_header_id[0]+'"]/div/div/div/div/div/div[1]')
        table_month2 = driver.find_elements_by_xpath('//*[@id="'+month_header_id[1]+'"]/div/div/div/div/div/div[1]')


        month_departure_table = table_month1[0].text


        month_dict={"01":"januari", "02":"februari", "03":"mars", "04":"april","05":"maj", "06":"juni", "07":"juli", "08":"augusti", "09":"september", "10":"oktober", "11":"november", "12":"december"}

        departure_day, departure_month = departure_date.split("/")


        if departure_day[0] =="0":
            departure_day=departure_day[-1]

        departure_month_extended = month_dict[departure_month]


        #### if the inputed month is not the current month, it will change the calendar to the desired month

        while True:
            if departure_month_extended != month_departure_table:
                driver.find_element_by_xpath("//*[@id='"+month_header_id[0]+"']/div/div/div/div/div/div[4]").click()

                table_month1 = driver.find_elements_by_xpath('//*[@id="'+month_header_id[0]+'"]/div/div/div/div/div/div[1]')
                month_departure_table = table_month1[0].text

            else:
                break


        #### Change the day for the departure train
        element_to_click = "//*[@id='"+tables_id[0]+"']//button[text()='"+ departure_day+"' and @class='picker__day picker__day--infocus']"

        wait = WebDriverWait(driver,10)
        wait.until(EC.element_to_be_clickable((By.XPATH, element_to_click))).click()

        table_month2 = driver.find_elements_by_xpath('//*[@id="'+month_header_id[1]+'"]/div/div/div/div/div/div[1]')
        month_return_table = table_month2[0].text
        return_day, return_month = return_date.split("/")
        if return_day[0]=="0":
            return_day=return_day[-1]
        return_month_extended = month_dict[return_month]

        #### change month on the return table
        while True:
            if return_month_extended != month_return_table:
                driver.find_element_by_xpath("//*[@id='"+month_header_id[1]+"']/div/div/div/div/div/div[4]").click()

                table_month2 = driver.find_elements_by_xpath('//*[@id="'+month_header_id[1]+'"]/div/div/div/div/div/div[1]')
                month_return_table = table_month2[0].text
            else:
                break

        #### Change the day for the returning train
        element_to_click2 = "//*[@id='"+tables_id[1]+"']//button[text()='"+ return_day+"' and @class='picker__day picker__day--infocus']"

        wait = WebDriverWait(driver,2)
        wait.until(EC.element_to_be_clickable((By.XPATH, element_to_click2))).click()


        #### choose to search from the earliest departure time possible
        dropdown = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'timeOptionsDeparture')))
        dropdown.click()

        departure_time = dropdown.parent.find_elements_by_xpath('//*[@id="timeOptionsDeparture"]//option')
        departure_time[0].click()

        #### choose to search from the earliest return time possible
        dropdown = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'timeOptionsArrival')))
        dropdown.click()

        return_time = dropdown.parent.find_elements_by_xpath('//*[@id="timeOptionsArrival"]//option')
        return_time[0].click()



        #### expand dropdown and choose traveler category (student)
        dropdown = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'passengerType')))

        # click the dropdown button
        dropdown.click()

        # find all list elements in the dropdown.
        # target the parent of the button for the list
        li = dropdown.parent.find_elements_by_xpath('//*[@id="passengerType"]//option')

        # click the second element in list
        li[2].click()

        #### choose age of first passengers
        age1 = 24
        age2 = 22
        dropdown = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'passengerAge')))

        # click the dropdown button
        dropdown.click()

        # find all list elements in the dropdown.
        # target the parent of the button for the list
        age=list(range(15,31))
        num_seq=list(range(0,16))
        num_seq = num_seq[::-1]
        age_dict = dict(zip(age, num_seq))

        li = dropdown.parent.find_elements_by_xpath('//*[@id="passengerAge"]/option')

        # click the age
        li[age_dict[age1-1]].click()

        add_passenger = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'addPassengerGroup')))

        # click the dropdown button
        add_passenger.click()

        li2 = dropdown.parent.find_elements_by_xpath('//*[@id="addPassengerGroup"]//option')
        li2[3].click() #selects student

        passenger2_age = dropdown.parent.find_elements_by_xpath('(//*[@id="passengerAge"])[2]/option')
        passenger2_age[age_dict[age2-1]].click()

        ### submit and go to next page
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/main/div[1]/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div/div[3]/button").click()

        #### ON THE RESULTS PAGE ####


        time.sleep(5)


        #### show all the times available for departure
        more_travel = driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div[1]/div[5]/div[4]/div/a")
        t = True
        while t:
            for el in more_travel:
                try:
                    el.click()
                    more_travel=driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div[1]/div[5]/div[4]/div/a")
                except WebDriverException:
                    t =False
                    #break

        #### show all the times available bot return
        more_travel2 = driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div[2]/div[5]/div[4]/div/a")
        t = True
        while t:
            for el in more_travel2:
                try:
                    el.click()
                    more_travel=driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/main/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div[2]/div[5]/div[4]/div/a")
                except WebDriverException:
                    t =False
                    #break


        arr = scraper(driver, dest)

        total_array = np.vstack((total_array,arr))
        #print(total_array)

        #driver.quit()

show_results(total_array,starting_location,"03:00", "05:00")
