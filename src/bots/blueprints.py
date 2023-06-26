from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv.main import load_dotenv
from time import sleep
import pickle


# This is the blueprint for the Linkedin bot
# This class contains the basic methods required to run the bot
# This class is to be inherited by the bot linked class
# The child class should override the run method, in which the main logic of the bot should be written
class LinkedinBotBlueprint:

    def __init__(self, wait_time=10):

        # install chrome driver if not found
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # set the wait time
        # this is the maximum time the bot will wait for an element to load before it throws an error
        self.wait_time = wait_time

        # get the login credentials from the environment variables
        load_dotenv()
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")

        # if any of the credentials are not found, exit the program
        if self.email == None or self.password == None:
            print("Login credentials for Linkedin missing or not found")
            exit(1)

    # login to the linkedin account
    def login(self):
        # go to the login page
        self.driver.get("https://www.linkedin.com/login")
        self.driver.maximize_window()

        # load the cookies if they exist
        print("Looking for cookies...")
        try:

            # check if the cookies folder exists
            if not os.path.exists("./cookies"):
                os.mkdir("./cookies")

            cookies = pickle.load(open("./cookies/cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            print("Cookies loaded")
        except:
            print("No cookies found, you may need to complete a securty check...")
            pass

        # wait for the page to load
        try:
            username = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            button = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
            )
        except:
            print("Login page not loaded")
            exit(1)
        
        # enter the credentials
        username.send_keys(self.email)
        password.send_keys(self.password)

        # click the login button
        button.click()

        # check if there is a security check
        # if there is, wait for it to complete and re-try logging in
        try:
            element = WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            if element.text == "Let's do a quick security check":
                print("Security check detected, plase solve it. The bot will collect the cookies and use them to avoid detection next time...")

                # wait for the user to complete the security check
                sleep(self.wait_time)

                # check if the cookies folder exists
                if not os.path.exists("./cookies"):
                    os.mkdir("./cookies")
        except:
            pass

        # dump the cookies to a file
        pickle.dump(self.driver.get_cookies() , open("./cookies/cookies.pkl","wb"))
        print("Cookies saved")

    # close the browser
    def close(self):
        self.driver.quit()
    
    # run the bot
    # This method is to be overridden by the child class
    # This method should contain the main logic of the bot
    def run(self):
        pass

    # run the bot
    def start(self):
        self.login()
        self.run()
        self.close()