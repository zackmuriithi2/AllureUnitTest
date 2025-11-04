import sys, os, time
sys.path.append(os.getcwd())
from modules.Utilities import Utilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, ElementNotSelectableException, ElementNotVisibleException, NoAlertPresentException, NoSuchAttributeException, UnexpectedTagNameException, TimeoutException

class BasePage:
    """Iniialize all pages and and the webdriver, and provide generic methods for visiting routes and accessing elements.
    """
    DEFAULT_WAIT_TIMER = 5
    driver = None
    data = None
    text_elements = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    
    
    def __init__(self, driver):
      self.driver = driver
      utilities = Utilities()
      self.data = utilities.data
      self.base_url = self.data['base_url']

    def find_element(self, *locator):
      """A function to find the element in the DOM given the locator strategy. It incorporates explicit wait methods using WebDriverWait and expected_conditions to check whether an element is:
        1. Present in the DOM
        2. Visible (can be seen)
        3. If it is a textual element, whether the text inside is loaded.
      
      Args:
        *locator (tuple): this is a pair containing the locator method and string that will be used to locate the element in the DOM. An example is (By.ID, 'username')

      Returns:
        element (WebElement): if the element was found fully loaded and active, it will be returned.
      """
      try:
        element = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(locator), 'Element not found in DOM')
        WebDriverWait(self.driver, 20).until(EC.visibility_of(element), 'Element not visible in DOM')
        if element.tag_name in self.text_elements:
          WebDriverWait(self.driver, 10).until(lambda driver: element.text.strip() != '', 'Element has no text')
      except TimeoutException as time_out_error:
        func_name = sys._getframe(1).f_code.co_name
        raise AssertionError(f"{func_name} - {time_out_error.msg}") from time_out_error
      except (ElementClickInterceptedException, ElementNotInteractableException, ElementNotSelectableException, ElementNotVisibleException, NoAlertPresentException, NoSuchAttributeException, UnexpectedTagNameException) as test_case_error:
        raise AssertionError(f"{test_case_error.msg}") from test_case_error
      return element
    
    def find_elements(self, *locator):
      """A function to finds several elements in the DOM given the locator strategy. It incorporates explicit wait methods using WebDriverWait and expected_conditions to check whether an element is:
        1. Present in the DOM
        2. Visible (can be seen)
        3. If they are textual elements, whether the text inside is loaded.
      
      Args:
        *locator (tuple): this is a pair containing the locator method and string that will be used to locate the elements in the DOM. An example is (By.ID, 'username')

      Returns:
        elements (list): if the elements were found fully loaded and active, they will be returned as a list.
      """
      elements = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(locator), 'Element not found in DOM')
      for element in elements:
        WebDriverWait(self.driver, 20).until(EC.visibility_of(element), f'Element {element.tag_name} not visible in DOM')
        if element.tag_name in self.text_elements:
          WebDriverWait(self.driver, 10).until(lambda driver: element.text.strip() != '', f'Element {element} has no text')
      return elements
      

    def visit(self, url):
      """Appends the url to the base url then navigates to that page.

      Args:
        url (string): the url extension of the resource or page to be appended tp the base url
      """
      self.driver.get(self.base_url + url)
      
    def pause(self, sleep_timer: int = None):
      """
      Pauses the execution of scripts for some time, by default 5 seconds

      Args:
          sleep_timer (int, optional): The default sleep duration. Defaults to None.
      """
      if sleep_timer is None:
        time.sleep(self.DEFAULT_WAIT_TIMER)
      else:
        time.sleep(sleep_timer)
      
    def getCurrentPageHeader(self):
      return self.find_element(*(By.XPATH, "//nz-content//div[@class='page-title']"))
        
    # def getInputFilter(self, position: int):
    #   """Gets the input element used to filter table data in a page, usually located above the data tables, by its index.

    #   Args:
    #     position (int): the position(index) of the input element among other input filter elements.

    #   Returns:
    #     WebElement: the required filtering input element.
    #   """
    #   return self.find_element(*(By.XPATH, f"//app-custom-ngx-table//div/input[{position}]"))

    # def getDropdownFilter(self, select_ID: str):
    #   """Gets the select element used to filter table data in a page, usually located above the data tables, by its ID.

    #   Args:
    #     select_ID (str): this is the id property of the select filter element you want.

    #   Returns:
    #     Select: a dropdown select element that is used to filter the data.
    #   """
    #   return Select(self.find_element(*(By.XPATH, f"//app-custom-ngx-table//div/select[@id='{select_ID}']")))
    
    # def resultPopup(self):
    #   """Checks whether the result popup is displayed

    #   Returns:
    #     bool: True if the popup is visible, False otherwise.
    #   """
    #   return self.find_element(*(By.XPATH, PopupLocators.result_popup)).is_displayed()
    
    # def getResultStatus(self):
    #   """Get whether the result of the operation is a success or an error.

    #   Returns:
    #     bool: True if the result is a success, otherwise False (for errors)
    #   """
    #   result_classes = self.find_element(*(By.XPATH, PopupLocators.result_icon)).get_attribute('class').strip()
    #   status = False
    #   if 'swal2-success' in result_classes:
    #     status = True
    #   return status
    
    # def getResultMessage(self):
    #   """Get the resulting message from the result popup

    #   Returns:
    #     str: The message displayed on the popup
    #   """
    #   return self.find_element(*(By.XPATH,PopupLocators.result_message)).text
    
    # def getResultTitle(self):
    #   """Get the result popup's title. 

    #   Returns:
    #     str: The title of the popup, e.g. Success, Error, Failed.
    #   """
    #   return self.find_element(*(By.XPATH, PopupLocators.result_title)).text
    
    # def closeResultPopup(self):
    #   """Closes the result popup"""
    #   self.find_element(*(By.XPATH, PopupLocators.result_ok_button)).click()
