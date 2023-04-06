import atexit
import hashlib
import os
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from consts import ROOT_DIR, COOKIES, CRED_CACHE_DIR


class BaseScraper:
    def __init__(self, email: str = None, password: str = None):
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager(path=ROOT_DIR).install())
        )
        atexit.register(self._dump_cookies, email, password)
        self.cache_path = os.path.join(CRED_CACHE_DIR, "." + str(self.__class__.__name__).lower())

    def _wait_till_loaded(self) -> None:
        while self.driver.execute_script("return document.readyState") != "complete":
            return

    def _dump_cookies(self, email: str = None, password: str = None) -> None:
        pickle.dump(self.driver.get_cookies(), open(COOKIES, "wb"))
        if email is None or password is None:
            return

        with open(self.cache_path, "w") as f:
            f.write(hashlib.sha256(email.encode("utf-8")).hexdigest())
            f.write("\n")
            f.write(hashlib.sha256(password.encode("utf-8")).hexdigest())

    def _can_load_cookies(
        self,
        url: str,
        cookies_path: str,
        email: str = None,
        password: str = None,
    ) -> bool:
        self.driver.get(url)
        self._wait_till_loaded()
        if (
            email is not None
            and password is not None
            and self._credentials_changed(email, password)
        ):
            return False

        if os.path.exists(cookies_path):
            cookies = pickle.load(open(cookies_path, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
            return True

        return False

    def _credentials_changed(self, email: str, password: str) -> bool:
        if not os.path.exists(self.cache_path):
            return True

        with open(self.cache_path, "r") as f:
            creds = [a.strip() for a in f.readlines()]
            if len(creds) != 2:
                return True

            if creds[0] != hashlib.sha256(email.encode("utf-8")).hexdigest():
                return True

            if creds[1] != hashlib.sha256(password.encode("utf-8")).hexdigest():
                return True

        return False
