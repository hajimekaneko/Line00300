import scrape as sc

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, TextSendMessage
)

from linebot.exceptions import (
    InvalidSignatureError
)

channel_secret = os.getenv('YOUR_CHANNEL_SECRET', None)
channel_access_token = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN', None)
my_line_user_Id = os.getenv('MY_LINE_USER_ID', None)

line_bot_api = LineBotApi(channel_access_token)

def push_mesage(word):
    try:
        line_bot_api.push_message(my_line_user_Id, TextSendMessage(text=word))
    except InvalidSignatureError as e:
        pass


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

word = "日向s坂"
result = sc.get_yahoo_news(word)
if len(result) != 0:
    messages = create_carucel(result)
    line_bot_api.push_message(my_line_user_Id, messages)
else :
    messages = "記事が見つかりませんでした！！"
    push_mesage(messages)



