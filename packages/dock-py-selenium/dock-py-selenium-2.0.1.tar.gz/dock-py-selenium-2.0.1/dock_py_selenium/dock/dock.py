import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Set options
options = ChromeOptions()
options.add_argument("--headless")

#driver settings
driver = webdriver.Chrome(options=options)
driver.maximize_window

class Driver:
    # Initialized with driver
    def __init__(self, driver):
        self.driver = driver

    def start(self):
        getUrl = input("Enter the url: ")
        self.driver.get(getUrl)

    # Gets the title of a webpage
    def getTitle(self):
        print(self.driver.title)
    
    # Only checks button & input of type submit
    def checkClick(self, element):
        cur_url = self.driver.current_url

        if element == "button":
            try:
                elem = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                return lambda: self._click_button(elem, cur_url)
            except NoSuchElementException as err:
                print("Exception: " + err.msg)
        elif element == "input":
            try:
                elem = self.driver.find_element(By.XPATH, "//input[@type='submit']")
                return lambda: self._click_button(elem, cur_url)
            except NoSuchElementException as err:
                print("Exception: " + err.msg)
        else:
            print("Invalid element.")

    def _click_button(self, button, cur_url):
        initial_page_source = self.driver.page_source
        button.click()
        time.sleep(5)
        updated_page_source = self.driver.page_source
        
        if initial_page_source != updated_page_source:
            print("The button is clickable.")
        else:
            print("The button is not clickable.")

    # Checks for the availability of an element in a page
    def checkElement(self,elem,i):
        match elem:
            case "ID":
                try:
                    e = self.driver.find_element(By.ID, i)
                    print("The element with ID '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case "NAME":
                try:
                    e = self.driver.find_element(By.NAME, i)
                    print("The element with name '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case "CLASS_NAME":
                try:
                    e = self.driver.find_element(By.CLASS_NAME, i)
                    print("The element with class name '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case "TAG_NAME":
                try:
                    e = self.driver.find_element(By.TAG_NAME, i)
                    print("The element with tag name '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case "LINK_TEXT":
                try:
                    e = self.driver.find_element(By.LINK_TEXT, i)
                    print("The element with link text '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case "PARTIAL_LINK_TEXT":
                try:
                    e = self.driver.find_element(By.PARTIAL_LINK_TEXT, i)
                    print("The element with partial link text '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case "CSS_SELECTOR":
                try:
                    e = self.driver.find_element(By.CSS_SELECTOR, i)
                    print("The element with CSS selector '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case "XPATH":
                try:
                    e = self.driver.find_element(By.XPATH, i)
                    print("The element with XPath '" + i + "' is available.")
                    return e
                except NoSuchElementException as err:
                    print("Exception: " + err.msg)
            
            case _:
                print("Invalid element.")

   

    # Rerun in dock for 'x' times
    def rerun(self, x, y):
        for _ in range(x):
            y()

    # Waiting time for webdriver to perform further action
    def wait(self, x):
        return WebDriverWait(self.driver, x)
