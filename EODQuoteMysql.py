import logging
import queue
import random
import threading
import time
import sys

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(stream=sys.stdout,format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)
 
