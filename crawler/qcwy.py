import requests
import csv
from bs4 import BeautifulSoup
import execjs
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def search(cityName, cityCode, keyword, index):
    params = {
        'lang': 'c',
        'postchannel': '0000',
        'workyear': '99',
        'cotype': '99',
        'degreefrom': '99',
        'jobterm': '99',
        'companysize': '99',
        'ord_field': '0',
        'dibiaoid': '0',
        'line': '',
        'welfare': ''
    }
    origin = 'https://search.51job.com/list/'
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    }
    url = origin+cityCode+',000000,0000,32,9,99,' + \
        keyword + ',2,'+str(index)+'.html'
    req = requests.get(url=url, headers=header, params=params)
    req = requests.get(url=url, headers=header, params=params)
    req.encoding = 'GBK'
    soup = BeautifulSoup(req.text, 'html.parser')
    sc = soup.body.find_all('script')[3].contents[0]
    sc = sc.replace('window.', '')
    ctx = execjs.compile(
        sc +
        '''
            function get_SEARCH_RESULT() {
                return __SEARCH_RESULT__
            }
            '''
    )
    searchResult = ctx.call('get_SEARCH_RESULT')
    total_page = searchResult['total_page']
    jobList = searchResult['engine_search_result']
    head = ['jobid', 'keyword', 'title', 'place', 'salary', 'experience',
            'education', 'companytype', 'company_name', 'jobwelf','time']

    def get_info(job): return [job['jobid'], keyword, job['job_title'], cityName, job['providesalary_text'],
                               job['attribute_text'][1], job['attribute_text'][2], job['companytype_text'], job['company_name'], job['jobwelf'],job['updatedate']]
    data = []
    for job in jobList[1:]:
        data.append(get_info(job))
    with open('../data/data.csv', 'a', newline='', encoding='GBK') as f:
        f_csv = csv.writer(f)
        # f_csv.writerow(head)
        f_csv.writerows(data)
    if(index <= int(total_page)):
        search(cityName, cityCode, keyword, int(index)+1)
    else:
        print(cityName, cityCode, keyword, ' ===========>succeed')


def searchList():
    threadPool = ThreadPoolExecutor(max_workers=15)
    cityList = csv.reader(open('../data/cityInfo.csv', 'r', encoding='GBK'))
    next(cityList)
    jobList = csv.reader(open('../data/job.csv', 'r', encoding='utf-8'))
    jobList = [i for i in jobList]
    for city in cityList:
        for job in jobList:
            threadPool.map(search, [city[0]], [city[3]], [job[0]], [1])
    threadPool.shutdown(wait=True)

import time
if __name__ == '__main__':
    # search('北京','010000','后端开发',1)
    time_start = time.time()
    searchList()
    time_end = time.time()
    print('totally cost', time_end-time_start)
