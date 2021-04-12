from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium import webdriver
from urllib3.exceptions import MaxRetryError
import os
import time
options = EdgeOptions()
options.use_chromium = True
options.headless = True


class Chat:
    def __init__(self):
        self.login = None
        self.password = None
        self.message = None
        self.thread = None
        self.picture = None
        self._driver = None
        self._session = None
        self._executor_url = None

        self._base_url = 'https://www.messenger.com/'
        self._initiate()

    def _initiate(self):
        try:
            with open('SessionExecutor.txt') as f:
                data = f.readlines()
            data = [a.strip() for a in data]
            self._session = data[0]
            self._executor_url = data[1]
            self._driver = webdriver.Remote(command_executor=self._executor_url, desired_capabilities={}, options=options)
            self._driver.session_id = self._session
            print('same browser')
        except (FileNotFoundError, IndexError, MaxRetryError):
            self._driver = Edge("./msedgedriver.exe", options=options)
            with open('SessionExecutor.txt', 'w+', encoding='utf-8') as f:
                f.write(self._driver.session_id)
                f.write('\n')
                f.write(self._driver.command_executor._url)
            print("new browser")

    def _log_in(self):
        self._driver.get(self._base_url)
        self._driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]').click()
        self._driver.find_element_by_id("email").send_keys(self.login)
        self._driver.find_element_by_id("pass").send_keys(self.password, Keys.RETURN)

    def send_message(self, thread, message, login, password):
        try:
            self.message = message
            self.login = login
            self.password = password
            self.thread = thread
        except ValueError:
            return 'Lacking key parameters'
        if "/t" not in self._driver.current_url:
            self._log_in()
        url = self._base_url + 't/' + self.thread
        if self._driver.current_url != url:
            self._driver.get(url)
        WebDriverWait(self._driver, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "_5rp7")))
        self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div[1]/ \
        div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/form/div/div[3]/div[2]/div[1]/div/ \
        div/div/div/div[2]/div/div/div/div').send_keys(self.message, Keys.RETURN)

    def send_picture(self, thread, picture, login, password):
        try:
            self.picture = picture
            self.login = login
            self.password = password
            self.thread = thread
        except ValueError:
            return 'Lacking key parameters'
        if "/t" not in self._driver.current_url:
            self._log_in()
        url = self._base_url + 't/' + self.thread
        if self._driver.current_url != url:
            self._driver.get(url)
        WebDriverWait(self._driver, 10).until(ec.presence_of_element_located((By.XPATH, "/html/body/div[1] \
        /div/div[1]/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/ \
        div[2]/div/form/div/div[3]/div[1]/input")))
        upload_picture = self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/ \
        div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[2]/div/div/div/div[2]/div/form/div/ \
        div[3]/div[1]/input')
        upload_picture.send_keys(self.picture)
        time.sleep(2)
        self._driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/ \
        div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div/div[2]/div/form/div/div[3]/div[2] \
        /div[1]/div/div/div/div/div[2]/div/div/div/div').send_keys(Keys.RETURN)

    def exit(self):
        self._driver.quit()
        os.system('cmd /c "taskkill /IM msedgedriver.exe /F /T"')