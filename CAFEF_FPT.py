import pytest
import pandas as pd
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions, wait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class TestTestcasefpt():
    dates = []
    titles = []
    links = []
    firstly = []
    author1  = []
    def setup_method(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_testcasefpt(self,Ma):
        self.driver.get("https://s.cafef.vn/du-lieu.chn")
        self.driver.set_window_size(1296, 688)
        self.driver.find_element(By.ID, "search-header").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "search-header")))
        self.driver.find_element(By.ID, "search-header").send_keys(Ma)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#autoCompleteLink p:nth-child(1)")))
        self.driver.find_element(By.CSS_SELECTOR, "#autoCompleteLink p:nth-child(1)").click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'tintucsukien')))
        time.sleep(1)
        self.driver.find_element(By.CLASS_NAME, 'tintucsukien').find_element(By.ID, "aViewMoreLink").click()
         # .find_element(By.LINK_TEXT,"Xem tất cả").click())
        # self.driver.find_element(By.ID, "aViewMoreLink").click()


        # ---------------------------------
        while True:
            time.sleep(1)
            a_elements = self.driver.find_element(By.CLASS_NAME, "tintucsukien").find_element(By.CSS_SELECTOR,'ul').find_elements(By.CSS_SELECTOR,"li")
            print(len(a_elements))
            if len(a_elements) == 0:
                return
            # a = self.driver.current_url
            for i in a_elements:
                # time.sleep(0.65)
                # Wait for the date element to be visible
                # link_stock = self.driver.current_url
                # print(self.driver.current_url)
                # WebDriverWait(i, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "timeTitle")))
                date = i.find_element(By.CLASS_NAME, "timeTitle").text
                title = i.find_element(By.CLASS_NAME,"docnhanhTitle").text
                link = i.find_element(By.CLASS_NAME,"docnhanhTitle").get_attribute('href')

                self.dates.append(date)
                self.titles.append(title)
                self.links.append(link)

                print('date: ', date)
                print('title:', title)
                print('link: ', link)
                # self.driver.get(a)

            self.driver.find_element(By.ID, "spanNext").click()
            if date:
                # Convert the date string to a datetime object for comparison
                date_object = datetime.datetime.strptime(date, "%d/%m/%Y %H:%M")

                # Check if the date is earlier than "01/01/2000 00:00"
                if date_object < datetime.datetime(2000, 9, 1, 0, 0):
                    return

    def layShortText(self):
        for i in self.links:
            self.driver.get(i)
            first=""
            author=""
            # WebDriverWait(i, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"intro")))
            try:
                first = self.driver.find_element(By.CLASS_NAME,"intro").text
            except:
                first =""
            try:
                author = self.driver.find_element(By.CSS_SELECTOR,'p[style="text-align:right;"]').find_element(By.TAG_NAME,'strong').text
            except :
                author = ""
            self.author1.append(author)
            self.firstly.append(first)
            print('Bold The Article:', first )
            print('author', author)
        # try:
        #     self.driver.get(link_stock)
        #     # rest of the code for interacting with the new page
        # except StaleElementReferenceException:
        #     # Handle the exception (e.g., print an error message, log the error, etc.)
        #     # Optionally, you can choose to continue the loop or break, depending on your requirements
        #     continue  # or break


selected_stock = input("Nhập mã cổ phiếu cần chọn: ")
a = TestTestcasefpt()
a.setup_method()
a.test_testcasefpt(selected_stock)
a.layShortText()

df1 = pd.DataFrame(list(zip(a.dates, a.titles, a.links,a.firstly,a.author1)), columns = ['DATE', 'TITLE','LINK','Bold The Article','Author'])
print(df1)

df1.to_excel('FPT.xlsx', index=False)
