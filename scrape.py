from bs4 import BeautifulSoup as bs4
import urllib.request
import json
import requests

url = 'https://news.yahoo.co.jp/topics'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) '\
    'Chrome/67.0.3396.99 Safari/537.36 '

def getNews(word):
   html = requests.get(url)
   soup = bs4(html.content, "html.parser")

   main = soup.find_all('li',attrs={'class': 'topicsListItem'})

   news_text = []
   news_link = []

   for i in range(0,len(main)):
       news_text.append(main[i].get_text())
       news_link.append(main[i].a.get("href"))

   count = 0
   news = []

   for i in range(0,len(news_text)):
           if news_text[i].find(word) > -1:
               news.append(news_text[i])
               news.append(news_link[i])
               count += 1
   if count == 0:
       news.append("記事が見つかりませんでした！！")

   result = '\n'.join(news)
   return result