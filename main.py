import base64

from decouple import config

from chat import FacebookScraper
from chat import PJScraper

scraper = PJScraper(
    student_id=base64.b64encode(config("PJ_ID").encode("utf-8")).decode("utf-8"),
    password=base64.b64encode(config("PJ_PASS").encode("utf-8")).decode("utf-8"),
).get_classes_schedule(0)
mess = []
for key, value in scraper.items():
    mess.append(f"{value['start']}-{value['end']} {key}")

config.encoding = "utf-8"
email = base64.b64encode(config("FB_EMAIL").encode("utf-8")).decode("utf-8")
password = base64.b64encode(config("FB_PASS").encode("utf-8")).decode("utf-8")

messenger = FacebookScraper(email, password).send_message(mess, 10000)
