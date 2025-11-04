import os, json, requests
from dotenv import load_dotenv

load_dotenv()

class ServerAuth():
  server: str = None
  username: str = None
  password: str = None
  session: requests.Session = None
  ssl_verify: bool = False
  csrf_access_token: str = None
  
  def __init__(self):
    self.server = os.getenv('ALLURE_HOST')
    self.username = os.getenv('ALLURE_USER', 'admin')
    self.password = os.getenv('ALLURE_PASSWORD', 'admin')
    if os.getenv('HTTPS_ENABLED') == '1' or os.getenv('HTTPS_ENABLED').lower() == 'true':
      self.ssl_verify = True
    self.session = requests.Session()
    
  def get_auth_body(self):
    credentials_body = {
      "username": self.username,
      "password": self.password
    }
    return json.dumps(credentials_body)
  
  def login(self):
    # if ssl_verification is not None:
    #   self.ssl_verify = ssl_verification
    headers = {'Content-type': 'application/json', 'accept': '*/*'}
    response = self.session.post(f'{self.server}/login', headers=headers, data=self.get_auth_body(), verify=self.ssl_verify)
    if response.status_code == 200:
      self.csrf_access_token = self.session.cookies.get('csrf_access_token')
      print(f"{response.json().get('meta_data').get('message')}")
    else:
      raise Exception(f"Login failed with status code {response.status_code}: {response.text}")
      
  def get_csrf_token(self):
    if self.csrf_access_token is None:
      raise Exception("CSRF token is not set. Please login first.")
    return self.csrf_access_token
  
  def get_session(self):
    if self.csrf_access_token is None:
      self.login()
    if self.session is None:
      raise Exception("Session is not initialized. Please login again.")
    return self.session
  
  def logout(self, session: requests.Session = None):
    headers = {'X-CSRF-TOKEN': self.get_csrf_token()}
    if session is not None:
      headers = {'X-CSRF-TOKEN': session.cookies.get('csrf_access_token')}
    response = self.session.delete(f'{self.server}/logout', headers=headers, verify=self.ssl_verify)
    if response.status_code == 200:
      self.csrf_access_token = None
      print(f"{response.json().get('meta_data').get('message')}")
    else:
      raise Exception(f"Logout failed with status code {response.status_code}: {response.text}")