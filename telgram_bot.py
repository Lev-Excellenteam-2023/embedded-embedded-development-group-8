import threading
import os
import requests
from flask import Flask, request, Response
import telegram
import time
import consts
from consts import TOKEN
from firbase_class import Nursery, User
from firbase_func import get_nursery_ref, get_user, update_notification, save_nursery, save_users,find_nursery_by_id,add_contact


requests.get(consts.TELEGRAM_INIT_WEBHOOK_URL)
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
        return consts.msg_entry_options
    update_notification( False)
    return consts.msg_stop_notification


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
        return consts.msg_add_new_contact
    else:
        return consts.msg_new_user

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
        if code == str(consts.SECRET_CODE):
            num_babies = s[1]
            new_nursery = Nursery(chat_id, num_babies)
            new_user = User(chat_id)
            new_user.manager_id=chat_id
            save_nursery(new_nursery)
            save_users(new_user)
            return consts.msg_succeeded_new_nursery+new_nursery.secret_code
        else:
            return consts.msg_new_user
    if len(s)==1:
        return new_contact(txt, chat_id)
    else:
        return consts.msg_new_user





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
            msg_send=consts.msg_not_valid_command+" /stop_notification " +"/start_notification"
    send_msg(msg_send,chat_id)
    return Response("success")


def send_notification():
    """
    The function sends notifications to all the genes whose notification is on.
    :return:
    """
    while True:
        nursery = get_nursery_ref()
        if nursery is not None:
            for id in nursery:
                if "notification" in nursery[id]:
                    if nursery[id]["notification"] == "rolling":
                        for contact_id in nursery[id]["contacts"]:
                            send_msg(consts.msg_notification, contact_id)
                    elif nursery[id]["notification"] == "not_moving":
                        for contact_id in nursery[id]["contacts"]:
                            send_msg(consts.msg_movement, contact_id)
        time.sleep(5)


def start_telegram_warks():
    t1 = threading.Thread(target=send_notification, args=())
    t1.start()
    app.run(port=5002)
    t1.join()

if __name__ == '__main__':
    start_telegram_warks()