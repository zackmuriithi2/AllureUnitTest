### File for utility functions used all around the program ###
import os, json, random, allure, requests, base64, unittest, inspect, string
from itertools import repeat
from dotenv import load_dotenv
load_dotenv()
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement 
from allure_commons.types import LabelType
from allure_commons.model2 import Status
from allure_commons.model2 import StatusDetails
from allure_commons.utils import SafeFormatter, format_exception, format_traceback, md5

ALLURE_DESCRIPTION_MARK = 'allure_description'
ALLURE_DESCRIPTION_HTML_MARK = 'allure_description_html'
ALLURE_LABEL_MARK = 'allure_label'
ALLURE_LINK_MARK = 'allure_link'
ALLURE_UNIQUE_LABELS = [
    LabelType.SEVERITY,
    LabelType.FRAMEWORK,
    LabelType.HOST,
    LabelType.SUITE,
    LabelType.PARENT_SUITE,
    LabelType.SUB_SUITE
]

MARK_NAMES_TO_IGNORE = {
    "usefixtures",
    "filterwarnings",
    "skip",
    "skipif",
    "xfail",
    "parametrize",
}

class Utilities:
  data = None
  
  def __init__(self):
    self.data = self.load_data(f"{os.getcwd()}/data/data.json")
    self.host = os.getenv('ALLURE_HOST', 'http://localhost:5050/allure-docker-service')

  # Utilities for data generation and loading
  def load_data(self, file: str):
    with open(file, 'r') as read_file:
      self.data = json.load(read_file)
      return self.data

  def generate_random_number(self, digit_count: int):
    if digit_count <= 0:
      raise ValueError("Digit count must be a positive integer.")
    lower_bound = 10 ** (digit_count - 1)
    upper_bound = 10 ** digit_count - 1
    return random.randint(lower_bound, upper_bound)
  
  def generate_random_letters(self, letter_count: int):
    """
    Generates a random alphabetical string of a specified length.

    Args:
      letter_count (int): The desired length of the string.

    Returns:
      str: A random string consisting of uppercase and lowercase alphabetical characters.
    """
    if letter_count <= 0:
      raise ValueError('Letter count should be at least 1')
    letters = string.ascii_letters
    random_string = ''.join(random.choice(letters) for _ in range(letter_count))
    return random_string

  def generate_random_fullname(self, name_count: int):
    match name_count:
      case 1:
        return self.get_random_name(first_name = True)
      case 2:
        return f"{self.get_random_name(first_name=True)} {self.get_random_name(last_name=True)}"
      case 3:
        return f"{self.get_random_name(first_name=True)} {self.get_random_name(middle_name=True)} {self.get_random_name(last_name=True)}"
      case _:
        return ValueError("Name count must be a positive integer between 1, 2 and 3.")

  def get_random_name(self, first_name = False, middle_name = False, last_name = False):
    name = ''
    if last_name:
      name = random.choice(self.data['names']['last_names'])
    else:
      name = random.choice(self.data['names']['first_names'])
    return name
  
  def generate_description(self):
    return random.choice(self.data.descriptions)
  
  def get_upload_file(file_name: str):
    return f"{os.getcwd()}/data/{file_name}"
  
  def randomize_browser(self):
    return random.choice(self.data['browsers'])
  
  # Utilities for sending data to server
  def post_test_generator(self, project_id: str = os.getenv('ALLURE_PROJECT_ID'), session: requests.Session = None):
    if session is None:
      response = requests.request("GET", f"{self.host}/projects/{project_id}", verify=False)
    else:
      response = session.get(f"{self.host}/projects/{project_id}")
    if response.status_code == 200 and response.json().get('data').get('project'):
      print(f"Project {project_id} exists, sending data to Allure server...")
      self.send_data(session=session, project_id=project_id)
    else:
      print(f"{response.json().get('meta_data').get('message')}")
      print("Allure server is not available or project does not exist.")
      try:
        self.create_project(project_id, session=session)
      except Exception as e:
        print(f"Failed to create project: {e}")
        return
      self.post_test_generator(project_id=project_id, session=session) # Recurse the function to retry sending results
  
  def create_project(self, project_name: str, session: requests.Session = None):
    if session is None:
      response = requests.request(
        "POST",
        f"{self.host}/projects",
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"id": project_name}),
        verify=False
      )
    else:
      header = {'Content-Type': 'application/json', 'X-CSRF-TOKEN': session.cookies.get('csrf_access_token')}
      response = session.post(f"{self.host}/projects", headers=header, data=json.dumps({"id": project_name}), verify=False)
    if response.status_code == 201:
      print(f"{response.json().get('meta_data').get('message')}")
    else:
      if response.status_code == 400:
        print(f"{response.json().get("meta_data").get("message")}. 400 Bad Request.")
      else:
        print(f"{response.json().get('meta_data').get('message')}")
   
  def send_data(self, project_id: str = os.getenv('ALLURE_PROJECT_ID'), session: requests.Session = None):
    allure_results_dir = os.getenv('ALLURE_RESULTS_DIR', 'allure-results')
    results = []
    for filename in os.listdir(allure_results_dir):
      file_path = os.path.join(allure_results_dir, filename)
      if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
          content = f.read()
          content_base64 = base64.b64encode(content).decode('utf-8')
          results.append({ "file_name": filename, "content_base64": content_base64 })
        f.close()
    request_body = { "results": results }
    json_data = json.dumps(request_body)
    
    if session is None:
      response = requests.post(
        f"{self.host}/send-results?project_id={project_id}", headers={'Content-type': 'application/json'}, data=json_data, verify=False
      )
    else:
      headers = {
        'Content-type': 'application/json',
        'X-CSRF-TOKEN': session.cookies.get('csrf_access_token')
      }
      ssl_verify = os.getenv('HTTPS_ENABLED', 'false').lower() == 'true' or os.getenv('HTTPS_ENABLED', '1') == '1'
      response = session.post(f"{self.host}/send-results?project_id={project_id}", headers=headers, data=json_data, verify=ssl_verify)
      
    if response.status_code == 200 or response.status_code == 201:
      print(response.json().get("meta_data").get("message"))
      self.generate_report(project_id=project_id, session=session)
    else:
      print(f"Failed to send data: {response.status_code} - {response.text}")
        
  def generate_report(self, project_id: str = os.getenv('ALLURE_PROJECT_ID'), session: requests.Session = None):
    execution_name = os.getenv('EXECUTION_NAME', 'Python Functinal Tests')
    execution_from = os.getenv('USER', 'Local Machine')
    execution_type = os.getenv('EXECUTION_TYPE', 'UnitTest')
    if session is None:
      report = requests.request(
        "GET",
        f"{self.host}/generate-report?project_id={project_id}&execution_name={execution_name}&execution_from={execution_from}&execution_type={execution_type}",
        headers={'accept': '*/*'},
        verify=False
      )
    else:
      headers = {
        'Content-type': 'application/json',
        'X-CSRF-TOKEN': session.cookies.get('csrf_access_token')
      }
      ssl_verify = os.getenv('HTTPS_ENABLED', 'false').lower() == 'true' or os.getenv('HTTPS_ENABLED', '1') == '1'
      report = session.get(
        f"{self.host}/generate-report?project_id={project_id}&execution_name={execution_name}&execution_from={execution_from}&execution_type={execution_type}",
        headers=headers,
        verify=ssl_verify
      )
    if report.status_code == 200:
      print(f"{report.json().get('meta_data').get('message')}")
    else:
      print(f"{report.json().get('meta_data').get('message')}")
  

