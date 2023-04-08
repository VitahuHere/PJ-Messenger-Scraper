__author__ = "Cong Minh Vu"
__version__ = "1.0.0"


from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from scraper import BaseScraper
from utils import get_base64_string


class PJScraper(BaseScraper):
    def __init__(
        self,
        student_id: str,
        password: str,
    ):
        super().__init__()
        self._root = "https://planzajec.pjwstk.edu.pl"

        self._student_id = get_base64_string(student_id)
        self._password = get_base64_string(password)
        self._login(self._student_id, self._password)

    def _login(self, student_id: str, password: str) -> None:
        self._driver.get(self._root + "/Logowanie.aspx")
        self._wait_till_loaded()
        self._driver.find_element(
            By.ID, "ContentPlaceHolder1_Login1_UserName"
        ).send_keys(student_id)
        self._driver.find_element(
            By.ID, "ContentPlaceHolder1_Login1_Password"
        ).send_keys(password)
        self._driver.find_element(
            By.ID, "ContentPlaceHolder1_Login1_Password"
        ).send_keys(Keys.RETURN)
        self._wait_till_loaded()
        if self._driver.current_url != self._root + "/TwojPlan.aspx":
            raise Exception("Wrong credentials")

    def get_classes_schedule(
        self, day_of_week: int = -1
    ) -> dict[str, dict[str, dict[str, str]]]:
        if not isinstance(day_of_week, int):
            raise TypeError("Day of week must be an integer")
        if day_of_week < -1 or day_of_week > 6:
            raise ValueError("Day of week must be between -1 and 6")

        if day_of_week == -1:
            start = 0
            stop = 7
        else:
            start = day_of_week
            stop = day_of_week + 1

        self._driver.get(self._root + "/TwojPlan.aspx")
        self._wait_till_loaded()
        table = self._driver.find_element(By.CLASS_NAME, "rsContentTable")
        rows = table.find_elements(By.TAG_NAME, "tr")
        week_day_name = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday",
        }
        subjects = {}
        for i in range(start, stop):
            subjects[week_day_name[i]] = {}
            half = False
            hour = 6
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                for cell in cells[i : i + 1]:
                    if cell.text.strip() != "":
                        div = cell.find_element(
                            By.CSS_SELECTOR,
                            '[id^="ctl00_ContentPlaceHolder1_DedykowanyPlanStudenta_PlanZajecRadScheduler"]',
                        )
                        class_name = cell.text.strip()
                        if "top: 12px" in div.get_attribute("style"):
                            subjects[week_day_name[i]][class_name] = {
                                "start": f"{hour}:{'45' if half else '15'}",
                                "end": f"{hour+2 if half else hour+1}:{'15' if half else '45'}",
                            }
                        else:
                            subjects[week_day_name[i]][class_name] = {
                                "start": f"{hour}:{'30' if half else '00'}",
                                "end": f"{hour+2 if half else hour+1}:{'00' if half else '30'}",
                            }

                        subjects[week_day_name[i]][class_name][
                            "remotely"
                        ] = "rgb(58, 235, 52)" in div.get_attribute("style")
                if half:
                    hour += 1
                half = not half

        return subjects
