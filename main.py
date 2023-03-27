import base64

from decouple import config

from messenger import Facebook

config.encoding = "utf-8"
email = base64.b64encode(config("FB_EMAIL").encode("utf-8")).decode("utf-8")
password = base64.b64encode(config("FB_PASS").encode("utf-8")).decode("utf-8")

messenger = Facebook(email, password).send_message("Hello There", 100004933353411)
