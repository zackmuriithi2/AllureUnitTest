import unittest, sys, traceback, allure_commons
from allure_commons.reporter import AllureReporter
from allure_commons.types import LabelType, AttachmentType, ParameterMode
from allure_commons.utils import now, uuid4, represent, platform_label, host_tag, thread_tag, md5
from allure_commons.model2 import (
    TestStepResult, TestResult, TestBeforeResult,
    TestAfterResult, TestResultContainer, StatusDetails,
    Parameter, Label, Link, Status
)
from modules.Utilities import (
    allure_description, allure_description_html, allure_labels, allure_links, unittest_markers,
    allure_full_name, allure_package, allure_name, allure_title_path, allure_suite_labels,
    get_status, get_status_details, get_outcome_status, get_outcome_status_details,
    format_allure_link, get_history_id
)

class AllureListener(unittest.TestResult):
    SUITE_LABELS = {
        LabelType.PARENT_SUITE,
        LabelType.SUITE,
        LabelType.SUB_SUITE,
    }

    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.allure_logger = AllureReporter()
        self._cache = ItemCache()
        self._host = host_tag()
        self._thread = thread_tag()
        self._current_test = None

    # --- Test lifecycle hooks ---

    def startTest(self, test):
        super().startTest(test)
        uuid = self._cache.push(test)
        params = self.__get_unittest_params(test)
        test_result = TestResult(
            name=allure_name(test, params),
            uuid=uuid,
            start=now(),
        )
        test_result.fullName = allure_full_name(test)
        test_result.titlePath = [*allure_title_path(test)]
        test_result.testCaseId = md5(test_result.fullName)
        test_result.description = allure_description(test)
        test_result.descriptionHtml = allure_description_html(test)
        test_result.parameters = [
            Parameter(name=name, value=represent(value))
            for name, value in params.items()
        ]
        self.allure_logger.schedule_test(uuid, test_result)
        self._current_test = test

    def stopTest(self, test):
        super().stopTest(test)
        uuid = self._cache.pop(test)
        if uuid:
            test_result = self.allure_logger.get_test(uuid)
            if test_result.status is None:
                test_result.status = Status.PASSED
            test_result.stop = now()
            self.__finalize_test_labels_links(test, test_result)
            self.allure_logger.close_test(uuid)
        self._current_test = None

    def addSuccess(self, test):
        super().addSuccess(test)
        uuid = self._cache.get(test)
        if uuid:
            test_result = self.allure_logger.get_test(uuid)
            test_result.status = Status.PASSED

    def addFailure(self, test, err):
        super().addFailure(test, err)
        uuid = self._cache.get(test)
        if uuid:
            test_result = self.allure_logger.get_test(uuid)
            test_result.status = Status.FAILED
            self.attach_data(
                body=test.driver.get_screenshot_as_png() if hasattr(test, 'driver') else b'',
                name=f'{test_result.name} failure',
                attachment_type=AttachmentType.PNG,
                extension='png'
            )
            test_result.statusDetails = self._make_status_details(err)

    def addError(self, test, err):
        super().addError(test, err)
        uuid = self._cache.get(test)
        if uuid:
            test_result = self.allure_logger.get_test(uuid)
            test_result.status = Status.BROKEN
            self.attach_data(
                body=test.driver.get_screenshot_as_png() if hasattr(test, 'driver') else b'',
                name=f'{test_result.name} error',
                attachment_type=AttachmentType.PNG,
                extension='png'
            )
            test_result.statusDetails = self._make_status_details(err)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        uuid = self._cache.get(test)
        if uuid:
            test_result = self.allure_logger.get_test(uuid)
            test_result.status = Status.SKIPPED
            test_result.statusDetails = StatusDetails(message=str(reason))

    # --- Allure hooks and helpers ---

    @allure_commons.hookimpl
    def start_step(self, uuid, title, params):
        parameters = [Parameter(name=name, value=value) for name, value in params.items()]
        step = TestStepResult(name=title, start=now(), parameters=parameters)
        self.allure_logger.start_step(None, uuid, step)

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb):
        self.allure_logger.stop_step(uuid,
                                     stop=now(),
                                     status=get_status(exc_val),
                                     statusDetails=get_status_details(exc_type, exc_val, exc_tb))

    @allure_commons.hookimpl
    def start_fixture(self, parent_uuid, uuid, name):
        after_fixture = TestAfterResult(name=name, start=now())
        self.allure_logger.start_after_fixture(parent_uuid, uuid, after_fixture)

    @allure_commons.hookimpl
    def stop_fixture(self, parent_uuid, uuid, name, exc_type, exc_val, exc_tb):
        self.allure_logger.stop_after_fixture(uuid,
                                              stop=now(),
                                              status=get_status(exc_val),
                                              statusDetails=get_status_details(exc_type, exc_val, exc_tb))

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        self.allure_logger.attach_data(uuid4(), body, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        self.allure_logger.attach_file(uuid4(), source, name=name, attachment_type=attachment_type, extension=extension)

    @allure_commons.hookimpl
    def add_title(self, test_title):
        test_result = self._get_current_test_result()
        if test_result:
            test_result.name = test_title

    @allure_commons.hookimpl
    def add_description(self, test_description):
        test_result = self._get_current_test_result()
        if test_result:
            test_result.description = test_description

    @allure_commons.hookimpl
    def add_description_html(self, test_description_html):
        test_result = self._get_current_test_result()
        if test_result:
            test_result.descriptionHtml = test_description_html

    @allure_commons.hookimpl
    def add_link(self, url, link_type, name):
        test_result = self._get_current_test_result()
        if test_result:
            link_url = format_allure_link(self.config, url, link_type) if self.config else url
            new_link = Link(link_type, link_url, link_url if name is None else name)
            for link in test_result.links:
                if link.url == new_link.url:
                    return
            test_result.links.append(new_link)

    @allure_commons.hookimpl
    def add_label(self, label_type, labels):
        test_result = self._get_current_test_result()
        for label in labels if test_result else ():
            test_result.labels.append(Label(label_type, label))

    @allure_commons.hookimpl
    def add_parameter(self, name, value, excluded, mode: ParameterMode):
        test_result: TestResult = self._get_current_test_result()
        if not test_result:
            return
        existing_param = next(filter(lambda x: x.name == name, test_result.parameters), None)
        if existing_param:
            existing_param.value = represent(value)
        else:
            test_result.parameters.append(
                Parameter(
                    name=name,
                    value=represent(value),
                    excluded=excluded or None,
                    mode=mode.value if mode else None
                )
            )

    # --- Internal helpers ---

    def _get_current_test_result(self):
        uuid = self._cache.get(self._current_test)
        if uuid:
            return self.allure_logger.get_test(uuid)
        return None

    def _make_status_details(self, err):
        exc_type, exc_value, tb = err
        message = "".join(traceback.format_exception_only(exc_type, exc_value, show_group=True)).strip()
        trace = "".join(traceback.format_tb(tb))
        return StatusDetails(message=message, trace=trace)

    def __get_unittest_params(self, test):
        # Unittest does not natively support parametrization, but you can extend this for custom cases
        return getattr(test, '_allure_parameters', {}) if hasattr(test, '_allure_parameters') else {}

    def __finalize_test_labels_links(self, test, test_result):
        test_result.historyId = get_history_id(
            test_result.fullName,
            test_result.parameters,
            original_values=self.__get_unittest_params(test)
        )
        test_result.labels.extend([Label(name=name, value=value) for name, value in allure_labels(test)])
        test_result.labels.extend([Label(name=LabelType.TAG, value=value) for value in unittest_markers(test)])
        self.__apply_default_suites(test, test_result)
        test_result.labels.append(Label(name=LabelType.HOST, value=self._host))
        test_result.labels.append(Label(name=LabelType.THREAD, value=self._thread))
        test_result.labels.append(Label(name=LabelType.FRAMEWORK, value='unittest'))
        test_result.labels.append(Label(name=LabelType.LANGUAGE, value=platform_label()))
        test_result.labels.append(Label(name='package', value=allure_package(test)))
        test_result.links.extend([Link(link_type, url, name) for link_type, url, name in allure_links(test)])

    def __apply_default_suites(self, test, test_result):
        default_suites = allure_suite_labels(test)
        existing_suites = {
            label.name
            for label in test_result.labels
            if label.name in AllureListener.SUITE_LABELS
        }
        test_result.labels.extend(
            Label(name=name, value=value)
            for name, value in default_suites
            if name not in existing_suites
        )

class ItemCache:
    def __init__(self):
      self._items = dict()

    def get(self, _id):
      return self._items.get(id(_id))

    def push(self, _id):
      return self._items.setdefault(id(_id), uuid4())

    def pop(self, _id):
      return self._items.pop(id(_id), None)