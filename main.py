import base64

from decouple import config

from chat import FacebookScraper
from scrapers import PJScraper

scraper = PJScraper(
    student_id=base64.b64encode(config("PJ_ID").encode("utf-8")).decode("utf-8"),
    password=base64.b64encode(config("PJ_PASS").encode("utf-8")).decode("utf-8"),
).get_classes_schedule()

mess = []
week_day_name = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
for key, value in scraper.items():
    if value == {}:
        continue
    sublist = [key]
    for k, v in value.items():
        sublist.append(f"{k} {v['start']}-{v['end']}{', remotely' if v['remotely'] else ''}")
    mess.append(sublist)

config.encoding = "utf-8"
email = base64.b64encode(config("FB_EMAIL").encode("utf-8")).decode("utf-8")
password = base64.b64encode(config("FB_PASS").encode("utf-8")).decode("utf-8")

messenger = FacebookScraper(email, password)
for m in mess:
    messenger.send_message(m, 1000)
