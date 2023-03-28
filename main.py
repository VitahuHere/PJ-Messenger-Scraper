import base64

from decouple import config

from fbchat import Facebook

config.encoding = "utf-8"
email = base64.b64encode(config("FB_EMAIL").encode("utf-8")).decode("utf-8")
password = base64.b64encode(config("FB_PASS").encode("utf-8")).decode("utf-8")

messenger = (
    Facebook(email, password)
    .send_message("Hello There", 100004933353411)
    .send_message("This is automated message", 100004933353411)
    .send_image(
        r"C:\Users\vumir\PycharmProjects\MessengerChat\Zrzut ekranu 2023-03-01 211138.png",
        100004933353411,
    )
)
