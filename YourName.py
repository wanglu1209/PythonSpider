import requests
import os
from bs4 import BeautifulSoup

BASE_URL = 'https://wall.alphacoders.com/'
BASE_LIST_URL = 'https://wall.alphacoders.com/by_sub_gallery.php?id=6137&page='
PAGE = 1


def getImgList():
    global PAGE
    html = requests.get(BASE_LIST_URL + str(PAGE), timeout=10)
    bsObj = BeautifulSoup(html.text, 'html.parser')
    picAll = bsObj.find_all('div', {'class': 'boxgrid'})
    for a in picAll:
        getImg(str(a.a['href']))

    PAGE += 1
    if PAGE >= 21:
        exit(0)
    print(PAGE)

    getImgList()


def getImg(imgId):
    html = requests.get(BASE_URL + imgId, timeout=10)
    bsObj = BeautifulSoup(html.text, 'html.parser')
    imgUrl = bsObj.find('img', {'class': 'img-responsive'})['src']
    saveImg(imgUrl)


def saveImg(imgUrl):
    global PAGE
    isExists = os.path.exists('Your Name')
    if not isExists:
        os.makedirs('Your Name')
    content = requests.get(imgUrl).content
    imgName = imgUrl[-15:]
    with open('Your Name/' + imgName, 'wb') as fileName:
        fileName.write(content)
    print(imgName + '--------------------> ok')


try:
    getImgList()
except Exception as e:
    print(e)
