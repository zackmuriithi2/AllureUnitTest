### Dashboard Test Script ###

import sys, os, unittest, allure
sys.path.append(os.getcwd())
from Src.TestBase.WebDriverSetup import WebDriverSetup
from Src.PageObject.Pages.SignInPage import SignIn
from Src.PageObject.Pages.NavigationMenu import NavigationMenu
from Src.PageObject.Pages.DashboardPage import Dashboard

class Dashboard_Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.webdriver = WebDriverSetup()
        cls.driver = cls.webdriver.driver
        with allure.step("Login to system"):
            cls.login_page = SignIn(cls.driver)
            cls.login_page.login()
            
    def setUp(self):
        allure.dynamic.suite("Dashboard Tests")
        allure.dynamic.feature("Dashboard Functionality")
        allure.dynamic.sub_suite("Dashboard Charts and Stats")
        allure.story("Dashboard Overview")
      
    def test_Dashboard_Overview(self):
        allure.dynamic.testcase(url="http://link/to/test-management-system(tms)/probably/squash/project/testcase", name="Dashboard Overview")
        allure.dynamic.severity(allure.severity_level.NORMAL)
        with allure.step("Load Dashboard Page"):
            self.dashboard = Dashboard(self.driver)
            self.menus = NavigationMenu(self.driver)
            self.menus.getDashboardNavlink().click()
            self.assertEqual(self.dashboard.getCurrentPageHeader().text, 'Dashboards', 'Did not redirect to Dashboard')
        with allure.step("Checkout Dashboard"):
            self.assertTrue(self.dashboard.getDashboard().is_displayed(), 'Cannot view the dashboard details')
            self.assertTrue(self.dashboard.getStatCardsSection().is_displayed(), 'Stat cards not visible')
            self.assertTrue(self.dashboard.getPieChart().is_displayed(), 'Pie chart not visible')
            self.assertTrue(self.dashboard.getTransactionsChart().is_displayed(), 'Transactions chart not visible')
            self.assertTrue(self.dashboard.getTotalTransactionsChart().is_displayed(), 'Total Transactions chart not visible')
            self.assertTrue(self.dashboard.getMerchantsStatChart().is_displayed(), 'Merchants\' stat chart not visible')
        with allure.step("Dashboard Overview Complete"): pass
        
    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        if (cls.driver != None):
            cls.driver.close()
            cls.driver.quit()
    
if __name__ == '__main__':
    unittest.main()