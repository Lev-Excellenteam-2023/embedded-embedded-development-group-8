import datetime
import os
from firbase_class import Nursery, User, Notification
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#******************************************
# const
database_url = os.environ["DATABASE_URL"]
database_cred_path = os.environ["DATABASE_CRED_PATH"]
cred = credentials.Certificate(database_cred_path)
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': database_url
})
#******************************************


nursery_ref = db.reference("/Nurseries")  # Reference to Firebase database
users_ref = db.reference("/Users")  # Reference to Firebase database
notification_ref = db.reference("/Notification")

def save_nursery(nursery: Nursery):
    """
    Saving nursery in a database
    :param nursery:
    :return:
    """
    new_data_ref = nursery_ref.push({
        'manager_id': nursery.manager_id,
        'contacts': nursery.contacts,
        'notification': nursery.notification,
        'num_babies': nursery.num_babies,
        "secret_code": nursery.secret_code
    })


def save_users(user: User):
    """
    Saving nursery in a database.
    :param user:
    :return:
    """
    new_data_ref = users_ref.push({
        'user_id': user.user_id,
        'state': user.state,
        'manager_id': user.manager_id
    })
def save_notification(notification: Notification):
    """
    Saving notification
    :param notification:
    :return:
    """
    new_data_ref = notification_ref.push({
        'secret_code': notification.secret_code,
        'id_notification': notification.id_notification,
        'start_time': notification.start_time,
        'end_time': notification.end_time,
        'user_id': notification.user_id

    })


def update_notification(id: int, flag: bool):
    """
    The function activates / deactivates an notification in the requested garden.
    :param id: The Telegram ID of the manager of the nursery.
    :param flag:  A variable that represents whether to turn the alert off or on.
    :return:
    """
    nursery = get_nursery_ref()
    if nursery == None:
        return None
    for key, value in nursery.items():
        if value["manager_id"] == id:
            nursery_ref.child(key).update({"notification": flag})


def update_notification(flag: bool):
    """
    The function activates/deactivates a notification in all nursery (The initial plan works to have one nursery)
    The function is temporary because later we will want to identify the gene where there is a problem
    :param flag: A variable that represents whether to turn the alert off or on.
    :return:
    """
    nursery = get_nursery_ref()
    if nursery == None:
        return None
    for key, value in nursery.items():
        nursery_ref.child(key).update({"notification": flag})


def get_nursery_ref():
    """
    :return:The function returns the tables of nursery from firbase.
    """
    return nursery_ref.get()


def get_users_ref():
    """
    The function returns the tables of users from firbase.
    :return:
    """
    return users_ref.get()


def get_nursery(manager_id: int) -> Nursery:
    """
    The function receives an id and looks it up in the table of Nursery we will return the object if we found it
    otherwise we will return None
    :param manager_id: id of the manger of the Nursery
    :return: Nursery ot none if not found
    """
    table_nursery = get_nursery_ref()
    if table_nursery == None:
        return None
    for i in table_nursery.keys():
        if table_nursery[i]["manager_id"] == manager_id:
            return table_nursery[i]
    return None


def find_nursery_by_id(id: str) -> Nursery:
    """
    The function looks for nursery according to the same identifier it received, in case no matching nursery is
    found, the function will return None. :param id:identifier of nursery. :return: nursery or None if not found.
    """
    table_nursery = get_nursery_ref()
    if table_nursery is None:
        return None
    for i in table_nursery.keys():
        if table_nursery[i]["secret_code"] == id:
            return table_nursery[i]
    return None


def get_user(user_id: int) -> User:
    """
    The function receives an id and looks it up in the table of Nursery we will return the object if we found it
    otherwise we will return None
    :param user_id: id of the user
    :return: User ot none if not found
    """
    table_user = get_users_ref()
    if table_user == None:
        return None
    for i in table_user.keys():
        if table_user[i]["user_id"] == user_id:
            return table_user[i]
    return None



def add_contact(code: str, chat_id: int) -> bool:
    """
    The function adds a contact to the list of contacts in nursery.
    :param code:ID of nursery.
    :param chat_id: Contact ID.
    :return: Returns a variable that represents whether the insert was successful or not.
    """
    nursery = get_nursery_ref()
    if nursery == None:
        return False
    for key, value in nursery.items():
        if value["secret_code"] == code:
            new_user = User(chat_id)
            new_user.manager_id = value["manager_id"]
            save_users(new_user)
            print(value["contacts"])
            l = value["contacts"]+[chat_id]
            print(l)
            nursery_ref.child(key).update({"contacts": l})
            return True
    return False


def get_notification_ref():
    """
        The function returns the table of notifications from firbase.
        :return:
        """
    return notification_ref.get()

def get_num_babies():
    nursery = get_nursery_ref()
    if nursery == None:
        return 0
    for key, value in nursery.items():
        return value["num_babies"]
    return 0

# def search_notification (secret_code: str )-> list(Notification):
#     """
#         param: secret code: it is the nursery_id
#         return: The function returns list of notification of the specific nursery.
#     """
#     notification_list = []
#     table_notification = get_notification_ref()
#     if table_notification == None:
#         return None
#     for i in table_notification.keys():
#         if table_notification[i]["secret_code"] == secret_code:
#             notification_list.append(table_notification[i])
#
#     return notification_list
# def calculate_average_reaction_time(secret_code: str)-> float:
#     notification_list = search_notification(secret_code)
#     number_of_notification = 0
#     total_time = 0
#
#     for notification in notification_list:
#         if notification.end_time != None:
#             number_of_notification += 1
#             total_time += (notification.end_time - notification.start_time)
#
#         average_time = total_time / number_of_notification
#         return average_time


