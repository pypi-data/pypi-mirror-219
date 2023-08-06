import abc
from tempfile import mkdtemp

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from dynamodb.dynamodb import DynamoDB


class AbstractAutomation(abc.ABC):

    def __init__(self, url: str, table: str):
        self.url = url
        self.driver = self.__get_driver()
        self.db = DynamoDB(table=table)

    def __get_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        service = Service(executable_path='/opt/chromedriver')
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        chrome = webdriver.Chrome(service=service, options=options)
        return chrome
