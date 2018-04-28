
from selenium import webdriver


class DriverManager:
    def __init__(self):
        self.driver = None

    def tear_down(self):
        self.driver.quit()
        print(' > driver is closed')

    def run_driver(self):
        if self.driver is None:
            self.driver = webdriver.Chrome('driver/chromedriver')
            self.driver.implicitly_wait(3)
            print(' > driver is loaded')

            return self.driver

    def get_driver(self):
        return self.driver