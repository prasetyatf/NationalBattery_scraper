from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv

class crawler:
    def __init__(self, url: str):
        self.driver = webdriver.Chrome("chromedriver-newest.exe")
        self.wait = WebDriverWait(self.driver, 3)
        self.action = ActionChains(self.driver)
        self.url = self.driver.get(url)

#cookie accept
    def cookie_popup(self):
        try:
            time.sleep(0.5)
            cookie_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".bg-yellow")))
            cookie_button.click()
        except:
            print("probably no cookie notif")
            self.driver.quit()

    def show_detail(self):
        try:
        #Find & open all tabs
            global view_details
            view_details = self.wait.until(EC.presence_of_all_elements_located((By.LINK_TEXT,"View Detail")))
            #table.dataTable
            for detail in view_details:
                detail.send_keys(Keys.CONTROL, Keys.ENTER)
                #break
        except:
            print('show detail error')
            self.driver.quit()

    def move_window(self):
        TAB = 1
        global DATA_BASKET
        DATA_BASKET = []
        
        while len(self.driver.window_handles) > 1: #data tersusun terbalik
            self.driver.switch_to.window(self.driver.window_handles[TAB])

    #Extract data
            time.sleep(0.3)
            data_table = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".table-responsive")))
            datas = data_table.text.split(f'\n')
            DATA_BASKET.append(datas)
            print(datas)
            self.driver.close()

    def to_csv(self):
        with open("result.csv", "a", encoding="utf-8") as write:
            write = csv.writer(write)
            write.writerows(DATA_BASKET)
        self.driver.quit()


nbri = crawler("https://n-bri.org/membership")

nbri.cookie_popup()
nbri.show_detail()
nbri.move_window()
nbri.to_csv()
