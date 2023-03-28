import base64

from decouple import config

from fbchat import Facebook

config.encoding = "utf-8"
email = base64.b64encode(config("FB_EMAIL").encode("utf-8")).decode("utf-8")
password = base64.b64encode(config("FB_PASS").encode("utf-8")).decode("utf-8")

messenger = (
    Facebook(email, password)
    .send_message("Hello There", 10000)
    .send_message("This is automated message", 10000)
    .send_image(
        r"path_to_image",
        10000,
    )
)
