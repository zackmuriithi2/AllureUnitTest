
from selenium import webdriver
import os, sys, urllib3, logging, datetime
sys.path.append(os.getcwd())
from modules.Utilities import Utilities

def get_log_filename():
    logs_folder_path = f"{os.getcwd()}/logs"
    if not os.path.exists(logs_folder_path):
        os.makedirs(logs_folder_path)
        print(f"Folder '{logs_folder_path}' created.")
    else:
        print(f"Folder '{logs_folder_path}' already exists.")
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f"webdriver_logs_{timestamp}.log"

logging.basicConfig(filename=f"{os.getcwd()}/logs/{get_log_filename()}", level=logging.NOTSET, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)
 
class WebDriverSetup():
    
    driver = None
    job_platform = ''
    options=webdriver.ChromeOptions()
    options_firefox=webdriver.FirefoxOptions()
    options_edge=webdriver.EdgeOptions()
    utilities = Utilities()
    
    
    # def __init__(self):
    #     """Initialize webdriver on Selenium hub (remote)"""
    #     self.job_platform = os.environ["CI_JOB_NAME"]
    #     self.prepare_options(remote=True)
    #     match self.job_platform:
    #         case "chrome-test-job":
    #             self.driver = webdriver.Remote(command_executor='http://selenium__standalone-chrome:4444/wd/hub', options=self.options)
    #         case "firefox-test-job":
    #             self.driver = webdriver.Remote(command_executor='http://selenium__standalone-firefox:4444/wd/hub', options=self.options_firefox)
    #         case "edge-test-job":
    #             self.driver = webdriver.Remote(command_executor='http://selenium__standalone-edge:4444/wd/hub', options=self.options_edge)
    #     self._capture_logs()

    def __init__(self):
        """Initialize webdriver locally with random browser"""
        self.job_platform = self.utilities.randomize_browser()
        self.prepare_options()
        match self.job_platform:
            case "chrome":
                self.driver = webdriver.Chrome(options=self.options)
                # self._capture_logs()
            case "firefox":
                self.driver = webdriver.Firefox(options=self.options_firefox)
            case "edge-test-job":
                self.driver = webdriver.Edge(options=self.options_edge)
            
    def prepare_options(self, remote=False):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.options.add_argument('--window-size=1390,1080')
        self.options_firefox.add_argument('--window-size=1390,1080')
        self.options_edge.add_argument('--window-size=1390,1080')
        if remote:
            self.options.add_experimental_option("useAutomationExtension", False)
            self.options.add_experimental_option("excludeSwitches", ['enable-automation'])
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--headless=new")
            self.options_firefox.add_argument("--disable-gpu")
            self.options_firefox.add_argument("--headless=new")
            self.options_edge.add_argument("--disable-gpu")
            self.options_edge.add_argument("--headless=new")
