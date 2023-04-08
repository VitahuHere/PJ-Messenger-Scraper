__author__ = "Cong Minh Vu"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"


import atexit
import hashlib
import os
import pickle
import pathlib

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from consts import ROOT_DIR, COOKIES, CRED_CACHE_DIR


class BaseScraper:
    def __init__(self, email: str = None, password: str = None):
        self._driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager(path=ROOT_DIR).install())
        )
        self._driver.maximize_window()
        atexit.register(self._dump_cookies, email, password)
        self._cache_path = os.path.join(
            CRED_CACHE_DIR, "." + str(self.__class__.__name__).lower()
        )
        self._cookie_path = os.path.join(
            COOKIES, "." + str(self.__class__.__name__).lower() + ".pkl"
        )

    def _wait_till_loaded(self) -> None:
        while self._driver.execute_script("return document.readyState") != "complete":
            return

    def _dump_cookies(self, email: str = None, password: str = None) -> None:
        pathlib.Path(COOKIES).mkdir(parents=True, exist_ok=True)
        pickle.dump(self._driver.get_cookies(), open(self._cookie_path, "wb"))
        if email is None or password is None:
            return

        with open(self._cache_path, "w") as f:
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
        self._driver.get(url)
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
                self._driver.add_cookie(cookie)
            self._driver.refresh()
            return True

        return False

    def _credentials_changed(self, email: str, password: str) -> bool:
        if not os.path.exists(self._cache_path):
            return True

        with open(self._cache_path, "r") as f:
            creds = [a.strip() for a in f.readlines()]
            if len(creds) != 2:
                return True

            if creds[0] != hashlib.sha256(email.encode("utf-8")).hexdigest():
                return True

            if creds[1] != hashlib.sha256(password.encode("utf-8")).hexdigest():
                return True

        return False
