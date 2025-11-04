### KentaPay Admin Portal Dashboard Page ###

# setup paths for reference
import sys, os
sys.path.append(os.getcwd())

from selenium.webdriver.common.by import By
from Src.PageObject.BasePage import BasePage
from Src.PageObject.Locators import DashboardLocators

class Dashboard(BasePage):
    
    # Element finders
    dashboard = (By.XPATH, DashboardLocators.dashboard_section)
    stat_cards_section = (By.XPATH, DashboardLocators.dashboard_stat_cards)
    pie_chart = (By.XPATH, DashboardLocators.dashboard_pie_chart)
    transactions_chart = (By.XPATH, DashboardLocators.dashboard_transactions_chart)
    total_transactions_chart = (By.XPATH, DashboardLocators.dashboard_total_trans_chart)
    merchants_stat_chart = (By.XPATH, DashboardLocators.dashboard_merchant_chart)
    
    # element getters
    def getDashboard(self):
        return self.find_element(*self.dashboard)
    
    def getStatCardsSection(self):
        return self.find_element(*self.stat_cards_section)
    
    def getPieChart(self):
        return self.find_element(*self.pie_chart)
    
    def getTransactionsChart(self):
        return self.find_element(*self.transactions_chart)
    
    def getTotalTransactionsChart(self):
        return self.find_element(*self.total_transactions_chart)
    
    def getMerchantsStatChart(self):
        return self.find_element(*self.merchants_stat_chart)