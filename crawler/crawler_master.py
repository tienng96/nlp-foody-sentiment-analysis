import sys
sys.path.append('..')

from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import multiprocessing
import json
import time
import os
import math
import argparse
import gc

class CrawlerMaster():
    def __init__(self):
        self.options = self.set_option_web_driver()
        self.urls    = []

    def set_option_web_driver(self):
        options    = Options()
        ua         = UserAgent()
        user_agent = ua.random
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("window-size=1400,600")
        options.add_argument('--headless')
        return options