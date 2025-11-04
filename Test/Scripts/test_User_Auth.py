### User Login Test Script ###

import sys, os, unittest, allure
sys.path.append(os.getcwd())
from modules.Utilities import Utilities
from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.SignInPage import SignIn
from Src.PageObject.Pages.NavigationMenu import NavigationMenu
from Src.PageObject.Pages.DashboardPage import Dashboard

class Login_Logout_Tests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.webdriver = WebDriverSetup()
        cls.driver = cls.webdriver.driver
        cls.login_page = SignIn(cls.driver)        
        cls.dashboard = Dashboard(cls.driver)
        cls.menus = NavigationMenu(cls.driver)
        
    def setUp(self):
        allure.dynamic.suite("Authentication Tests")
        allure.dynamic.feature("User Authentication")
        allure.dynamic.story("Login and Logout")
        allure.dynamic.sub_suite("Login & Logout")
        # self.driver = self.__class__.driver
        
    def test_1_validate_login_form(self):
        allure.dynamic.title("Login Form Validation")
        allure.dynamic.description("Test to verify user login form validates user input, only allowing proper username")
        allure.dynamic.severity(allure.severity_level.CRITICAL)
        with allure.step("Open login page"):
            self.login_page.visit('')
            self.assertTrue(self.login_page.getLoginPageTitle().is_displayed(), 'Could not open login page')
        with allure.step('Prevent numeric input in username'):
            self.login_page.getUserInput().send_keys('1234567890')
            self.assertTrue(self.login_page.getUsernameInputHelper().is_displayed(), "Did not display error message")
        with allure.step("Prevent special characters (@,_,-,[],' ') input in username"):
            self.login_page.getUserInput().clear()
            self.login_page.getUserInput().send_keys('@')
            self.assertTrue(self.login_page.getUsernameInputHelper().is_displayed(), "'@' symbol was allowed")
            self.login_page.getUserInput().clear()
            self.login_page.getUserInput().send_keys('_')
            self.assertTrue(self.login_page.getUsernameInputHelper().is_displayed(), "Underscore '_' was allowed")
            self.login_page.getUserInput().clear()
            self.login_page.getUserInput().send_keys('[]')
            self.assertTrue(self.login_page.getUsernameInputHelper().is_displayed(), "A square bracket '[]' was allowed")
            self.login_page.getUserInput().clear()
            self.login_page.getUserInput().send_keys('-')
            self.assertTrue(self.login_page.getUsernameInputHelper().is_displayed(), "Dash '-' was allowed")
            self.login_page.getUserInput().clear()
            self.login_page.getUserInput().send_keys('-')
            self.assertTrue(self.login_page.getUsernameInputHelper().is_displayed(), "Dash '-' was allowed")
        with allure.step("Prevent a lot of characters in the input"):
            character_length = 120
            random_chars = Utilities().generate_random_letters(character_length)
            self.login_page.getUserInput().clear()
            self.login_page.getUserInput().send_keys(random_chars)
            self.assertTrue(self.login_page.getUsernameInputHelper().is_displayed(), f"A string of length {character_length} was allowed")
        
    def test_2_Login(self):
        allure.dynamic.title("User Login Test")
        allure.dynamic.description("Test to verify user login functionality with valid and invalid credentials.")
        allure.dynamic.severity(allure.severity_level.CRITICAL)
        with allure.step("Open login page"):
            self.login_page.visit('')
            self.assertTrue(self.login_page.getLoginPageTitle().is_displayed(), 'Could not open login page')
        with allure.step('Prevent login with wrong credentials'):
            self.login_page.getUserInput().send_keys(self.login_page.data['users'][0]['username'])
            self.login_page.getPasswordInput().send_keys(self.login_page.data['users'][0]['password'])
            self.login_page.getLoginButton().click()
            self.assertTrue(self.login_page.getAlertContainer().is_displayed())
        with allure.step("Close error alert notification"):
            self.login_page.getAlertCloseButton().click()
            self.assertTrue(self.login_page.getAlertContainer().is_displayed())
        with allure.step('Allow login with correct credentials'):
            self.login_page.getUserInput().clear()
            self.login_page.getPasswordInput().clear()
            self.login_page.getUserInput().send_keys(self.login_page.data['users'][1]['username'])
            self.login_page.getPasswordInput().send_keys(self.login_page.data['users'][1]['password'])
            self.login_page.getLoginButton().click()
            self.assertEqual(self.dashboard.getCurrentPageHeader().text, 'Dashboards', 'Did not redirect to Dashboard')
        with allure.step("Verify menu is interactible"):
            self.menus.getDashboardNavlink().click()
            self.assertTrue(self.menus.getDashboardNavlink().is_displayed(), 'Dashboard link not displayed')
          
    def test_3_Logout(self):
        allure.dynamic.title("User Logout Test")
        allure.dynamic.description("Test to verify user logout functionality.")
        allure.dynamic.suite("Authentication Tests")
        with allure.step("Click Logout Button"):
            self.menus.getLogoutButton().click()
        with allure.step('Redirect to login page'):
            self.assertTrue(self.login_page.getLoginPageTitle().is_displayed(), 'Did not route back to login page')
        
    def tearDown(self):
        if self.driver:
            self.driver.refresh()

    @classmethod
    def tearDownClass(cls):
        if (cls.driver != None):
            cls.driver.close()
            cls.driver.quit()
    
if __name__ == '__main__':
    unittest.main()