import atexit
import base64
import os.path
import pickle
import time

from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from consts import (
    TIMEOUT,
    COOKIES,
    SENT_SVG,
    TEXT_BOX,
    DECLINE_COOKIES,
    EMAIL_ID,
    PASS_ID,
    IMAGE_BOX,
    MESSAGE_ROW,
    DELIVERED_SVG,
)


class Facebook:
    def __init__(self, email: str, password: str) -> None:
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager(path="./driver").install())
        )
        self.root = "https://www.facebook.com/"
        self._load_cookies(email, password)
        atexit.register(self._dump_cookies)

    def _wait_till_loaded(self):
        while self.driver.execute_script("return document.readyState") != "complete":
            return

    def _dump_cookies(self):
        pickle.dump(self.driver.get_cookies(), open(COOKIES, "wb"))

    def _load_cookies(self, email: str, password: str):
        self.driver.get(self.root)
        self._wait_till_loaded()

        if os.path.exists(COOKIES):
            cookies = pickle.load(open(COOKIES, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        else:
            self._login(email, password)

    def _login(self, email: str, password: str):
        self.driver.get(self.root)
        self._wait_till_loaded()
        try:
            self.driver.find_element(By.CSS_SELECTOR, f"[{DECLINE_COOKIES}]").click()
        except NoSuchElementException:
            pass

        self.driver.find_element(By.ID, EMAIL_ID).send_keys(
            base64.b64decode(email.encode("utf-8")).decode("utf-8")
        )
        self.driver.find_element(By.ID, PASS_ID).send_keys(
            base64.b64decode(password.encode("utf-8")).decode("utf-8")
        )
        self.driver.find_element(By.ID, PASS_ID).send_keys(Keys.RETURN)

    def _get_conv(self, recipient: str | int):
        if self.driver.current_url != f"{self.root}messages/t/{recipient}":
            self.driver.get(f"{self.root}messages/t/{recipient}")

        WebDriverWait(self.driver, timeout=TIMEOUT).until(
            lambda _: self.driver.find_element(By.CSS_SELECTOR, f"[{TEXT_BOX}]")
        )

    def _wait_till_message_sent(self):
        end_time = time.monotonic() + float(TIMEOUT)
        while True:
            try:
                rows = self.driver.find_elements(By.CSS_SELECTOR, f"[{MESSAGE_ROW}]")
                last_row = rows[-1]
                last_row.find_element(By.CSS_SELECTOR, f"[{DELIVERED_SVG}]")
                return
            except NoSuchElementException:
                try:
                    rows = self.driver.find_elements(
                        By.CSS_SELECTOR, f"[{MESSAGE_ROW}]"
                    )
                    last_row = rows[-1]
                    last_row.find_element(By.CSS_SELECTOR, f"[{SENT_SVG}]")
                    return
                except NoSuchElementException:
                    pass

            time.sleep(0.5)
            if time.monotonic() > end_time:
                break
        raise TimeoutException()

    def send_message(self, message: str, recipient: str | int) -> "Facebook":
        self._get_conv(recipient)
        text_box = self.driver.find_element(By.CSS_SELECTOR, f"[{TEXT_BOX}]")
        text_box.send_keys(message)
        text_box.send_keys(Keys.RETURN)
        self._wait_till_message_sent()
        return self

    def send_image(self, image_path: str, recipient: str | int) -> "Facebook":
        self._get_conv(recipient)
        image_box = self.driver.find_element(By.CSS_SELECTOR, f"[{IMAGE_BOX}]")
        image_box.send_keys(image_path)
        text_box = self.driver.find_element(By.CSS_SELECTOR, f"[{TEXT_BOX}]")
        text_box.send_keys(Keys.RETURN)
        self._wait_till_message_sent()
        return self
