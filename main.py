import urllib.request
import os
import sys
import json
import scrape as sc
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage, CarouselTemplate, CarouselColumn, URIAction
)

app = Flask(__name__)

channel_secret = os.getenv('YOUR_CHANNEL_SECRET', None)
channel_access_token = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN', None)
my_line_user_Id = os.getenv('MY_LINE_USER_ID', None)

if channel_secret is None:
    print('Specify YOUR_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify YOUR_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def create_carucel(result):
    notes = []
    for _, body in enumerate(result):
        notes.append(CarouselColumn(thumbnail_image_url=body["image"],
                            title=body["title"][:40],
                            text=body["text"][:60],
                            # actions=[{"type": "uri","label": "サイトURL","uri": body["link"]}]),
                            defaultAction =URIAction(
                                uri=body["link"]
                            ),
                            actions=[URIAction(
                                label='newsを開く',
                                uri=body["link"]
                            )]
        ))
    messages = TemplateSendMessage(
        alt_text="{}の検索結果".format(body["word"]),
        template=CarouselTemplate(columns=notes),
    )
    return messages

@app.route("/callback", methods=['POST'])
def callback():
    print("コールバックされたの！？")
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def push_mesage(word):
    try:
        line_bot_api.push_message(my_line_user_Id, TextSendMessage(text=word))
    except InvalidSignatureError as e:
        abort(400)

def send_carucel_routine(word, not_find_news):
    news = []
    search_range = 5
    
    news = sc.get_yahoo_news(word[0] + word[1], news, search_range)
    if len(news) != 0:
        messages = create_carucel(news)
        push_mesage("{}の検索結果".format(word[0]))
        line_bot_api.push_message(my_line_user_Id, messages)
    else :
        not_find_news.append(word[0])
    return not_find_news


@handler.add(MessageEvent, message=TextMessage)
def send_carucel_message(event):
    news = []
    word = event.message.text
    search_range = 5
    result = sc.get_yahoo_news(word, news, search_range)
    if len(result) != 0:
        messages = create_carucel(result)
        line_bot_api.reply_message(event.reply_token, messages)
    else :
        messages = "記事が見つかりませんでした！！"
        push_mesage(messages)


messages = "今日のニュース"
push_mesage(messages) 
words = [
    ["日向坂"," (ライブ)"],
    ["ヨルシカ", " (展示 舞台 ライブ)"],
    ["ライゾマティクス", " (展示 舞台 ライブ)"],
    ["東京ゲゲゲイ", " (展示 舞台 ライブ)"],
    ["Creepy Nuts", " (展示 舞台 ライブ)"],
    ["東京事変", " (展示 舞台 ライブ)"],
    ["井上小百合", " (ドラマ 展示 舞台 ライブ)"],
    ["伊藤万理華", " (ドラマ 展示 舞台 ライブ)"],
    ["小坂菜緒", " (ドラマ 展示 舞台 ライブ)"],
    ["バナナマン", " (ドラマ 展示 舞台 ライブ)"],
    ["オードリー", " (ドラマ 展示 舞台 ライブ)"],
    ["空気階段", " (ドラマ 展示 舞台 ライブ)"],
    ["バカリズム", " (ドラマ 展示 舞台 ライブ)"],
    ["東京03", " (ドラマ 展示 舞台 ライブ)"]
]

not_find_news = []
for word in words:
    not_find_news = send_carucel_routine(word, not_find_news)
if not_find_news:
    messages = "{}の記事が見つかりませんでした！！".format(not_find_news)
    push_mesage(messages)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
    print("起動されたよ！！！！！")
    try:
        result = "起動しました"
        push_mesage(result)
    except Exception as e:
        print("エラー: " + str(e))
    