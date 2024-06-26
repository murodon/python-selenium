import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

class ChromeInstance:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = '/opt/headless-chromium'
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--single-process")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1280x1696")
        self.options.add_argument("--disable-application-cache")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--hide-scrollbars")
        self.options.add_argument("--enable-logging")
        self.options.add_argument("--log-level=0")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--homedir=/tmp")

        self.driver = webdriver.Chrome(
            executable_path="/opt/chromedriver",
            options = self.options
        )
        
def lambda_handler(event, context):
    # call chrome_headless instance.
    chrome = ChromeInstance()

    try:
        if chrome.driver:
            # Googleにアクセスして検索
            chrome.driver.get("https://www.google.com")
            search_box = chrome.driver.find_element(By.NAME, "q")
            search_box.send_keys('Selenium')
            search_box.submit()

            title = chrome.driver.title
            print(title)

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "title: " + title
                }),
            }

    except Exception as e:
        print(f"処理中にエラーが発生しました: {e}")

    finally:
        if chrome.driver:
            chrome.driver.quit()
