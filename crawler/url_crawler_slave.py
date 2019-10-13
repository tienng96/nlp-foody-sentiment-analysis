import sys
sys.path.append('..')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import psutil
from utils.utils import convert_to_nosymbol, gen_uuid_list, random_time_sleep

TIME_OUT         = 40

class CrawlerSlave():
    def __init__(self, url, city, order_option, web_driver_options):
        self.city     = city
        self.order_option = order_option
        self.id       = 0
        self.comments = []
        self.driver   = webdriver.Firefox(executable_path='../web_driver/geckodriver', options=web_driver_options)
        # set page load timeout
        self.driver.set_page_load_timeout(TIME_OUT)
        try:
            self.driver.get(url)
        except:
            print('Time out')
            self.driver = None

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
        time.sleep(random_time_sleep(level=1))

    def page_down(self, times):
        body = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body")))
        for i in range(times):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(random_time_sleep(level=0))

    def load_more_result(self):
        load_more_button = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "fd-btn-more")))
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

    def choose_location_option(self):
        location_options_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "head-province")))
        location_options_box.click()
        input_location_box   = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "loc-query")))
        input_location_box.send_keys(self.city)
        chosen_location_box  = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "flp-countries")))
        location             = chosen_location_box.find_elements_by_class_name('ng-scope')[0]
        location.click()

    def choose_order_option(self):
        order_options_box = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "list-nav")))
        order_options     = order_options_box.find_elements_by_tag_name('li')
        flag              = 0
        for option in order_options:
            if option.text == self.order_option:
                option.click()
                flag = 1
                break
        if flag == 0:
            raise Exception('Not found {} order option'.format(self.order_option))

    def get_urls(self):
        self.urls       = []
        result_block    = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'content-container')))
        result_elements = result_block.find_elements_by_class_name('content-item')
        for element in result_elements:
            url        = element.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
            prefix_url = 'https://www.foody.vn'
            if prefix_url not in url:
                url = prefix_url + url
            self.urls.append(url)

    def save_urls(self):
        url_table = pd.DataFrame()
        url_table['url'] = self.urls
        url_table['city'] = self.city
        url_table['order_option'] = self.order_option
        url_table['id'] = gen_uuid_list(len(self.urls))
        url_table = url_table[url_table.duplicated(subset=['url'], keep='first') == False].reset_index(drop=True)
        url_table.to_csv('../data/urls/urls_{}_{}.csv'.format(convert_to_nosymbol(self.city), convert_to_nosymbol(self.order_option)), index=False)

    def crawl(self):
        try:
            self.choose_location_option()
            self.log_in()
            # wait for loading page
            time.sleep(random_time_sleep(level=2))
            self.page_down(times=10)
            self.choose_order_option()
            self.load_more_result()
            self.get_urls()
            self.save_urls()
            self.driver.quit()
        except:
            print('Error {} - {}'.format(self.city, self.order_option))
            if self.driver is not None:
                self.driver.quit()