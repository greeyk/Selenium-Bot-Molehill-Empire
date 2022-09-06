import re
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from imperium.constants import fields, no_click
import time


class Plant:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def autoclick_area(self):
        for field in fields:
            elem = self.driver.find_element(By.XPATH, f'//*[@id="gardenTile{field}"]')
            elem.click()


    def plant(self, *regal_number):
        for number in regal_number:
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="regal_{number}"]').click()    # choose item to plant
            except:
                print('----- Cannot choose item to plant -----')
                continue

            for field in fields:
                elem = self.driver.find_element(By.XPATH, f'//*[@id="gardenTile{field}"]')  # finding available fields
                elem_style = elem.find_element(By.CSS_SELECTOR, '*')

                background_style = str(elem_style.get_attribute('style'))   # checking that is field empty
                match = r".*" + '0.gif' + r".*"

                if re.match(match, background_style) is not None:
                    try:
                        elem.click()
                    except:
                        print('----- Field click error -----')
        time.sleep(2)

        try:
            self.driver.find_element(By.XPATH, '//*[@id="baseDialogButton"]/div[2]').click()    # closing window ads
        except:
            pass


    def harvest(self):
        self.driver.find_element(By.XPATH, '//*[@id="wimpareaHelper"]/div[2]/div').click()
        try:
            self.driver.find_element(By.XPATH, '//*[@id="ernte_log"]/img').click()
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, '//*[@id="baseDialogButton"]/div[2]').click()
        except:
            pass


    def water(self):
        self.driver.find_element(By.XPATH, '//*[@id="giessen"]').click()
        try:
            for field in fields:
                elem_field = self.driver.find_element(By.XPATH, f'//*[@id="gardenTile{field}"]')
                elem_water = elem_field.find_element(By.XPATH, f'//*[@id="gardenTile{field}_water"]')

                elem_plant = elem_field.find_element(By.XPATH, f'//*[@id="gardenTile{field}"]/div[1]')
                elem_field_style = str(elem_plant.get_attribute('style'))

                elem_water_src = str(elem_water.get_attribute('src'))
                src_match = r".*" + 'gegossen.gif' + r".*"

                is_clickable = True

                for i in no_click:
                    style_match = r".*" + i + r".*"
                    if re.match(style_match, elem_field_style, re.IGNORECASE) is not None:
                        is_clickable = False

                if re.match(src_match, elem_water_src, re.IGNORECASE) is None:
                    if is_clickable:
                        elem_field.click()

        except Exception as e:
            print('Watering error -----' + str(e))


    def sell_plants(self):
        buyers_div = self.driver.find_element(By.XPATH, '//*[@id="wimpareaWimps"]')
        number_of_buyers = len(buyers_div.find_elements(By.XPATH, './div'))

        for i in range(number_of_buyers):
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="i{i}"]').click()

            except:
                pass

            elem = self.driver.find_element(By.XPATH, '//*[@id="wimpVerkaufYes"]')

            if str(elem.get_attribute('class')) == "msg_input link":
                product_div = self.driver.find_element(By.XPATH, '//*[@id="wimpVerkaufProducts"]')
                number_of_products = product_div.find_elements(By.XPATH, './div')

                for plant in range(len(number_of_products)):
                    try:
                        plants_amount = self.driver.find_element(By.XPATH,
                                                                 f'//*[@id="wimpVerkaufProducts"]/div[{plant + 1}]')
                        print(str(plants_amount.text))
                    except:
                        pass

                try:
                    suma = self.driver.find_element(By.XPATH, '//*[@id="wimpVerkaufSumAmount"]')
                    print('---------> Sold for ' + str(suma.text))
                    elem.click()
                    time.sleep(5)
                except:
                    pass

            else:
                self.driver.find_element(By.XPATH, '//*[@id="wimpVerkaufLater"]').click()
                time.sleep(1)


