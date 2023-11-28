
# import external libraries.
import logging
logging.basicConfig(filename='grabber.log', encoding='utf-8', level=logging.DEBUG)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display

# set xvfb display since there is no GUI in docker container.
display = Display(visible=0, size=(800, 600))
display.start()

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

print('building session')
driver = webdriver.Chrome(options=chrome_options)

## DO STUFF

xpath_string = '//*[@id="chart3push"]/span[2]/span'
element = driver.find_element_by_xpath(xpath_string)
logging.debug('element ' + str(element))

# close chromedriver and display
session.quit()
display.stop()
