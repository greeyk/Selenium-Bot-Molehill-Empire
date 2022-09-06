import os
import time

import imperium.constants as const
from selenium import webdriver
from selenium.webdriver.common.by import By
from imperium.login import Login
from imperium.planting import Plant

class Imperium(webdriver.Chrome):
    def __init__(self, driver_path=r"SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Imperium, self).__init__()
        self.implicitly_wait(15)
        #self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def try_login(self, name, password, server):
        login = Login(driver=self)
        login.server_choice(name, password, server)

    def try_login_again(self, name, password):
        Login(driver=self).login_again(name, password)

    def accept_cookies(self):
        self.find_element(By.XPATH, '/html/body/div[6]/div[2]/a[1]').click()

    def closing_windows(self):
        self.find_element(By.XPATH, '/html/body/div[3]/div[9]/img').click()
        time.sleep(0.5)
        self.find_element(By.XPATH, '//*[@id="achievement"]/img').click()
        time.sleep(0.5)
        self.find_element(By.XPATH, '//*[@id="bonuspack_inner"]/div[9]').click()

    def planting(self, *args):
        plant = Plant(driver=self)
        plant.plant(*args)  # nr: 2, 6...

    def harvesting(self):
        Plant(driver=self).harvest()

    def selling(self):
        Plant(driver=self).sell_plants()

    def refreshing(self):
        webdriver.Chrome.refresh(self)

    def watering(self):
        try:
            Plant(driver=self).water()
        except:
            pass

    def quit(self):
        webdriver.Chrome.quit(self)