# Cheap_SJ

Cheap_SJ searches the [SJ website](https://www.sj.se/#/) for the cheapest prices from a location of your choosing (defaulting to Uppsala) on your choice of dates. There are several options that can be specified.


## To run it
This program uses python3

You'll need to install:
* selenium
* bs4
* lxml
* numpy
Depending on which browser you want to run it:
* chromedriver ([page](http://chromedriver.chromium.org))
* geckodriver
* safaridriver ([Apple's help page](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari))

```
pip3 install selenium
pip3 install bs4
pip3 install lxml
pip3 install numpy

### Webdriver ###
brew install chromedriver
brew install geckodriver
```
To run the program:
```
python3 sj_filler.py -dd DD/MM -rd DD/MM
```
## Arguments
The program can take several arguments:


Argument | Input | Default | Description |
------------ | ------------- |------------- |------------- |
-brw | browser | Chrome | Browser to use
-f | place | Uppsala | Departure place 
-dd | dd/mm | No default | Departure date
-rd | dd/mm | No default | Return date
-ns | int | 2 | Number of students
-mintt | hh:mm | 02:00 | Minimum travel time
-maxtt | hh:mm | 05:00 | Minimum travel time
-nc | int | 1 | Maximum number of transfers
