# Allure-Unittest POM Template

Hello there, QA Test Automator!

This is your guiding template to creating your Allure reporting framework for your unittest scripts. Follow this structure and do not edit any unnecessary files unless you must.

## Usage

Once you clone this repo, immediately duplicate (checkout) to a new branch using <script>git checkout -b <name></script> before you do any alterations to the branch.

Do not push or merge to the master branch except only to update the template and after a code review of your merge request.

This is only a reference guide for our Allure-Unittest POM structure. Do not mess with it; you will misguide a lot of people.

### Requirements

To run this system, you are required to have at least the following:
- An allure-reports server which you can get from the container `docker.io/frankescobar/allure-docker-service` or simply run it from the docker compose file in the project root folder using `docker compose -f docker-compose-dev.yaml up -d` command
- Python language(at least version 3.10) an dthe requirements listed in the `requirements.txt` file
- At least one browser installed, preferrable Chrome or Firefox
The docker image is used for storing and serving the reports locally, and if provided, can be substituted with a hosted service of the same container image. Just make sure to update your `ALLURE_HOST` value in the `.env`.

## Editing Files and Folders

There are files you are not supposed to touch...AT ALL. Then there are those you can edit as fits your needs. THen there are those you should add. Lets see all these;

### Files & Folders Not To Be Touched
The following folders and files should not be touched at all unless when updating the template:

- modules
- Src
  - TestBase
    - WebDriverSetup.py
- .gitignore
- .gitlab-ci.yml
- requirements.txt

As for the <b>WebDriverSetup.py</b> file, you are allowed to switch between the remote drivers and local(Chrome, Firefox) driver by commenting in and out the different __init__ functions. The first, obviously bigger init function is for opening the remote webdrivers while the next shorter init function is for local webdriver.
You are also permitted to change the name(URL) of the remote webdrivers in case you are using custom Selenium Grid containers.

### Files & Folders To Be Edited
The following files and folders may be edited according to the project to ensure smooth running of the scripts:

- Src
  - PageObject
    - BasePage.py (Edit the base URL to fit your project, add or comment out any common, cross-page functionalities)
    - Locators.py (You will need to edit your locators for your elements. Follow guidelines.)
- Test
  - TestSuite
    - TestRunner.py (Change result folder, tests being loaded into the suite and maybe report name if necessary. Leave the rest alone, please )
- .env.example (Show what is expected in your .env file in case we need to create one for your branch)
- README.md (Tell us something meaningful about your branch, surely)

Take care when editing though; one small mistake and you'll be debugging for hours!

### Files & Folders To Be Added
These folders and files are to be or will be added:

- logs This is where your webdriver log files will be put. It will be automatically created if not existing at runtime.
- data
  - data.json (This are any data files to be parsed or uploaded for the tests to run)
- Src
  - PageObject
    - Pages
      - WebPage.py (Here is where you add all your web page finders and getters which will be used by the test scripts.)
- Test
  - Scripts
    - test_WebPage.py (Here is where you add all your test scripts to do actions and test functionalities. Your test cases are here.)
- .env (Your environment variables will be stored in this file and loaded into the scripts when required. Get the template from the <i>.env.example</i> file)

As you might have noticed, most of your work will be adding files into the Pages folder, adding test files into the Scripts folder and loading the tests into the TestRunner file. The principle is KISS: Keep It Simple and Smart/Safe.

## Support
In case you need help with aything, feel free to reach out to the repo maintainers via email or create an issue and it will be tracked and resolved ASAP.

## Roadmap
The plan is to make this template as robust as possible to handle most of the repetitive test automation work leaving the user with only script writing.
Also look forward to customizing the template for the report as we see it now.