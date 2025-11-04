import allure_commons
from modules.Utilities import (
    ALLURE_DESCRIPTION_MARK, ALLURE_DESCRIPTION_HTML_MARK,
    ALLURE_LABEL_MARK, ALLURE_LINK_MARK, format_allure_link
)

class AllureTitleHelper:
    @allure_commons.hookimpl
    def decorate_as_title(self, test_title):
        def decorator(func):
            func.__allure_display_name__ = test_title
            return func
        return decorator

class AllureTestHelper:
    def __init__(self, config):
        self.config = config

    @allure_commons.hookimpl
    def decorate_as_description(self, test_description):
        def decorator(func):
            setattr(func, ALLURE_DESCRIPTION_MARK, test_description)
            return func
        return decorator

    @allure_commons.hookimpl
    def decorate_as_description_html(self, test_description_html):
        def decorator(func):
            setattr(func, ALLURE_DESCRIPTION_HTML_MARK, test_description_html)
            return func
        return decorator

    @allure_commons.hookimpl
    def decorate_as_label(self, label_type, labels):
        def decorator(func):
            if not hasattr(func, '__allure_labels__'):
                func.__allure_labels__ = []
            for label in labels:
                func.__allure_labels__.append((label_type, label))
            return func
        return decorator

    @allure_commons.hookimpl
    def decorate_as_link(self, url, link_type, name):
      def decorator(func):
        if not hasattr(func, '__allure_links__'):
          func.__allure_links__ = []
        link_url = format_allure_link(self.config, url, link_type)
        func.__allure_links__.append((link_type, link_url, link_url if name is None else name))
        return func
      return decorator