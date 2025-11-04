### Kentapay Admin Portal Login Page ###

import sys, os
sys.path.append(os.getcwd())
from selenium.webdriver.common.by import By
from Src.PageObject.BasePage import BasePage
from Src.PageObject.Locators import LoginLocators

class SignIn(BasePage):
    
    # Element finders
    login_form_title = (By.XPATH, LoginLocators.login_page_title)
    login_button = (By.XPATH, LoginLocators.login_button)
    user_input = (By.XPATH, LoginLocators.user_input)
    password_input = (By.XPATH, LoginLocators.password_input)
    user_input_helper = (By.XPATH, LoginLocators.user_input_helper)
    login_alert = (By.XPATH, LoginLocators.toast_alert_popup)
    login_alert_container = (By.XPATH, LoginLocators.toast_alert_container)
    login_alert_title = (By.XPATH, LoginLocators.toast_alert_title)
    login_alert_message = (By.XPATH, LoginLocators.toast_alert_message)
    login_alert_close_button = (By.XPATH, LoginLocators.toast_alert_close_btn)
    
    # login
    def login(self):
        self.visit("")
        self.getUserInput().send_keys(self.data['users'][1]['username'])
        # self.getPasswordInput().send_keys(os.getenv('CORRECT_PASSWORD'))
        self.getPasswordInput().send_keys('test12345')
        self.getLoginButton().click()
        
    def getLoginButton(self):
        return self.find_element(*self.login_button)
    
    def getUserInput(self):
        return self.find_element(*self.user_input)
    
    def getPasswordInput(self):
        return self.find_element(*self.password_input)
    
    def getUsernameInputHelper(self):
        return self.find_element(*self.user_input_helper)
    
    def getAlert(self):
        return self.find_element(*self.login_alert)
    
    def getAlertContainer(self):
        return self.find_element(*self.login_alert_container)
    
    def getAlertTitle(self):
        return self.find_element(*self.login_alert_title)
    
    def getAlertMessage(self):
        return self.find_element(*self.login_alert_message)
    
    def getAlertCloseButton(self):
        return self.find_element(*self.login_alert_close_button)
    
    def getLoginPageTitle(self):
        return self.find_element(*self.login_form_title)
    
    def getGoogleSearchButton(self):
        return self.find_element(*self.google_search_button)