### Allure test report utilities
def allure_title(test):
  return getattr(
    getattr(test, "__allure_display_name__", None),
    "__call__",
    None
  ) or getattr(test, "__allure_display_name__", None)

def allure_description(test):
  description = get_marker_value(test, ALLURE_DESCRIPTION_MARK)
  if description:
    return description
  if isinstance(test, unittest.TestCase):
    method = getattr(test, test._testMethodName, None)
    if method:
      return inspect.getdoc(method)
  elif inspect.isfunction(test):
    return inspect.getdoc(test)
  return None

def allure_description_html(test):
  return get_marker_value(test, ALLURE_DESCRIPTION_HTML_MARK)

def allure_label(test, label):
  """ Uses attributes or decorators to set labels"""
  labels = []
  if hasattr(test, '__allure_labels__'):
    for ltype, lval in getattr(test, '__allure_labels__', []):
      if ltype == label:
        labels.append(lval)
  return labels

def allure_labels(test):
  unique_labels = dict()
  labels = set()
  if hasattr(test, '__allure_labels__'):
    for label_type, arg in getattr(test, '__allure_labels__', []):
      if label_type in ALLURE_UNIQUE_LABELS:
        if label_type not in unique_labels:
          unique_labels[label_type] = arg
      else:
        labels.add((label_type, arg))
  for k, v in unique_labels.items():
    labels.add((k, v))
  return labels

