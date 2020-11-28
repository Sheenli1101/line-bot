
#web app

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('5d2Isf4VuIuY8dPY/SKK1LuMGG0lMwN1JWY8c/oG9foLzRf52FBah1jl+tS8Kj2PG5HGTzQ9g8BM//MgCMiSGZXsAvM/u4Aux2LsUBC0M9dQJN3JHJqywf2LmmqWHKs26XPfQkeCe7PhkqvHQ7icmwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d10a08da4d21d972470c64bc14c26521')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()