from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import bs4 as bs
import urllib.request
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import Select


driver = webdriver.Safari()
driver.get('https://www.sj.se/sv/hem.html#/')

from_location= driver.find_element_by_id("booking-departure")
from_location.send_keys("Uppsala")


destinations = ['Abisko Turiststation', 'Abisko Östra', 'Kiruna', 'Gällivare', 'Nattavaara', 'Murjek', 'Älvsbyn', 'Jörn', 'Bastuträsk', 'Vindeln', 'Umeå', 'Umeå Ö', 'Nordmaling', 'Örnsköldsvik', 'Kramfors', 'Härnösand', 'Boden', 'Sunderby sjukhus', 'Luleå', 'Duved', 'Åre', 'Järpen', 'Krokom', 'Undersåker', 'Morastrand', 'Mora', 'Rättvik', 'Östersund','Bräcke', 'Ånge', 'Ljusdal', 'Järvsö', 'Bollnäs', 'Ockelbo', 'Timrå', 'Sundsvall', 'Tällberg', 'Ludvika', 'Leksand', 'Insjön', 'Gagnef', 'Djurås', 'Borlänge', 'Smedjebacken', 'Söderbärke', 'Falun', 'Hofors', 'Storvik', 'Sandviken', 'Hudiksvall', 'Söderhamn', 'Gävle', 'Tierp', 'Uppsala', 'Knivsta', 'Arlanda', 'Sundbyberg', 'Stockholm', 'Flemingsberg', 'Södertälje Syd', 'Grängesberg', 'Ställdalen', 'Säter', 'Hedemora', 'Torsåker', 'Horndals Bruk', 'Kongsvinger', 'Avestacentrum', 'Fagersta N', 'Kopparberg', 'Vad', 'Storå', 'Lindesberg', 'Fors', 'Avesta', 'Krylbo', 'Karbenning', 'Fagersta', 'Ängelsberg', 'Virsbo', 'Ramnäs', 'Sala', 'Heby', 'Morgongåva', 'Skinnskatteberg', 'Oslo','Munkedal', 'Uddevalla', 'Ransta', 'Märsta', 'Frövi', 'Surahammar', 'Dingtuna', 'Västerås', 'Arvika', 'Grums', 'Kil', 'Karlstad', 'Kristinehamn', 'Hallstahammar', 'Köping', 'Arboga', 'Kolbäck', 'Bålsta', 'Kvicksund', 'Strängnäs', 'Eskilstuna', 'Läggesta', 'Flen', 'Nykvarn', 'Strömstad', 'Skee', 'Halden', 'Ed', 'Säffle', 'Åmål', 'Mellerud', 'Degerfors', 'Laxå', 'Örebro', 'ÖrebroS', 'Kumla', 'Kungsör', 'Hälleforsnäs', 'Vingåker', 'Tanum', 'Dingle', 'Töreboda', 'Skövde', 'Hallsberg', 'Motala', 'Skänninge', 'Katrineholm', 'Gnesta', 'Vagnhärad', 'Nyköping', 'Öxnered', 'Vänersborg', 'Vara', 'Trollhättan', 'Alingsås', 'Mjölby', 'Tranås', 'Linköping', 'Falköping', 'Norrköping', 'Kolmården', 'Vårgårda', 'Herrljunga', 'Borås', 'Limmared', 'Hestra', 'Gnosjö', 'Helsingborg', 'Kastrup', 'Göteborg', 'Varberg', 'Halmstad', 'Jönköping', 'Huskvarna', 'Nässjö', 'Värnamo', 'Alvesta', 'Älmhult', 'Hässleholm', 'Växjö', 'Hovmantorp', 'Lessebo', 'Emmaboda', 'Nybro', 'Kalmar', 'Köpenhamn', 'Lund', 'Malmö', 'Narvik', 'Rombak', 'Katterat', 'Sösterbekk', 'Björnfjell', 'Riksgränsen', 'Katterjåkk', 'Vassijaure', 'Låktatjåkka', 'Björkliden']

destination_location = driver.find_element_by_id("booking-arrival")
destination_location.send_keys(destinations[0])
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

departure_day = str(4)
return_day = str(20)

tables = driver.find_elements_by_class_name("picker__table")
tables_id =[]
for t in tables:
    tables_id.append(t.get_attribute("id"))


#### Change the day for the departure train
element_to_click = "//*[@id='"+tables_id[0]+"']//button[contains(text(),'"+ departure_day+"') and @class='picker__day picker__day--infocus']"

wait = WebDriverWait(driver,2)
wait.until(EC.element_to_be_clickable((By.XPATH, element_to_click))).click()

#### Change the day for the returning train
element_to_click = "//*[@id='"+tables_id[1]+"']//button[contains(text(),'"+ return_day+"') and @class='picker__day picker__day--infocus']"

wait = WebDriverWait(driver,2)
wait.until(EC.element_to_be_clickable((By.XPATH, element_to_click))).click()

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

driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/main/div[1]/div/div/div/div[2]/div/div/div[3]/div[1]/div/div/div/div[3]/button").click()
