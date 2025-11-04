### Locators.py ###

class LoginLocators(object):
    # Login Page (https://test-portal.ekenya.co.ke/mobile-banking/auth/login)
    google_search_button = "//body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]"
    login_page_title = "//app-root//div[contains(@class,'auth-form')]//h3"
    user_input = "//input[@id='username']"
    user_input_helper = "//nz-form-control//div[contains(@class,'ant-form-item-explain-error')]/div"
    password_input = "//input[@type='password']"
    login_button = "//button[@id='alt-btn']"
    toast_alert_popup = "//nz-notification"
    toast_alert_container = "//nz-notification//div[contains(@class,'ant-notification-notice-message')]"
    toast_alert_title = "//nz-notification//div[contains(@class,'ant-notification-notice-description')]/div"
    toast_alert_message = "//nz-notification//div[contains(@class,'ant-notification-notice-message')]/div"
    toast_alert_close_btn = "//nz-notification//div[contains(@class,'ant-notification-notice')]/a"

class NavigationMenuLocators(object):
    # Sidebar Navigation menu items
    dashboard_navlink = "//ng-list-item-content/a[.//span[contains(text(),'Dashboard')]]"
    onboarding_navlink = "//ng-list-item-content/a[.//span[contains(text(),'Onboarding')]]"
    wakala_support_navlink = "//ng-list-item-content/a[.//span[contains(text(),'Wakala Support')]]"
    wakala_tools_navlink = "//ng-list-item-content/a[.//span[contains(text(),'Wakala Tools')]]"
    approvals_navlink = "//ng-list-item-content/a[.//span[contains(text(),'Approvals')]]"
    workflows_navlink = "//ng-list-item-content/a[.//span[contains(text(),'Workflows')]]"
    configs_navlink = "//ng-list-item-content/a[.//span[contains(text(),'Configurations')]]"
    user_mngmnt_navlink = "//ng-list-item-content/a[.//span[contains(text(),'User Management')]]"
    logout_button = "//nz-sider//app-side-bar//div[@id='logout']/button"
    # Navbar menu items
    notifications_icon = "//nz-header//button[.//*[contains(@class,'fa-bell')]]"
    user_profile_section = "//nz-header//div//span[contains(@class,'ant-dropdown-trigger')]"
    user_profile_menu = "//div[@class='cdk-overlay-container']//ul"
    edit_profile_button = "//div[@class='cdk-overlay-pane']/div[contains(@class,'mat-menu-panel')]/div[@class='mat-menu-content']/button[1]"
    change_password_button = "//div[@class='cdk-overlay-pane']/div[contains(@class,'mat-menu-panel')]/div[@class='mat-menu-content']/button[2]"
    logout_navlink = "//div[@class='cdk-overlay-container']//ul//li"
    # Section top navigations
    wakala_navlink = "//app-header-tabs//button[contains(text(),'Wakala')]"
    find_transaction_navlink = "//app-header-tabs//button[contains(text(),'Find Transaction')]"
    reported_issues_navlink = "//app-header-tabs//button[contains(text(),'Reported Issues')]"
    sit_visits_navlink = "//app-header-tabs//button[contains(text(),'Site Visits')]"
    # Section bottom navigations
    statistics_navlink = "//nz-content//button[.//span[contains(text(),'Statistics')]]"
    agent_commission_navlink = "//nz-content//button[.//span[contains(text(),'Agent Commission')]]"
    
    
class DashboardLocators(object):
    # Dashboard page (https://test-portal.ekenya.co.ke/kentapay-admin-portal/dashboard/kenta-pay)
    dashboard_page_header = "//nz-content//div[@class='page-title']"
    dashboard_section = "//app-kenta-dashboard"
    dashboard_stat_cards = "//app-kenta-dashboard/app-dashboard-cards"
    dashboard_pie_chart = "//app-kenta-dashboard/div[@class='charts-data']//app-pie-chart-dash"
    dashboard_transactions_chart = "//app-kenta-dashboard/div[@class='charts-data']//app-transactions-dash"
    dashboard_total_trans_chart = "//app-kenta-dashboard/div[@class='charts-data']//app-total-trans-dash"
    dashboard_merchant_chart = "//app-kenta-dashboard/div[@class='charts-data']//app-merchant-stats"
    