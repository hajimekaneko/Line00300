import scrape as sc

import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction
)

from linebot.exceptions import (
    InvalidSignatureError
)

channel_secret = os.getenv('YOUR_CHANNEL_SECRET', None)
channel_access_token = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN', None)
my_line_user_Id = os.getenv('MY_LINE_USER_ID', None)

word = "大谷"

result = sc.getNews(word)
line_bot_api = LineBotApi(channel_access_token)

notes = []

for i, body in enumerate(result):
    notes.append(CarouselColumn(thumbnail_image_url=body["image"],
                        title=body["text"][:35],
                        text=body["text"][:35],
                        actions=[{"type": "uri","label": "サイトURL","uri": body["link"]}]),
)


messages = TemplateSendMessage(
    alt_text='news',
    template=CarouselTemplate(columns=notes),
)


line_bot_api.push_message(my_line_user_Id, messages)



