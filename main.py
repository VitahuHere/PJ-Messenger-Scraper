import base64

from decouple import config

from fbchat import Facebook

config.encoding = "utf-8"
email = base64.b64encode(config("FB_EMAIL").encode("utf-8")).decode("utf-8")
password = base64.b64encode(config("FB_PASS").encode("utf-8")).decode("utf-8")

mess = [
    "Hello There",
    "This is a test message",
    "I hope you like it",
]

messenger = (
    Facebook(email, password)
    .send_message(mess, 10000)
    .send_image(
        r"C:\Users\Zrzut.png",
        10000,
    )
)
