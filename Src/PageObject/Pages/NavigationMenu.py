### Stanchart Channels Left Navigation Menu ###

# setup paths for reference
import sys, os
sys.path.append(os.getcwd())

from selenium.webdriver.common.by import By
from Src.PageObject.BasePage import BasePage
from Src.PageObject.Locators import NavigationMenuLocators

class NavigationMenu(BasePage):
    
    # Sidebar element finders
    dashboard_navlink = (By.XPATH, NavigationMenuLocators.dashboard_navlink)
    onboarding_navlink = (By.XPATH, NavigationMenuLocators.onboarding_navlink)
    wakala_support_navlink = (By.XPATH, NavigationMenuLocators.wakala_support_navlink)
    wakala_tools_navlink = (By.XPATH, NavigationMenuLocators.wakala_tools_navlink)
    configs_navlink = (By.XPATH, NavigationMenuLocators.configs_navlink)
    workflows_navlink = (By.XPATH, NavigationMenuLocators.workflows_navlink)
    user_mngmnt_navlink = (By.XPATH, NavigationMenuLocators.user_mngmnt_navlink)
    logout_button = (By.XPATH, NavigationMenuLocators.logout_button)
    # Navbar Items
    notifications_icon = (By.XPATH, NavigationMenuLocators.notifications_icon)
    user_profile_section = (By.XPATH, NavigationMenuLocators.user_profile_section)
    user_profile_menu = (By.XPATH, NavigationMenuLocators.user_profile_menu)
    user_logout_navlink = (By.XPATH, NavigationMenuLocators.logout_navlink)
    # Top section links
    wakala_navlink = (By.XPATH, NavigationMenuLocators.wakala_navlink)
    find_transactions_navlink = (By.XPATH, NavigationMenuLocators.find_transaction_navlink)
    site_visits_navlink = (By.XPATH, NavigationMenuLocators.sit_visits_navlink)
    reported_issues_navlink = (By.XPATH, NavigationMenuLocators.reported_issues_navlink)
    # Bottom page Navigation buttons
    statistics_nav_button = (By.XPATH, NavigationMenuLocators.statistics_navlink)
    agent_commission_nav_button = (By.XPATH, NavigationMenuLocators.agent_commission_navlink)

    # sidebar main menu element getters
    def getDashboardNavlink(self):
        return self.find_element(*self.dashboard_navlink)
    
    def getOnboardingNavlink(self):
        return self.find_element(*self.onboarding_navlink)
    
    def getWakalaSupportNavlink(self):
        return self.find_element(*self.wakala_support_navlink)
    
    def getWakalaToolsNavlink(self):
        return self.find_element(*self.wakala_tools_navlink)
    
    def getWorkflowsNavlink(self):
        return self.find_element(*self.workflows_navlink)
    
    def getConfigsNavlink(self):
        return self.find_element(*self.configs_navlink)
    
    def getUserManagementNavlink(self):
        return self.find_element(*self.user_mngmnt_navlink)
    
    def getLogoutButton(self):
        return self.find_element(*self.logout_button)
    
    # navbar menu getters
    def getNotificationsButton(self):
        return self.find_element(*self.notifications_icon)
    
    def getUserProfileSection(self):
        return self.find_element(*self.user_profile_section)
    
    def getUserProfileMenu(self):
        return self.find_element(*self.user_profile_menu)
    
    def getUserProfileLogoutButton(self):
        return self.find_element(*self.user_logout_navlink)
    
    # Top section navlinks
    def getWakalaNavlink(self):
        return self.find_element(*self.wakala_navlink)
    
    def getFindTransactionsNavlink(self):
        return self.find_element(*self.find_transactions_navlink)
    
    def getReportedIssuesNavlink(self):
        return self.find_element(*self.reported_issues_navlink)
    
    def getSiteVisitsNavlink(self):
        return self.find_element(*self.site_visits_navlink)
    
    # Bottom section navlinks
    def getStatisticsNavButton(self):
        return self.find_element(*self.statistics_nav_button)
    
    def getAgentCommissionNavButton(self):
        return self.find_element(*self.agent_commission_nav_button)