from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os

options = EdgeOptions()
options.use_chromium = True
options.headless = True
options.add_argument('--window-size=1920,1080')


class Librus(object):
    def __init__(self):
        self.driver = Edge("./msedgedriver.exe", options=options)

    def log_in_librus(self, login=None, password=None):
        self.driver.get("https://portal.librus.pl/rodzina")
        self.driver.find_element_by_css_selector('a.btn.btn-third.btn-synergia-top.btn-navbar.dropdown-toggle').click()
        self.driver.find_element_by_css_selector("div.navbar-small-menu a.dropdown-item:nth-of-type(2)").click()
        self.driver.switch_to.frame(self.driver.find_element_by_id('caLoginIframe'))
        self.driver.find_element_by_id("Login").send_keys(login)
        self.driver.find_element_by_id("Pass").send_keys(password, Keys.RETURN)
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "icon-terminarz")))

    def table_today(self):
        elements = []
        self.driver.get('https://synergia.librus.pl/terminarz')
        today_column = self.driver.find_element_by_css_selector('td.center.today')
        self.driver.execute_script("arguments[0].scrollIntoView();", today_column)
        num_of_el = len(today_column.find_elements_by_xpath('./div/table/tbody/tr'))
        for i in range(1, num_of_el+1):
            details = today_column.find_element_by_xpath(f'./div/table/tbody/tr[{i}]/td').get_attribute("title")
            details = details.replace("<br />", "\n")
            elements.append(details)
        today_column.screenshot("ss_table_today.png")
        return elements
    
    def table_date(self, day):
        elements = []
        self.driver.get('https://synergia.librus.pl/terminarz')
        date = self.driver.find_element_by_xpath(f"//div[contains(@class, 'kalendarz-numer-dnia') and text()='{day}']")
        column = date.find_element_by_xpath("./..")
        self.driver.execute_script("arguments[0].scrollIntoView();", column)
        column.screenshot("ss_table_date.png")
        num = len(column.find_elements_by_xpath('./table/tbody/tr'))
        for i in range(1, num + 1):
            details = column.find_element_by_xpath(f'./table/tbody/tr[{i}]/td').get_attribute("title")
            details = details.replace("<br />", "\n")
            elements.append(details)
        return elements
    
    def messages(self):
        inbox = []
        self.driver.get('https://synergia.librus.pl/wiadomosci')
        message_table = self.driver.find_element_by_xpath('//*[@id="formWiadomosci"]/div/div/table/tbody/tr/td[2]/table[2]/tbody')
        num = message_table.find_elements_by_xpath("//td[@style='font-weight: bold;']")
        if len(num) == 0:
            return "No new messages"
        for i in range(1, (len(num)//3)+1):
            mess = message_table.find_element_by_xpath(f"./tr[{i}]")
            inbox.append(mess.text)
        return inbox

    def messages_click(self):
        self.driver.get('https://synergia.librus.pl/wiadomosci')
        tabela_wiadomosci = self.driver.find_element_by_xpath(
            '//*[@id="formWiadomosci"]/div/div/table/tbody/tr/td[2]/table[2]/tbody')
        ile = tabela_wiadomosci.find_elements_by_xpath("//td[@style='font-weight: bold;']")
        for i in range(1, (len(ile) // 3) + 1):
            wiad = tabela_wiadomosci.find_element_by_xpath(f"./tr[{i}]")
            ActionChains(self.driver).key_down(Keys.CONTROL).click(wiad).key_up(Keys.CONTROL).perform()

    def get_grades(self):
        grades = []
        self.driver.get('https://synergia.librus.pl/przegladaj_oceny/uczen')
        grade_table = self.driver.find_element_by_xpath('//*[@id="body"]/form[1]/div/div/table[1]/tbody')
        num = grade_table.find_elements_by_xpath('./tr')
        for i in range(1, len(num) - 1, 2):
            line = self.driver.find_element_by_xpath(f'//*[@id="body"]/form[1]/div/div/table[1]/tbody/tr[{i}]')
            subject = line.find_element_by_xpath('./td[2]').text
            first = line.find_element_by_xpath('./td[3]').text
            second = line.find_element_by_xpath('./td[7]').text
            grades.append([subject, first, second])
        return grades

    def exit(self):
        if os.path.exists('ss_table_date.png'):
            os.remove('ss_table_date.png')
        if os.path.exists('ss_table_today.png'):
            os.remove('ss_table_today.png')
        self.driver.quit()
        os.system('cmd /c "taskkill /IM msedgedriver.exe /F /T"')

