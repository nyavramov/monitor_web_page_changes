import smtplib, ssl
from selenium import webdriver
from PIL import Image
from io import BytesIO
import time
import imagehash

HASH_SIZE = 128
MAX_HASH_DIFFERENCE = 65536

class Email_Client:

    def __init__(self, sender_email, password):
        self.sender_email = sender_email
        self.password = password

        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        
    def send_email(self, receiver_email, message):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message)

class Chrome_Driver:

    def __init__(self, executable_path):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--test-type")
        self.driver = webdriver.Chrome(chrome_options=self.options, executable_path=executable_path)
        
    def open_page(self, url, scroll_percent):
        divider = (100 / scroll_percent)
        self.driver.get(url)
        self.driver.execute_script("document.body.style.zoom='80%'")
        self.driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight / {divider});")
        time.sleep(2)

    def close(self):
        self.driver.close()

    def screenshot_page(self):
        page_screenshot = self.driver.get_screenshot_as_png()
        page_screenshot = Image.open(BytesIO(page_screenshot))
        return page_screenshot

    def display_screenshot(self, page_screenshot):
        page_screenshot.show()

class Change_Monitor:

    def __init__(self, Chrome_Driver, Email_Client):
        self.driver = Chrome_Driver
        self.client = Email_Client

    def calculate_hash(self, page_screenshot):
        return imagehash.phash(page_screenshot, hash_size=HASH_SIZE)

    def get_hash_difference_percent(self, old_screenshot, new_screenshot):
        old_hash = self.calculate_hash(old_screenshot)
        new_hash  = self.calculate_hash(new_screenshot)
        difference = old_hash - new_hash
        percent_difference = ( difference / MAX_HASH_DIFFERENCE ) * 100
        print(percent_difference)
        return percent_difference

    def send_change_alert(self, url):
        self.client.send_email("nikolay.test91@gmail.com", f"Change detected at {url}")

    def check_page_for_changes(self, url, check_interval=60, scroll_percent=5):
        old_screenshot = None
        new_screenshot = None

        while True:
            self.driver.open_page(url, scroll_percent)

            if old_screenshot == None:
                old_screenshot = self.driver.screenshot_page()
            else:
                new_screenshot = self.driver.screenshot_page()
                percent_different = self.get_hash_difference_percent(old_screenshot, new_screenshot)

                if percent_different > 1:
                    self.send_change_alert(url)
                print(percent_different)
            time.sleep(check_interval)

def main():
    EMAIL = ""
    PASSWORD = ""
    URL_TO_MONITOR = ""
    CHROME_DRIVER_LOCATION = ""
    driver = Chrome_Driver(CHROME_DRIVER_LOCATION)
    email_client = Email_Client(EMAIL, PASSWORD)
    monitor = Change_Monitor(driver, email_client)
    monitor.check_page_for_changes(URL_TO_MONITOR, 30, 5)
    
main()
