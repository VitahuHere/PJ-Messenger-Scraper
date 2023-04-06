import base64

from scraper import BaseScraper


class ScheduleScraper(BaseScraper):
    def __init__(
        self,
        personal_schedule: bool = False,
        group_schedule: bool = False,
        group_id: str = None,
        student_id: str = None,
        password: str = None,
    ):
        super().__init__(student_id, password)
        self.personal_schedule = personal_schedule
        self.group_schedule = group_schedule
        self.group_id = group_id
        self.student_id = base64.b64decode(student_id.encode("utf-8")).decode("utf-8")
        self.password = base64.b64decode(password.encode("utf-8")).decode("utf-8")
        self.root = "https://planzajec.pjwstk.edu.pl/Logowanie.aspx"
