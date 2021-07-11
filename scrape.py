from bs4 import BeautifulSoup as bs4
import urllib.request
import json
import requests

url = 'https://news.google.com/search'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) '\
    'Chrome/67.0.3396.99 Safari/537.36 '
news_text = []
news_link = []

def getNews(word):
    params = {'hl':'ja', 'gl':'JP', 'ceid':'JP:ja', 'q':word}
    # url、パラメータを設定してリクエストを送る
    res = requests.get(url, params=params)
    # レスポンスをBeautifulSoupで解析する
    soup = bs4(res.content, "html.parser")
    # レスポンスからh3階層のニュースを抽出する（classにxrnccdを含むタグ）
    h3_blocks = soup.select(".xrnccd")
    for i, h3_entry in enumerate(h3_blocks):
        # 記事を10件だけ処理する
        if len(news_text) == 3:
            break
        # ニュースのタイトルを抽出する（h3タグ配下のaタグの内容）
        h3_title = h3_entry.select_one("h3 a").text
        # ニュースのリンクを抽出する（h3タグ配下のaタグのhref属性）
        h3_link = h3_entry.select_one("h3 a")["href"]
        # 抽出したURLを整形して絶対パスを作る
        h3_link = urllib.parse.urljoin(url, h3_link)
        news_text.append(h3_title)
        news_link.append(h3_link)


        # h3階層のニュースからh4階層のニュースを抽出する
        # h4_block = h3_entry.select_one(".SbNwzf")

        # if h4_block != None:
        #     # h4階層が存在するときのみニュースを抽出する
        #     h4_articles = h4_block.select("article")

        #     for j, h4_entry in enumerate(h4_articles):
        #         h4_title = h4_entry.select_one("h4 a").text
        #         h4_link = h4_entry.select_one("h4 a")["href"]
        #         h4_link = urllib.parse.urljoin(url, h4_link)
        #         news_text.append(h4_title)
        #         news_link.append(h4_link)

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