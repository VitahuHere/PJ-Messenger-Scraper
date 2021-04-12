import Librus
import messenger
import time
import os


librus = Librus.Librus()
chat = messenger.Chat()
librus.log_in_librus('Login', 'Password')
chat.send_picture('conversation thread', 'path to file', 'mail', 'password')
chat.send_message('conversation thread', 'message', 'mail', 'password')
time.sleep(4)
librus.exit()
