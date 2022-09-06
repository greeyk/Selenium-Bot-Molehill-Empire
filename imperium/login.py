from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class Login:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def server_choice(self, name, password, server):
        s = self.driver.find_element(By.ID, 'login_server')
        select_server = Select(s)
        select_server.select_by_value(server)

        put_login = self.driver.find_element(By.ID, 'login_user')
        put_login.send_keys(name)
        put_password = self.driver.find_element(By.ID, 'login_pass')
        put_password.send_keys(password)

        submit_login = self.driver.find_element(By.ID, 'submitlogin')
        submit_login.click()

    def login_again(self, name, password):
        self.driver.find_element(By.XPATH, '//*[@id="logout_user"]').send_keys(name)
        self.driver.find_element(By.XPATH, '//*[@id="logout_pass"]').send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="submitlogin_logout"]').click()
