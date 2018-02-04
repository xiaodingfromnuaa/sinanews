import requests
from bs4 import BeautifulSoup
import re
import json

sinanewsUrl = 'http://news.sina.com.cn/china'
commonPage = 'http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page={}'

#1- 获取china首页新闻列表
#def getNewsListData(newsUrl):
#    newsList = []

#    res = requests.get(newsUrl)
#    res.encoding = 'utf-8'

#    soup = BeautifulSoup(res.text, 'html.parser')

#    newsSoupList = soup.select('.news-item')

#    for newsSoup in newsSoupList:

#        newsModel = {}

#        if len(newsSoup.select('h2')) > 0:
#            news = newsSoup.select('h2')[0]
#            newsTime = newsSoup.select('.time')[0]

#            # 获取Href
#            a = news.select('a')[0]
#            href = a['href']

#            # 获取新闻ID
#            m = re.search('doc-i(.*?).shtml', href)
#            newsID = m.group(1)

#            # 获取title
#            title = news.text

#            # 获取时间
#            time = newsTime.text

#            newsModel['newsID'] = newsID
#            newsModel['newsHref'] = href
#            newsModel['title'] = title
#            newsModel['time'] = time

#            newsList.append(newsModel)
#    return newsList
#    
#print(getNewsListData(sinanewsUrl))p
	
#2- 获取新闻内详情
def getNewsDetail(newsUrl):
    newsModel = {}
    res = requests.get(newsUrl)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    # 获取newsUrl
    print(newsUrl)

    # 新闻ID
    match = re.search('doc-i(.*?).shtml', newsUrl)
    newsID = match.group(1)
    #print(newsID)

    # 新闻标题
    title = soup.select('.main-title')[0].text
    print(title)

    # 获取时间
    time = soup.select('.date-source span')[0].text
    print(time)

    # 获取来源
    source = ''
    if len(soup.select('.date-source a')) > 0:
        source = soup.select('.date-source a')[0].text
        print(source)
    elif len(soup.select('.source')) > 0:
        source = soup.select('.source')[0].text
        print(source)
    else:
        print('当前未检测到来源', newsUrl)


    #获取内容
    article = '\n'.join([article.text.strip() for article in soup.select('.article p')])
    # for article in soup.select('.article p'):
    #     print(article.text)
    print(article+'\n')

    #获取编辑/作者
    show_author = soup.select('.show_author')[0].text
    #print(show_author)

    newsModel['newsID'] = newsID
    newsModel['newsHref'] = newsUrl
    newsModel['title'] = title
    newsModel['time'] = time
    newsModel['source'] = source
    newsModel['article'] = article
    newsModel['show_author'] = show_author

    return newsModel
    
def getNewLists(url):
    newsList = []
    for i in range(1, 2):
        newsPage = url.format(i)
        # print(newsPage)
        res = requests.get(newsPage)
        res.encoding = 'utf-8'
        if res.status_code == 200:
            jsonData = json.loads(res.text)
            for ent in jsonData['result']['data']:
                newsList.append(getNewsDetail(ent['url']))
        else:
            print('分页结束******')
            break
    return newsList
    
if __name__ == '__main__':
	list = getNewLists(commonPage)
	#print(list)
	print('\n共有'+str(len(list))+'篇新闻')
