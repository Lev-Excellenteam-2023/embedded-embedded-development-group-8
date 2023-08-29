import uuid
from dataclasses import dataclass


@dataclass
class User:
    """
    The class represents a user.
    user_id-id telegram of user.
    state-Keeps the state the user is in, useful for cases where you need to track the user's messages.
    manager_id-id telegram of the manger of
    """
    user_id: int
    state: str
    manager_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.state = ""
        self.manager_id=None

@dataclass
class Nursery:
    """
    The class keeps information on nursery the information you keep,manager_id - The Telegram ID of the manager of
    the nursery, contacts-A list of the Telegram ID of the contacts of the nursery, notification- save whether the
    alarm is activated - if equal to true it is activated, num_babies-The number of babies in the nursery.
    screat_code- A unique ID for the kindergarten, so that contacts who enter can enter their unique ID.
    """
    manager_id: int
    contacts: list[int]
    notification: bool
    num_babies: int
    screat_code:str

    def __init__(self, manager_id: int,num_babies: int):
        self.manager_id = manager_id
        self.contacts = [manager_id]
        self.notification=False
        self.num_babies=num_babies
        self.screat_code= str(uuid.uuid4().hex)

    def add_contact(self,id:int):
        """
        The function adds a contact to nursery
        :param id: telegram ID of the contact
        :return:
        """
        self.contacts.append(id)



