import os

import requests
from flask import Flask, request, Response
import telegram

TOKEN = os.environ["TELEGRAM_TOKEN"]
init_webhook=os.environ["TELEGRAM_INIT_WEBHOOK_URL"]
TELEGRAM_INIT_WEBHOOK_URL =init_webhook.format(TOKEN)

# requests.get(TELEGRAM_INIT_WEBHOOK_URL) #למה צריך את זה???
list_id=[653029654]
flag=True

app = Flask(__name__)

@app.route('/sanity')
def sanity():
    return "Server is running"

# @app.route('/message', methods=["POST"])
# def handle_message():
#     print("got message")
#     chat_id = request.get_json()['message']['chat']['id']
#     if chat_id not in list_id:
#         list_id.append(chat_id)
#     print(list_id)
#     # res =requests.get(TELEGRAM_INIT_WEBHOOK_URL)
#     requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, "Got it"))
#     # requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, "Got it"))
#     return Response("success")

@app.route('/message', methods=["POST"])
def handle_message():
    print("got message")
    chat_id = request.get_json()['message']['chat']['id']
    msg=request.get_json()['message']['chat']['txt']
    if chat_id not in list_id:
        list_id.append(chat_id)
    print(list_id)
    # res =requests.get(TELEGRAM_INIT_WEBHOOK_URL)
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, msg))
    # requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, chat_id, "Got it"))
    return Response("success")


def send_image(image):
    while flag:
        for id in list_id:
            requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, id, image))
    # print(image)




if __name__ == '__main__':
    send_image("hi")
    app.run(port=5002)
    print("got message")

