import os, allure_commons, unittest
from allure_commons.types import LabelType, Severity
from allure_commons.logger import AllureFileLogger
from allure_commons.utils import get_testplan
from modules.Utilities import allure_label, allure_labels, allure_full_name
from modules.Utilities import ALLURE_DESCRIPTION_MARK, ALLURE_DESCRIPTION_HTML_MARK, ALLURE_LABEL_MARK, ALLURE_LINK_MARK
from modules.AllureHelper import AllureTestHelper
from modules.AllureListener import AllureListener


def run_with_allure(test_suite: unittest.TestSuite, report_dir="allure-results", clean=False, config=None):
    """
    Run unittest test-suite with Allure reporting.
    Args:
        test_suite: A list of iterable test functions or TestSuite
        report_dir: path to folder where you would like to store the result files
        clean: whether or not to delete old result files when writing new ones
        config: configurations on how to run the tests e.g. which suite to run
    """
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    file_logger = AllureFileLogger(report_dir, clean)
    allure_commons.plugin_manager.register(file_logger)
    test_listener = AllureListener(config)
    allure_commons.plugin_manager.register(test_listener)
    # use testtestrunner for terminal logger
    runner = unittest.TextTestRunner(resultclass=lambda *a, **kw: test_listener)
    result = runner.run(test_suite)
    allure_commons.plugin_manager.unregister(file_logger)
    allure_commons.plugin_manager.unregister(test_listener)
    return result

def select_by_labels(tests, config):
    """
    Args:
        tests (list[unittest.TestCase | func]): iterable of unittest.TestCase or test functions
    """
    arg_labels = set()
    if hasattr(config, "allure_epics"):
        arg_labels |= set(config.allure_epics)
    if hasattr(config, "allure_features"):
        arg_labels |= set(config.allure_features)
    if hasattr(config, "allure_stories"):
        arg_labels |= set(config.allure_stories)
    if hasattr(config, "allure_ids"):
        arg_labels |= set(config.allure_ids)
    if hasattr(config, "allure_severities"):
        arg_labels |= set(config.allure_severities)
    if hasattr(config, "allure_labels"):
        for label in config.allure_labels:
            arg_labels |= set(label)
    if arg_labels:
        selected, deselected = [], []
        for test in tests:
            test_labels = set(allure_labels(test))
            test_severity = allure_label(test, LabelType.SEVERITY)
            if not test_severity:
                test_labels.add((LabelType.SEVERITY, Severity.NORMAL))
            if arg_labels & test_labels:
                selected.append(test)
            else:
                deselected.append(test)
        return selected, deselected
    else:
        return tests, []

def select_by_testcase(tests, config):
    planned_tests = get_testplan()
    is_inversion = getattr(config, "inversion", False)
    if planned_tests:
        def is_planned(test):
            allure_ids = allure_label(test, LabelType.ID)
            allure_string_ids = list(map(str, allure_ids))
            for planned_item in planned_tests:
                planned_item_string_id = str(planned_item.get("id"))
                planned_item_selector = planned_item.get("selector")
                if (
                    planned_item_string_id in allure_string_ids
                    or planned_item_selector == allure_full_name(test)
                ):
                    return True if not is_inversion else False
            return False if not is_inversion else True
        selected, deselected = [], []
        for test in tests:
            selected.append(test) if is_planned(test) else deselected.append(test)
        return selected, deselected
    else:
        return tests, []

def filter_tests(test_suite: unittest.TestSuite, config):
    """
    Recursively filter tests in a unittest suite by Allure labels and testplan.
    Returns a new suite with only selected tests.
    """
    tests = []
    for test in unittest.TestSuite(test_suite):
        if isinstance(test, unittest.TestSuite):
            filtered = filter_tests(test, config)
            if filtered.countTestCases() > 0:
                tests.append(filtered)
        else:
            selected, _ = select_by_testcase([test], config)
            selected, _ = select_by_labels(selected, config)
            if selected:
                tests.extend(selected)
    return unittest.TestSuite(tests)