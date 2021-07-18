from bs4 import BeautifulSoup as bs4
import urllib.request
import json
import requests

url = 'https://news.google.com/search'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '\
    'AppleWebKit/537.36 (KHTML, like Gecko) '\
    'Chrome/67.0.3396.99 Safari/537.36 '




def getNews(word):
    news = []
    
    params = {'hl':'ja', 'gl':'JP', 'ceid':'JP:ja', 'q':word}
    # url、パラメータを設定してリクエストを送る
    res = requests.get(url, params=params)
    # レスポンスをBeautifulSoupで解析する
    soup = bs4(res.content, "html.parser")
    # レスポンスからh3階層のニュースを抽出する（classにxrnccd　→　NiLAweを含むタグ）
    
    h3_blocks = soup.select(".NiLAwe")
    print("{}と検索し、{}件のニュースがヒットしました。".format(word,len(h3_blocks)))
    for i, h3_entry in enumerate(h3_blocks):
        # 記事を10件だけ処理する
        if len(news) == 6:
            break
        article = {}
        # ニュースのタイトルを抽出する（h3タグ配下のaタグの内容）
        article["text"]  = h3_entry.select_one("h3 a").text
        # ニュースのリンクを抽出する（h3タグ配下のaタグのhref属性）、整形して絶対パスを作る
        article["link"] = urllib.parse.urljoin(url, h3_entry.select_one("h3 a")["href"])
        if h3_entry.select_one("figure img"):
            article["image"] = h3_entry.select_one("figure img")['src']
        else:
            article["image"] ="https://lh3.googleusercontent.com/proxy/Sy3FNVXitGe7c7HPoLauYL97NK0db-Kitp5Bt0bqktUEhEIKgxAx33C-Uxwm4Q9PUfVB3ADdofUvPmGsKOg4Vm_iUzL7mEgRakGYX3bdfPSNdzHJAVhz20IRLvM0NZmx7oCwu6pGegrX=-p-df-h100-w100-rw"
        news.append(article)

    if len(news) ==0:
        news.append("記事が見つかりませんでした！！")
    return news