def allure_links(test):
  if hasattr(test, '__allure_links__'):
    for link_type, url, name in getattr(test, '__allure_links__', []):
      yield (link_type, url, name)

def format_allure_link(config, url, link_type):
  pattern = dict(getattr(config, 'allure_link_pattern', {})).get(link_type, '{}')
  return pattern.format(url)

def unittest_markers(test):
  # Not applicable in unittest; could use custom attributes
  if hasattr(test, '__allure_tags__'):
    for tag in getattr(test, '__allure_tags__', []):
      if should_convert_mark_to_tag(tag):
        yield tag

def should_convert_mark_to_tag(mark):
  return mark not in MARK_NAMES_TO_IGNORE

def allure_package(test):
  return ParsedUnittestId(test).package

def allure_name(test, parameters, param_id=None):
  if isinstance(test, unittest.TestCase):
    name = test._testMethodName
  elif inspect.isfunction(test):
    name = test.__name__
  else:
    name = str(test)
  title = allure_title(test)
  param_id_kwargs = {}
  if param_id:
    if isinstance(param_id, str) and param_id.isascii():
      param_id = param_id.encode().decode("unicode-escape")
    param_id_kwargs["param_id"] = param_id
  # parameters: dict
  return SafeFormatter().format(
    title,
    **{**param_id_kwargs, **parameters}
  ) if title else name

def allure_full_name(test):
  nodeid = ParsedUnittestId(test)
  class_part = ("." + ".".join(nodeid.class_names)) if nodeid.class_names else ""
  test_name = nodeid.test_function
  full_name = f"{nodeid.package}{class_part}#{test_name}"
  return full_name

def allure_title_path(test):
  nodeid = ParsedUnittestId(test)
  return list(
    filter(None, [*nodeid.path_segments, *nodeid.class_names]),
  )

def allure_suite_labels(test):
  nodeid = ParsedUnittestId(test)
  default_suite_labels = {
    LabelType.PARENT_SUITE: nodeid.parent_package,
    LabelType.SUITE: nodeid.module,
    LabelType.SUB_SUITE: " > ".join(nodeid.class_names),
  }
  existing_labels = dict(allure_labels(test))
  resolved_default_suite_labels = []
  for label, value in default_suite_labels.items():
    if label not in existing_labels and value:
      resolved_default_suite_labels.append((label, value))
  return resolved_default_suite_labels

def get_outcome_status(outcome):
  """ Args:
    outcome: unittest.TestResult outcome or exception info 
  """
  exception = getattr(outcome, 'exception', None)
  return get_status(exception)

