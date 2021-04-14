import messenger
import time
import os


chat = messenger.Chat()
chat.send_picture('conversation thread', 'path to file', 'mail', 'password')
chat.send_message('conversation thread', 'message', 'mail', 'password')
time.sleep(4)
chat.exit()
