__author__ = "Cong Minh Vu"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"

from decouple import config

from scrapers import FacebookScraper, PJScraper


config.encoding = "utf-8"


scraper = PJScraper(
    student_id=config("PJ_ID"),
    password=config("PJ_PASS"),
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
        sublist.append(
            f"{k} {v['start']}-{v['end']}{', remotely' if v['remotely'] else ''}"
        )
    mess.append(sublist)

email = config("FB_EMAIL")
password = config("FB_PASS")

messenger = FacebookScraper(email, password)
for m in mess:
    messenger.send_message(m, config("CONVERSATION_ID"), False)
