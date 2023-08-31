import threading
import os
import requests
from flask import Flask, request, Response
import telegram
import time

from firbase_class import Nursery, User
from firbase_func import get_nursery_ref, get_user, update_notification, save_nursery, save_users,find_nursery_by_id,add_contact


#******************************************
# const
msg_notification = "There is a baby in danger send /stop_notification to stop the notification"
msg_new_user = "Welcome, if you are manager of a nursery enter a secret code and number of babies. if you are contact enter a secret code of the nursery"
msg_not_valid_command = "Select a valid command"
msg_stop_notification = "The notification is off"
msg_incorrect_code = "The secret code is incorrect\n" + msg_new_user
msg_succeeded_new_nursery = "The nursery required for the system Welcome!\n ID nursery ="
msg_entry_options = "You are not registered in the system.\n There are two entry options:\n 1. If you are an manager of nursery /manager\n2. If you are a kindergarten contact /contact \n"
msg_secret_code_nursery_wrong="secret code of nursery wrong\n" + msg_new_user
msg_add_new_contact="Adding the contact was successful"
SECRET_CODE=100

webhook=os.environ["webhook"]
TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_INIT_WEBHOOK_URL="https://api.telegram.org/bot"+TOKEN+"/setWebhook?url="+webhook+"/message"

#******************************************


requests.get(TELEGRAM_INIT_WEBHOOK_URL)  # למה צריך את זה???

app = Flask(__name__)


def stop_notification(id: int)->str:
    """
    The function receives the id of a contact in nursery and turns off the notification of nursery.
    :param id: the telegram id of user.
    :return: The function returns a message to the user that the alert has been turned off or a message that the user
    is not recognized by the system.
    """
    user = get_user(id)
    if user==None:
        return msg_entry_options
    update_notification( False)
    return msg_stop_notification


def send_msg(msg:str, id:int):
    """
    The function sends a message to the ID it received.
    :param msg: the message you want to send
    :param id: The ID to which the message is sent.
    :return:
    """
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(TOKEN, id, msg))

def new_contact(code: str, chat_id:int)->str:
    """
    The function receives an ID of chat_id and adds the nursery as a contact if code=screat code of nursery and adds the chat_id as a new user.
    :param code: The code of the nursery to which you want to add the contact.
    :param chat_id: ID of the Telegram bot of the user you want to add as a contact
    :return: Returns a message to be sent to the user, saying whether adding the contact was successful or not.
    """
    if add_contact(code,chat_id):
        return msg_add_new_contact
    else:
        return msg_new_user

#The function currently exists for testing, but it needs to be deleted.
def start_notification(flag):
    update_notification(flag)

def new_id(txt:str, chat_id:int)->str:
    """
    The function handles the case that a new user enters the system, if the message received is a secret code of the
    product and a baby number we will add it as nursery new and if the message is an ID of nursery we will add the user as a
    contact.
    :param txt: msg from the user.
    :param chat_id: Tuser telgram id
    :return: The function returns a message to the user
    """
    s = txt.split()
    if len(s) == 2:
        code = s[0]
        if code == str(SECRET_CODE):
            num_babies = s[1]
            new_nursery = Nursery(chat_id, num_babies)
            new_user = User(chat_id)
            new_user.manager_id=chat_id
            save_nursery(new_nursery)
            save_users(new_user)
            return msg_succeeded_new_nursery+new_nursery.secret_code
        else:
            return msg_new_user
    if len(s)==1:
        return new_contact(txt, chat_id)
    else:
        return msg_new_user





state = {"/stop_notification": stop_notification,"/start_notification":start_notification}


@app.route('/sanity')
def sanity():
    return "Server is running"


@app.route('/message', methods=["POST"])
def handle_message():
    data = request.json
    print(data)
    chat_id = data['message']['chat']['id']
    msg = data['message']['text']
    msg_send=""
    if get_user(chat_id) == None:
        msg_send=new_id(msg, chat_id)
    else:
        try:
            msg_send=state[msg](chat_id)
        except:
            msg_send=msg_not_valid_command+" /stop_notification " +"/start_notification"
    send_msg(msg_send,chat_id)
    return Response("success")


def send_notification():
    while True:
        nursery=get_nursery_ref()
        if nursery!=None:
            for id in nursery:
                if nursery[id]["notification"]:
                    for id in nursery[id]["contacts"]:
                        send_msg(msg_notification, id)


def start_telegram_warks():
    t1 = threading.Thread(target=send_notification, args=())
    t1.start()
    app.run(port=5002)
    t1.join()

if __name__ == '__main__':
    start_telegram_warks()