def get_outcome_status_details(outcome):
  exception_type = getattr(outcome, 'exception_type', None)
  exception = getattr(outcome, 'exception', None)
  exception_traceback = getattr(outcome, 'exception_traceback', None)
  return get_status_details(exception_type, exception, exception_traceback)

def get_status(exception):
  """
  Returns whether the test failed, passed, was skipped or is broken. Only AssertionErrors return failed, any other error or exception is considered a broken test. If no exception or error, then the test passed.

  Args:
    exception (Exception | Error | Any): The exception from the test outcome

  Returns:
    str : One of either 'passed', 'failed', 'skipped' or 'broken'
  """
  if exception:
    if isinstance(exception, AssertionError):
      return Status.FAILED
    elif isinstance(exception, unittest.SkipTest):
      return Status.SKIPPED
    return Status.BROKEN
  else:
    return Status.PASSED

def get_status_details(exception_type, exception, exception_traceback):
  message = format_exception(exception_type, exception)
  trace = format_traceback(exception_traceback)
  return StatusDetails(message=message, trace=trace) if message or trace else None

def get_history_id(full_name, parameters, original_values):
  """
  Args:
    parameters list[{name: str, value: str, excluded: boolean}]: list of named objects with .name, .value, .excluded
  """
  return md5(
    full_name,
    *(original_values.get(p.name, p.value) for p in sorted(filter(
        lambda p: not getattr(p, 'excluded', False),
        parameters
      ), key=lambda p: p.name)
    )
  )
def ensure_len(value, min_length, fill_value=None):
  yield from value
  yield from repeat(fill_value, min_length - len(value))

def get_marker_value(test, keyword):
  """ Try to get from attribute directly (e.g., set by allure.dynamic or decorators like `@allure.*` )"""
  value = getattr(test, keyword, None)
  if value:
    return value
  # Try to get from method (for unittest.TestCase)
  if isinstance(test, unittest.TestCase):
    method = getattr(test, test._testMethodName, None)
    if method:
      value = getattr(method, keyword, None)
      if value:
        return value
  # Try to get from function (for plain functions)
  if inspect.isfunction(test):
    value = getattr(test, keyword, None)
    if value:
      return value
  # Try to get from class (for unittest.TestCase)
  if isinstance(test, unittest.TestCase):
    cls = test.__class__
    value = getattr(cls, keyword, None)
    if value:
      return value
  # If nothing found, just give up
  return None
    
    
class ParsedUnittestId:
  """ Helper to parse test id for unittest """
  def __init__(self, test):
    # test.id() returns 'package.module.ClassName.test_method'
    if hasattr(test, 'id'):
      test_id = test.id()
      parts = test_id.split('.')
      if len(parts) >= 3:
        self.package = '.'.join(parts[:-3])
        self.module = parts[-3]
        self.class_names = [parts[-2]]
        self.test_function = parts[-1]
        self.path_segments = self.package.split('.') + [self.module + '.py']
        self.parent_package = self.package
        self.filepath = '/'.join(self.path_segments)
      elif len(parts) == 2:
        self.package = ''
        self.module = parts[0]
        self.class_names = []
        self.test_function = parts[1]
        self.path_segments = [self.module + '.py']
        self.parent_package = ''
        self.filepath = self.module + '.py'
      else:
        self.package = ''
        self.module = ''
        self.class_names = []
        self.test_function = test_id
        self.path_segments = []
        self.parent_package = ''
        self.filepath = ''
    elif inspect.isfunction(test):
      self.package = test.__module__
      self.module = test.__module__.split('.')[-1]
      self.class_names = []
      self.test_function = test.__name__
      self.path_segments = self.package.split('.') + [self.module + '.py']
      self.parent_package = '.'.join(self.package.split('.')[:-1])
      self.filepath = '/'.join(self.path_segments)
    else:
      self.package = ''
      self.module = ''
      self.class_names = []
      self.test_function = str(test)
      self.path_segments = []
      self.parent_package = ''
      self.filepath = ''