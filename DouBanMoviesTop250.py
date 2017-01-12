# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://movie.douban.com/top250?start='
FILE_PATH = '豆瓣电影TOP250.txt'
PAGE = 0


def getMovie(page=0):
    global PAGE
    html = requests.get(BASE_URL + str(page)).text
    bs = BeautifulSoup(html, 'html.parser')

    for item in bs.findAll('div', {'class': 'item'}):
        title = item.find('span', {'class': 'title'}).get_text()
        info = item.find('div', {'class': 'bd'})
        movieInfo = ''
        for m in info.p.stripped_strings:
            movieInfo += ('\n' + m)
        ratingNum = '评分：' + info.find('span', {'class', 'rating_num'}).get_text() + '\n'
        print(title + movieInfo + "\n" + ratingNum)
        f.writelines(title + movieInfo + '\n' + ratingNum + '========================================>\n\n')
    PAGE += 25
    if PAGE >= 225:
        print('抓取成功=======================>')
        return
    else:
        getMovie(PAGE)


f = open(FILE_PATH, 'w', encoding='utf-8')
getMovie()
f.close()
