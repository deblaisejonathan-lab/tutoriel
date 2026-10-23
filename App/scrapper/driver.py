from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Driver:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_arguments("--start-maximized")

        self.options.add_argument("--headless=new")
        self.options.add_argument("--disable-gpu")  #
        self.options.add_argument("--window-size=1920,1080")
    def get_driver(self):
        """Initialise et retourne le navigateur sans s'occuper du driver."""
        driver = webdriver.Chrome(options=self.options)
        return driver


