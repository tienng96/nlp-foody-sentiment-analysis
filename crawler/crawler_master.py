import sys
sys.path.append('..')

from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options
import multiprocessing
from constant import options
from crawler.url_crawler_slave import CrawlerSlave


class CrawlerMaster():
    def __init__(self):
        self.url = 'https://www.foody.vn'
        self.web_driver_options = self.set_option_web_driver()
        self.foody_options = []

    def set_option_web_driver(self):
        options = Options()
        ua = UserAgent()
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'  # ua.random
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("window-size=1920,1080")
        # options.add_argument('--headless')
        return options

    def create_foody_option(self):
        for i in range(len(options.Location.city)):
            for j in range(len(options.Option.order_option)):
                self.foody_options.append(
                    {'city': options.Location.city[i], 'order_option': options.Option.order_option[j]})

    def control_url_slave(self, id):
        foody_option = self.foody_options[id]
        print('Crawl URL: {} - {}'.format(foody_option['city'], foody_option['order_option']))
        slave = CrawlerSlave(url=self.url,
                             city=foody_option['city'],
                             order_option=foody_option['order_option'],
                             web_driver_options=self.web_driver_options)
        slave.crawl()

    def control_crawling_urls(self):
        self.create_foody_option()
        nrof_processes = min(multiprocessing.cpu_count(), 8)
        pool = multiprocessing.Pool(processes=nrof_processes)
        pool.map(self.control_url_slave, range(len(self.foody_options)))

if __name__ == '__main__':
    master = CrawlerMaster()
    master.control_crawling_urls()