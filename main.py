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
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage, CarouselTemplate, CarouselColumn
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
                            actions=[{"type": "uri","label": "サイトURL","uri": body["link"]}]),
    )
    messages = TemplateSendMessage(
        alt_text='news',
        template=CarouselTemplate(columns=notes),
    )
    return messages


@app.route("/callback", methods=['POST'])
def callback():
    print("コールバックされたよ！！")
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    word = event.message.text
    result = sc.getNews(word)
    messages = create_carucel(result)
    
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=messages)
    )

def push_mesage(word):
    try:
        line_bot_api.push_message(my_line_user_Id, TextSendMessage(text=word))
    except InvalidSignatureError as e:
        abort(400)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
    print("起動されたよ！！！！！")
    try:
        result = "起動しました"
        push_mesage(result)
    except Exception as e:
        print("エラー: " + str(e))
    