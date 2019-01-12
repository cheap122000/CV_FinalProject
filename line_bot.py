# LineBot
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea, ImageSendMessage, TemplateSendMessage, ConfirmTemplate, MessageAction
)
import time
import threading
import datetime
import json
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

app = Flask(__name__)

'''
# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    #sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    #sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
'''

line_bot_api = LineBotApi("LineBot_api_key")
handler = WebhookHandler("LineBot_api_secrete")
table_service = TableService(account_name='acc_name', account_key='acc_key')

@app.route("/pushtest", methods=['POST'])
def pushToGroup():
	body = request.get_data(as_text=True)
	print(body)
	replyM = json.loads(body)
	line_bot_api.push_message('Ue6706d642c7d3872948903d70108ec4f', TextSendMessage(text=replyM['message']))
	return "Send Success"

@app.route("/pushimage", methods=['POST'])
def pushToUser():
    body = request.get_data(as_text=True)
    print(body)
    replyM = json.loads(body)

    line_bot_api.push_message('Ue6706d642c7d3872948903d70108ec4f', messages=ImageSendMessage(original_content_url='https://newsolarwebstorage.blob.core.windows.net/tatunglinebot/{0}'.format(replyM['image']), preview_image_url='https://newsolarwebstorage.blob.core.windows.net/tatunglinebot/{0}'.format(replyM['image']), quick_reply='?'))
    #line_bot_api.push_message('Ue6706d642c7d3872948903d70108ec4f', TextSendMessage(text=replyM['message']))
    line_bot_api.push_message('Ue6706d642c7d3872948903d70108ec4f', TemplateSendMessage(alt_text='要開門嗎?', template=ConfirmTemplate(text=replyM['message'], actions=[MessageAction(label='開門', text='開門'), MessageAction(label='不要', text='不要')])))
    return "Send Success"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    jbody = json.loads(body)
    print('check this:', body)
    user_id = jbody['events'][0]['source']['userId']
    profile = line_bot_api.get_profile(user_id)
    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)
    #print(jbody['events'][0]['source']['groupId'])

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    if event.message.text == '開門':
        task = {}
        task['PartitionKey'] = 'ComputerVision'
        task['RowKey'] = 'instruct'
        task['action'] = 'open'
        table_service.insert_or_replace_entity('testAPPs', task)
        replyM = '已傳送開門訊息'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=replyM))
    else :
        pass 

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()
    port = int(os.environ.get('PORT', 5000))
    print(port)
    app.run(debug=options.debug, host='0.0.0.0', port=port)
    #1
