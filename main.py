import base64

from decouple import config

from chat import FacebookScraper

config.encoding = "utf-8"
email = base64.b64encode(config("FB_EMAIL").encode("utf-8")).decode("utf-8")
password = base64.b64encode(config("FB_PASS").encode("utf-8")).decode("utf-8")

mess = [
    "Hi",
    "this is an automated message",
    "for testing purposes you are receiving this message",
    "do not resist otherwise you will be removed from the process",
]

messenger = FacebookScraper(email, password).send_message(mess, 100004933353411)
