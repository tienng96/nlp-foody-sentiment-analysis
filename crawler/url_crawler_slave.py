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
from crawler.crawler_master import CrawlerMaster
import random
import psutil

TIME_SLEEP       = 2
TIME_OUT         = 40
MAX_COUNT_LOOP   = 100

def random_time_sleep(level):
    if level == 0:
        return random.uniform(0.2, 0.5)
    if level == 1:
        return random.uniform(0.5, 1)
    if level >= 2:
        return random.uniform(1, 2)

class CrawlerSlave():
    def __init__(self, url, options):
        self.id = 0
        self.comments = []
        self.driver = webdriver.Firefox(executable_path='../web_driver/geckodriver', options=options)
        # set page load timeout
        self.driver.set_page_load_timeout(TIME_OUT)
        try:
            self.driver.get(url)
        except:
            print('Time out')
            self.driver = None
        self.log_in()
        # wait for loading page
        time.sleep(TIME_SLEEP)
        self.page_down(times=15)

    #         if self.driver != None:
    #             self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')

    def log_in(self):
        log_in_button = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "account-manage")))
        log_in_button.click()
        time.sleep(random_time_sleep(level=1))
        user_name_block = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Email"]')))
        user_name_block.send_keys('langtunhi96@gmail.com')
        time.sleep(random_time_sleep(level=1))
        pass_word_block = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="Password"]')))
        pass_word_block.send_keys('langtunhi96')
        pass_word_block.submit()
        time.sleep(random_time_sleep(level=2))

    def page_down(self, times):
        body = WebDriverWait(self.driver, 30). \
            until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        for i in range(times):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(random_time_sleep(level=0))

    def load_more_result(self):
        load_more_button = WebDriverWait(self.driver, 30). \
            until(EC.presence_of_element_located((By.CLASS_NAME, "fd-btn-more")))
        while True:
            try:
                memory_percent = psutil.virtual_memory().percent
                if memory_percent > 90:
                    print('Stop because memory > 90%')
                    break
                load_more_button.click()
                self.page_down(times=1)
            except:
                break

    def get_urls(self):
        self.urls = []
        result_block = WebDriverWait(self.driver, 30). \
            until(EC.presence_of_element_located((By.CLASS_NAME, 'content-container')))
        result_elements = result_block.find_elements_by_class_name('content-item')
        for element in result_elements:
            url = element.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
            prefix_url = 'https://www.foody.vn'
            if prefix_url not in url:
                url = prefix_url + url
            self.urls.append(url)