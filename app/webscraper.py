
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
import datetime


def storeEOD(r,quote,symbol):
    # Aktuelles Datum als Schlüssel
    heutiges_datum = datetime.date.today().isoformat()
    
    # Schlüssel für Redis erstellen
    redis_schluessel = f'eod:{heutiges_datum}:{symbol}'
    
    # Prüfen, ob der Schlüssel bereits vorhanden ist
    if not r.exists(redis_schluessel):
        # Neuen Schlüssel erstellen, wenn er nicht existiert
        redis_schluessel = f'eod:{heutiges_datum}:{symbol}'
    
    # Messwert in Redis speichern
    r.set(redis_schluessel, f'{quote}:{time.time()}')
              
    print(f'Messwert {quote} für {heutiges_datum} in Redis gespeichert.')

class webscraper():

    def grabGenericProducer(url,xpath_string,symbolname,clickaction=None,clickaction2=None):
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
        #url = 'https://www.boerse.de/realtime-kurse/SundP-500-Aktien/US78378X1072'
        driver.get(url)
        logging.debug('opened: ' + url)

        #with connect("ws://localhost:8765") as websocket:
        #    logging.debug('opened websocket connection')

        if clickaction != None:
            # Find the element by XPath
            xpath_of_element = clickaction
            element = driver.find_element(By.XPATH,xpath_of_element)

            # Click on the element
            element.click()
        
        WebDriverWait(driver, 2)  

        if clickaction2 != None:
            # Find the element by XPath
            xpath_of_element = clickaction2
            element = driver.find_element(By.XPATH,xpath_of_element)

            # Click on the element
            element.click()
        
        WebDriverWait(driver, 2)     

        while True:
            #xpath_string = '//*[@id="content_container"]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/span/span[1]'

            try:  
                wait = WebDriverWait(driver, 1)
                element = driver.find_element(By.XPATH,xpath_string).text
                
           
            except exceptions.StaleElementReferenceException as e:
                logging.debug('StaleElementReferenceException: ' + str(e))
                r.setex(symbolname+'_lastexception',1980,str(e))
          
                pass  
            except Exception as e:
                logging.debug('Exception: ' + str(e))
                r.setex(symbolname+'_lastexception',1980,str(e))
                pass

            logging.debug('Generic element ' + str(element))
            
            ##websocket.send(dax)
            keylupd = str(symbolname)+'_lastquote'
            last_published_quote = r.get(keylupd)
           
            logging.debug("last_published_quote: "+ str(last_published_quote))
            if last_published_quote != str(element):
                logging.debug("last_published_quote updated: " +"symbol "+ symbolname +" "+ str(element))
                r.set(symbolname+'_lastquote',str(element))
                lastupdatetime = time.time()
                r.set(f'{keylupd}_last_updated', lastupdatetime)
               
            lastupdatetime = r.get(f'{keylupd}_last_updated')
            logging.debug("lastupdatetime: "+ str(lastupdatetime))
            SP500 = symbolname+":"+str(element)+":"+str(lastupdatetime)
            r.publish(symbolname, str(SP500))
            storeEOD(r,str(element),symbolname)
            
            time.sleep(0.6)

            # close chromedriver and display
        driver.quit()
        display.stop()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(stream=sys.stdout,format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)
 

    #thread = threading.Thread(target = webscraper.grabDAXproducer)
    thread = threading.Thread(target = webscraper.grabGenericProducer, args=('https://www.ls-tc.de/de/', '//*[@id="chart3push"]/span[2]/span','DAX',None,None))
    #thread500 = threading.Thread(target = webscraper.grabGenericProducer, args=('https://www.boerse.de/realtime-kurse/SundP-500-Aktien/US78378X1072','//*[@id="content_container"]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div/div[2]/div[1]/span/span[1]','SP500'))
    thread500 = threading.Thread(target = webscraper.grabGenericProducer, args=('https://www.sg-zertifikate.de/underlying-detail?underlyingId=693','/html/body/app-root/div/app-main/underlying-detail/div/div[2]/div[2]/div[1]/div/div[2]/h5/lightstreamer-ticker-indication/span[1]','SP500','//*[@id="mat-checkbox-1"]/label/div' , '//*[@id="mat-dialog-0"]/cookies-one-layer/div/div/button[2]'))
   
    #threadBTCUSD = threading.Thread(target = webscraper.grabGenericProducer, args=('https://www.coinbase.com/price/bitcoin','//*[@id="PriceSection"]/div[1]/div/div[1]/div[1]/div/div[1]/div[2]/div/span','BTCUSD'))
    threadBTCUSD = threading.Thread(target = webscraper.grabGenericProducer, args=('https://bitcointicker.co/coinbase/btc/usd/1hr/','//*[@id="lastTrade"]','BTCUSD',None,None))
    threadBTCUSD.start()
    logging.debug("threadBTCUSD start: " + str(threadBTCUSD))
    thread.start()
    logging.debug("thread1 start: " + str(thread))
    thread500.start()
    logging.debug("thread2 start: " + str(thread500))
    thread500.join()
    logging.debug("thread finished...exiting")

