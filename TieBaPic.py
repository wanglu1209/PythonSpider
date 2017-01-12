import requests
import os
from bs4 import BeautifulSoup

totalPage = 1
path = '/Users/WangLu/Study/TieBa'
itemName = ''
urlId = ''

BASE_URL = 'http://tieba.baidu.com/f?kw=%E9%BB%91%E4%B8%9D&ie=utf-8'
ITEM_URL = 'http://tieba.baidu.com/p/'


def getImgUrl(id, page=1):
    try:
        global totalPage
        if (totalPage is not None and page is not None) and (int(page) > int(totalPage) or int(page) > 6):
            print("爬取成功")
            return
        url = ITEM_URL + id + '?pn=' + str(page)
        request = requests.get(url, timeout=10)
        htmlText = request.text
        bsObj = BeautifulSoup(htmlText, 'html.parser')
        totalPage = bsObj.find('li', {'class': 'l_reply_num'}).contents[2].get_text()
        content = bsObj.findAll('img', {'class': 'BDE_Image'})
        for s in content:
            saveImg(s['src'])
        page += 1
        getImgUrl(urlId, page)

    except Exception as e:
        print(e)


def saveImg(imgUrl):
    global itemName
    global path

    isExists = os.path.exists(path + '/' + itemName)
    if not isExists:
        os.makedirs(path + '/' + itemName)
    url = path + '/' + itemName + '/' + imgUrl[-15:]
    content = requests.get(imgUrl).content
    with open(url, 'wb') as fileName:
        fileName.write(content)
    return


def getUrl():
    global urlId
    global itemName
    htmlText = requests.get(BASE_URL, timeout=10).text
    bsObj = BeautifulSoup(htmlText, 'html.parser')
    reply = bsObj.findAll('div', {'class': 't_con cleafix'})

    for r in reply:
        replyCount = r.find('div', {'class', 'col2_left j_threadlist_li_left'}).contents[1].get_text()

        if 200 < int(replyCount) < 10000:
            item = r.find('a', {'class', 'j_th_tit'})
            itemName = item.get_text()
            urlId = item['href'][3:]
            print(itemName + "=======================>", end='\t')
            getImgUrl(urlId)


try:
    getUrl()
except Exception as e:
    print(e)
