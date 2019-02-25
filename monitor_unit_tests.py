import unittest, os, warnings, re
from monitor import Email_Client, Chrome_Driver, Change_Monitor, get_dependency_name, get_credentials
from PIL import Image 
from email.mime.multipart import MIMEMultipart


class Test_Monitor(unittest.TestCase):

    def setUp(self):

        warnings.simplefilter("ignore") # Remove warnings that obscure the test results

        email, password = get_credentials()

        directory_this_script = os.path.dirname(os.path.realpath(__file__)) # Get location of where this file is located
        chrome_driver_name = get_dependency_name()
        chrome_driver_location = os.path.join(directory_this_script, "bin", chrome_driver_name) # Assume chromedriver is in same directory

        self.driver = Chrome_Driver(chrome_driver_location)
        self.email_client = Email_Client(email, password)
        self.monitor = Change_Monitor(self.driver, self.email_client)

    # Test that the hash is being computed correctly for a given test image
    def test_calculate_hash(self):

        file = open("testing/monorail_cat_hash.txt", "r")
        cat_hash = file.read()
        file.close()
        test_image = Image.open("testing/monorail_cat_test.jpg")
        
        self.assertEqual(cat_hash, str(self.monitor.calculate_hash(test_image)))

    # Make sure that the e-mail is being composed properly by matching to known, valid email message structure
    def test_prepare_message(self):

        url = "https://www.google.com"

        test_image_1 = Image.open("testing/flying_cat.jpg")
        test_image_2 = Image.open("testing/monorail_cat_test.jpg")

        prepared_message = self.monitor.prepare_message(MIMEMultipart(), test_image_1, test_image_2, url)
        
        # Regex to check for valid email header & message body
        pattern = re.compile("Content-Type: multipart/mixed; boundary=\"===============[0-9]*==\"\nMIME-Version:"
            " 1.0\nSubject: .*\nFrom: \".*\"\nTo: \".*\"\n\n--===============[0-9]*==\nContent-Type: text/plain;"
            " charset=\"us-ascii\"\nMIME-Version: 1.0\nContent-Transfer-Encoding: 7bit\n\n.*\n--===============[0-9]"
            "*==\nContent-Type: application/octet-stream\nMIME-Version: 1.0\nContent-Transfer-Encoding: base64\nContent"
            "-Disposition: attachment; filename=new_screenshot.png.*--===============[0-9]*==--", re.IGNORECASE|re.DOTALL)

        self.assertTrue(pattern.match(prepared_message))
        
        

if __name__ == '__main__':
    unittest.main()