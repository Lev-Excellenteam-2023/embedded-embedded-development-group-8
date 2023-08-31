import os

NUM_OF_IMAGES=5
OK_IMAGES=3
TIME_BETWEEN_IMAGES=1

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