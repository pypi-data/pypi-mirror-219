import logging
import os
from ..settings import *
from datetime import datetime

def setup_logger():
    if not os.path.exists(PATH.OPENI_FOLDER):
        os.mkdir(PATH.OPENI_FOLDER)
    LOG_FORMAT = "%(asctime)s [%(levelname)s] - %(filename)s %(funcName)s() %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
    logging.basicConfig(filename=PATH.LOG_PATH, level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def debug(ob):
    if type(ob) == dict:
        import json
        print(json.dumps(ob, indent=4))
    else:
        print(ob)
    print("Debug stop!")
    exit(1)