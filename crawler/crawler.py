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
from prepare_data.get_url import UrlsManager

TIME_SLEEP       = 2
TIME_OUT         = 40
MAX_COUNT_LOOP   = 100
PUBLISHER        = 'vnexpress'
RAW_DATA_PATH    = os.path.join('../data/raw_data', PUBLISHER)
KILL_FIREFOX_CMD = "pkill firefox"
# run example: python crawler.py -b 8 -p 8

parser = argparse.ArgumentParser()
parser.add_argument('-b', dest='batch_size', type=int, help='Batch size')
parser.add_argument('-p', dest='processes', type=int, help='number of processes for multiprocessing')
args = parser.parse_args()

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

    def get_url(self):
        urls_manager = UrlsManager(publishers=PUBLISHER, data_path=RAW_DATA_PATH)
        urls_manager.fetch_urls()
        self.urls = urls_manager.save_urls()
        # path = '/home/ngogiatien/Projects/HitNews/hitvn-ai-auto-comment/data/raw_data/vnexpress/urls.txt'
        # f = open(path, "r")
        # self.urls = f.readlines()

    def control_slave(self, id):
        print('#{} Crawling {}'.format(id, self.urls[id]))
        slave = CrawlerSlave(url=self.urls[id], options=self.options)
        if slave.driver != None:
            slave.crawl(url_id=id)

    def control_crawling(self):
        batch_size = args.batch_size
        processes  = args.processes
        nrof_batch = math.ceil(len(self.urls) / batch_size)
        for i in range(nrof_batch):
            if i != nrof_batch - 1:
                try:
                    print('Crawl batch', i)
                    pool = multiprocessing.Pool(processes=processes)
                    pool.map(master.control_slave, range(i * batch_size, (i+1) * batch_size))
                    pool.close()
                    pool.join()
                    os.system(KILL_FIREFOX_CMD)
                    # pool.terminate()
                except:
                    os.system(KILL_FIREFOX_CMD)
                gc.collect()
                time.sleep(TIME_SLEEP)
                print('----------------------\n')
            else:
                try:
                    print('Crawl batch', i)
                    pool = multiprocessing.Pool(processes=processes)
                    pool.map(master.control_slave, range(i * batch_size, len(self.urls)))
                    pool.close()
                    pool.join()
                    gc.collect()
                    os.system(KILL_FIREFOX_CMD)
                except:
                    os.system(KILL_FIREFOX_CMD)
                gc.collect()


class CrawlerSlave():
    def __init__(self, url, options):
        self.id       = 0
        self.comments = []
        self.driver   = webdriver.Firefox(executable_path='../web_driver/geckodriver', options=options)
        # set page load timeout
        self.driver.set_page_load_timeout(TIME_OUT)
        try:
            self.driver.get(url)
        except:
            print('Time out')
            self.driver = None
        # wait for loading page
        time.sleep(TIME_SLEEP)
        # body = self.driver.find_element_by_css_selector('body')
        # for i in range(20):
        #     body.send_keys(Keys.PAGE_DOWN)
        #     time.sleep(0.1)
        if self.driver != None:
            self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')

    def get_comment_info(self, root_element, id):
        comment_info = {
            'id'         : id,
            'content'    : "",
            'user_name'  : "",
            'like_count' : 0
        }
        # get content of comment
        try:
            content_less           = root_element.find_element_by_class_name('content_less')
            # content_less = WebDriverWait(root_element, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "content_less")))
            show_full_comment_icon = content_less.find_element_by_class_name('icon_show_full_comment')
            show_full_comment_icon.click()
            comment_info['content'] = root_element.find_element_by_class_name('content_more').text
        except:
            try:
                comment_info['content'] = root_element.find_element_by_class_name('full_content').text
            except:
                pass
        # get more information
        try:
            user_status                = root_element.find_element_by_class_name('user_status')
            comment_info['user_name']  = user_status.find_element_by_class_name('nickname').text.strip()
            comment_info['like_count'] = int(user_status.find_element_by_class_name('total_like').text.strip())
        except:
            pass
        return comment_info

    def crawl_page(self):
        box_comment = self.driver.find_element_by_class_name('main_show_comment')
        try:
            load_more_box = self.driver.find_element_by_class_name('view_more_coment')
            load_more_box.click()
        except:
            pass
        comments         = []
        comment_elements = box_comment.find_elements_by_class_name('comment_item')
        for id, element in enumerate(comment_elements):
            comment_info    = self.get_comment_info(root_element=element, id=self.id)
            sub_comment_box = element.find_element_by_class_name('sub_comment')
            cnt = 0
            while True:
                cnt += 1
                if cnt > MAX_COUNT_LOOP:
                    break
                try:
                    # load more sub comment
                    load_more_sub_comment_element = sub_comment_box.find_element_by_class_name('view_all_reply')
                    load_more_sub_comment_element.click()
                except:
                    break
            sub_comment_elements = sub_comment_box.find_elements_by_class_name('sub_comment_item')
            sub_comment_info     = []
            for sub_id, sub_comment_element in enumerate(sub_comment_elements):
                sub_comment_info.append(self.get_comment_info(root_element=sub_comment_element, id=sub_id))
            comment_info.update({'sub_comment': sub_comment_info})
            comments.append(comment_info)
            self.id += 1
        return comments

    def crawl(self, url_id):
        while True:
            try:
                print('Try crawl page')
                self.comments += self.crawl_page()
                # body = self.driver.find_element_by_css_selector('body')
                # for i in range(10):
                #     body.send_keys(Keys.PAGE_DOWN)
                #     time.sleep(0.1)
            except Exception as e:
                print('Except crawl page')
                print(e)
                pass
            try:
                print('try click next')
                pagination_box   = self.driver.find_element_by_class_name('pagination')
                next_page_button = pagination_box.find_element_by_class_name('next')
                next_page_button.click()
            except Exception as e:
                print('Except click next')
                print(e)
                break
        self.driver.quit()
        # write json file
        with open(os.path.join(RAW_DATA_PATH, 'comment_%03d.json' % url_id), 'w') as out_put:
            json.dump(self.comments, out_put)


if __name__ == '__main__':
    master = CrawlerMaster()
    # get urls
    master.get_url()
    # crawl
    master.control_crawling()
