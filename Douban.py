import re
import csv
import time
import random
from urllib import request
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Spider:
    def __init__(self, start_page, end_page):
        self.url = 'https://movie.douban.com/top250?start={}&filter='
        self.start_page = start_page
        self.end_page = end_page

    def get_page(self, url):
        ua = UserAgent()
        header = {
            'User-Agent': ua.firefox,
            # 'Cookie': '__mta=208959789.1585106920033.1593509077842.1593509107607.47;
            # _lxsdk_cuid=1710fbc224bc8-0048503dcb84eb-f313f6d-1a298c-1710fbc224cc8;
            # mojo-uuid=bc73035186bc203e1e0a1a9d69cf0c8f; uuid_n_v=v1;
            # uuid=010A4750BAB111EA977B252D9527D646FCA82B59C6B54FB3934C361D719643F2;
            # _csrf=ab7e60b187089a5c797755f042abdbd14eed1760f8308dc455570ee9ea4edfa2; mojo-session-'
        }
        html = request.Request(url=url, headers=header)
        html = request.urlopen(html)
        return BeautifulSoup(html, 'html.parser')

    def run(self):
        for i in range(self.start_page, self.end_page + 1):
            url = self.url.format(str(25 * (i - 1)))
            self.parse(url)
            time.sleep(random.uniform(1, 2))

    def parse(self, url):
        bs = self.get_page(url)
        bodys = bs.find_all('div', {'class': 'item'})
        for body in bodys:
            order = body.find('em', {'class': ''}).get_text()
            pre_title = body.find('span', {'class': 'title'}).get_text().replace('\n', ' ').replace(' ', '').split('/')
            title = pre_title[0]
            score = body.find('span', {'class': 'rating_num'}).get_text()
            try:
                quote = body.find('span', {'class': 'inq'}).get_text()
            except Exception:
                quote = 'None'
            self.file_save(order, title, score, quote)

    def file_save(self, order, title, score, quote):
        with open('Douban_Top250.csv', 'a', newline='', encoding='utf-8') as csv_file:
            file = csv.writer(csv_file, delimiter=' ')
            file.writerow((order, title, score, quote))


if __name__ == '__main__':
    start = eval(input('Please input start page:\n'))
    end = eval(input('Please input end page:\n'))
    print()
    S = Spider(start, end)
    S.run()