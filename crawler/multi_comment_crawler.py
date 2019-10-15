import os
from dotenv import load_dotenv
import subprocess
env_path = '.env'
load_dotenv(dotenv_path=env_path)
import sys
sys.path.append('..')
from constant import options
from utils import utils
import pandas as pd
import multiprocessing
from functools import partial
import multiprocessing as mp
import subprocess
# path_urls = os.environ['PATH_URLS']
path_url = '../data/urls'
path_save_comment = '../data/raw_data'
# def get_url_by_city(city):
#     city_norm = utils.convert_to_nosymbol(city)
def load_urls(path):
    with open(os.path.join(path,'urls.txt')) as input_file:
        urls = input_file.readlines()
    return urls

def getting_city_requirement(city_norm):
    file_needed = []
    for file_name in os.listdir(path_url):
        if city_norm in file_name:
            file_needed.append(file_name)
    return file_needed

def extract(index, urls, ids):
    print("Url:",urls[index])
    extractor = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'comment_crawler_slave.js')
    if os.path.exists(os.path.join(path_save_comment, '{}.json'.format(ids[index]))):
        print("File exists")
        return
    subprocess.call('cd "%(path)s" && node "%(extractor)s" "%(url)s" "%(label)s" > "%(label)s.log" 2>&1' % {
        'path': path_save_comment,
        'extractor': extractor,
        'url': urls[index],
        'label': ids[index]
    }, shell=True)
    print("Extract success url...")

def get_url_by_city(city,path_file):
    city_norm = utils.convert_to_nosymbol(city)
    city_csv = getting_city_requirement(city_norm)
    print("==================",city_csv)
    pd_list = []
    urls = []
    ids = []
    if city_csv != []:
        for file in city_csv:
            path_csv = os.path.join(path_file,file)
            data = pd.read_csv(path_csv)
            pd_list.append(data)
        new_df = pd.concat(pd_list)
        urls = list(new_df['url'].values)
        ids = list(new_df['id'].values)
        print("{} urls extracted from {}...".format(len(urls),city))
    else:
        print("None extracted from {}...".format(city))
    return urls,ids

def main():
    print('Crawling ...')
    total_urls = 0
    for city in options.Location.city:
        urls, ids = get_url_by_city(city, path_url)
        total_urls += len(urls)
        #     pool = mp.Pool(processes=len(urls)
        pool = multiprocessing.Pool(processes=10)
        #     pool.map_async(extract, range(len(urls))) #len(extractor.urls)
        pool.map(partial(extract, urls=urls, ids=ids), range(len(urls)))
        pool.close()
        pool.join()
    print("Total urls:", total_urls)
if __name__ == '__main__':
    main()