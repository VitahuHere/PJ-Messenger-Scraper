import requests as req
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from dotenv import dotenv_values


class Messenger:
    def __init__(self, options: ChromeOptions = None, env_path: str = None) -> None:
        self.BASE_URL = "https://www.messenger.com/"
        self.options = options or self._get_default_options()
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.config = self._load_env(env_path=env_path)

    def login(self) -> "Messenger":
        self.driver.get(self.BASE_URL)
        self.driver.find_element(By.CSS_SELECTOR, "[data-cookiebanner=\"accept_only_essential_button\"]").click()
        self.driver.find_element(By.ID, "email").send_keys(self.config.get("FB_EMAIL"))
        self.driver.find_element(By.ID, "pass").send_keys(self.config.get("FB_PASS"))
        self.driver.find_element(By.ID, "loginbutton").submit()
        return self

    def send_message(self, message: str, recipient: str) -> "Messenger":
        self.driver.get(f"{self.BASE_URL}t/{recipient}")
        textbox = self.driver.find_element(By.CSS_SELECTOR, "[role=\"textbox\"]")
        textbox.send_keys(message)
        textbox.submit()
        return self

    def send_image(self, image_path: str, recipient: str) -> "Messenger":
        self.driver.get(f"{self.BASE_URL}t/{recipient}")
        self.driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Attach a photo or video\"]").click()
        self.driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Upload a photo or video\"]").send_keys(image_path)
        self.driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Send photo or video\"]").click()
        return self

    @staticmethod
    def _get_default_options():
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        return options

    @staticmethod
    def _load_env(env_path: str = None):
        return dotenv_values(env_path or ".env")


response = req.post("https://livehereapp.com/api/spaces/matched/")
print(response.text)
# TestPasswordForRequests2023
