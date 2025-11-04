### Test Runner to run all the test scripts required ###

import sys, os, shutil, unittest
from dotenv import load_dotenv
sys.path.append(os.getcwd())
load_dotenv()
from modules.Utilities import Utilities
from modules.ServerHelper import ServerAuth
from pathlib import Path
from Test.Scripts.test_User_Auth import Login_Logout_Tests
from Test.Scripts.test_Dashboard import Dashboard_Test
import modules.Reporter as testRunner
        

if __name__ == "__main__":
    test_suite = unittest.defaultTestLoader.loadTestsFromTestCase(Login_Logout_Tests)
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Dashboard_Test))
    result_folder = 'allure-results'
    report_source_path = Path(result_folder).absolute()
    if report_source_path.is_dir() and os.getenv('CLEAN_REPORTS', 'true').lower() == 'true':
        shutil.rmtree(report_source_path)
    testRunner.run_with_allure(test_suite, report_source_path, clean=True)
    if os.getenv('SECURE_LOGIN').lower() == 'true':
        user = ServerAuth()
        session = user.get_session()
        Utilities().post_test_generator(session=session)
        user.logout()
    else:
        Utilities().post_test_generator()