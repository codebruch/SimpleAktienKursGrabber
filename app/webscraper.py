
# import external libraries.
import logging
import time
import redis
#logging.basicConfig(filename='grabber.log', encoding='utf-8', level=logging.DEBUG)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import asyncio
from websockets.server import serve
import concurrent.futures
import logging
import queue
import random
import threading
import time
import sys
from websockets.sync.client import connect
from selenium.common import exceptions  

class webscraper():

    def grabDAXproducer():
        r = redis.Redis(host='redis.lan', port=6379, decode_responses=True)

        # set xvfb display since there is no GUI in docker container.
        display = Display(visible=0, size=(800, 600))
        display.start()

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        logging.debug('building session')
        driver = webdriver.Chrome(options=chrome_options)

        ## DO STUFF
        url = 'https://www.ls-tc.de/de/'
        driver.get(url)
        logging.debug('opened: ' + url)

        #with connect("ws://localhost:8765") as websocket:
        #    logging.debug('opened websocket connection')

        while True:
            xpath_string = '//*[@id="chart3push"]/span[2]/span'
            element = driver.find_element(By.XPATH,xpath_string).text

            logging.debug('DAX element ' + str(element))
            dax = "DAX: "+str(element)
            ##websocket.send(dax)
            r.publish("DAX", str(element))
            
            time.sleep(1)

            # close chromedriver and display
        driver.quit()
        display.stop()

    def grabSP500producer():
        r = redis.Redis(host='redis.lan', port=6379, decode_responses=True)

        # set xvfb display since there is no GUI in docker container.
        display = Display(visible=0, size=(800, 600))
        display.start()

        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        logging.debug('building session')
        driver = webdriver.Chrome(options=chrome_options)

        ## DO STUFF
        url = 'https://www.boerse.de/realtime-kurse/SundP-500-Aktien/US78378X1072'
        driver.get(url)
        logging.debug('opened: ' + url)

        #with connect("ws://localhost:8765") as websocket:
        #    logging.debug('opened websocket connection')

        while True:
            xpath_string = '//*[@id="content_container"]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/span/span[1]'

            try:  
                element = driver.find_element(By.XPATH,xpath_string).text
                
                
            except exceptions.StaleElementReferenceException as e:
                logging.debug('StaleElementReferenceException: ' + str(e))
                pass  
            

            logging.debug('SP500 element ' + str(element))
            SP500 = "SP500: "+str(element)
            ##websocket.send(dax)
            r.publish("SP500", str(element))
            
            time.sleep(1)

            # close chromedriver and display
        driver.quit()
        display.stop()



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(stream=sys.stdout,format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)
 

    thread = threading.Thread(target = webscraper.grabDAXproducer)
    thread2 = threading.Thread(target = webscraper.grabSP500producer)
    thread.start()
    logging.debug("thread1 start: " + str(thread))
    thread2.start()
    logging.debug("thread2 start: " + str(thread2))
    thread.join()
    logging.debug("thread finished...exiting")

