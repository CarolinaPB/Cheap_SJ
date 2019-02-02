from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Safari()
driver.get('https://www.sj.se/sv/hem.html#/')

from_location= driver.find_element_by_id("booking-departure")
from_location.send_keys("UPPSALA")


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

#firstday = driver.find_element_by_id("P279231690_table")

table_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='P279231690_table']")))
for table_element in table_elements:
    for row in table_element.find_elements_by_xpath(".//tr"):
        print(row.text)








#driver.quit()
