import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
import os
import zipfile
from collections import defaultdict


CHROMEDRIVER_FILENAME = "chromedriver.exe"


def get_chrome_latest_release():
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.request("GET", url)
    return response.text


def download_latest_chrome():
    latest_ver = get_chrome_latest_release()
    url = f"https://chromedriver.storage.googleapis.com/{latest_ver}/chromedriver_win32.zip"
    zip_filename = url.split("/")[-1]
    req = requests.get(url, stream=True)  # Stream allow for immediate download

    # Stop if webdriver exists
    if os.path.exists(CHROMEDRIVER_FILENAME):
        return

    # Stream zip content
    with open(zip_filename, "wb") as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:  # Filter out to keep alive-new chunks
                f.write(chunk)

    # Unzip file
    with zipfile.ZipFile(zip_filename) as chrome_zip:
        chrome_zip.extract(CHROMEDRIVER_FILENAME)

    # Delete zipfile
    os.remove(zip_filename)
    
    return


class DataTable:
    def __init__(self):
        self.table = defaultdict(list)

    def push(self, index, value):
        self.table[index].append(value)

    def keys(self):
        return self.table.keys()

    def values(self):
        return self.table.values()

    def show(self):
        print(self.table)

    def to_csv(self, name):
        with open(name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.keys())
            writer.writeheader()

            # Change {a: [1, 2], b: [1, 2]} to [{a: 1, b: 1}, {a: 2, b: 2}]
            writer.writerows(dict(zip(self.keys(), value)) for value in zip(*self.values()))
            




class crawler:
    def __init__(self, url: str):
        self.driver_fn = download_latest_chrome()
        self.driver = webdriver.Chrome(CHROMEDRIVER_FILENAME)
        self.wait = WebDriverWait(self.driver, 3)
        self.action = ActionChains(self.driver)
        self.url = self.driver.get(url)
        self.table = DataTable()

    #cookie accept
    def cookie_popup(self):
        try:
            time.sleep(0.5)
            cookie_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,"button.btn-readmore")))
            cookie_button.click()

        except:
            pass
            

    def show_detail(self):
        try:
            # Find and open all tabs
            view_details = self.wait.until(
                EC.presence_of_all_elements_located((By.LINK_TEXT,"View Detail")))

            for detail in view_details:
                detail.send_keys(Keys.CONTROL, Keys.ENTER)

        except:
            print("Elements not found")
            self.driver.quit()
            

    def move_window(self):
        
        while len(self.driver.window_handles) > 1:
            # Switch to tab
            self.driver.switch_to.window(self.driver.window_handles[-1])

            # Extract data
            time.sleep(0.3)
            data_table = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.table")))

            rows = data_table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                field, value = columns
                self.table.push(field.text, value.text)

            # Close Tabs
            self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    
    def next_page(self):
        paginate_button = self.driver.find_element(By.CSS_SELECTOR, "a.paginate_button.next")

        if "disabled" in paginate_button.get_attribute("class").split():
            return False

        paginate_button.click()
        return True


    def to_csv(self):
        self.table.to_csv("result.csv")


    def quit(self):
        self.driver.quit()

    
    def run(self):
        self.cookie_popup()

        while True:
            self.show_detail()
            self.move_window()
            time.sleep(1)

            if not self.next_page():
                break

        self.to_csv()
        self.quit()



if __name__ == "__main__":
    nbri = crawler("https://n-bri.org/membership")
    nbri.run()
    ...