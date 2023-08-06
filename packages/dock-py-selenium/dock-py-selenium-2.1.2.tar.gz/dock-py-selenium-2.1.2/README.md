# DOCK SELENIUM

## Python only

This is a startup directory to write the selenium scripts in python along with some customization.

### Steps.
1. `pip install dock-py-selenium`
2. Create a `test.py` file in your root directory and write your test scripts.
3. Always bind any selenium script with the created instance.


## Features

1. Setting a custom wait time for the webdriver `test_instance.wait(5)`
2. Settting the number of times a test should be performed `test_instance.rerun(3, lambda: run())`
3. Getting the title of the page `test_instance.getTitle()`
4. Checking whether the button or input type submit is clickable `test_instance.checkClick("button")` or `test_instance.checkClick("input")`
5. Checking the presence of an element in a webpage `test_instance.checkElement("CLASS_NAME","container")`


<mark> Note that, this project is still experimental and hence does not support the full render wait time for any test actions. </mark>


### Example 
```
from dock_py_selenium.dock.dock import Driver, options, Keys
from selenium import webdriver

driver = webdriver.Chrome(options=options)
dock_instance = Driver(driver)

# Starting the dock instance
# This step is compulsory
dock_instance.start()

# Getting the title of the webpage
dock_instance.getTitle()

# Checking whether an element with name = username is present
dock_instance.checkElement("name", "username")

# Checking whether an element with name = fname is present & sending "John" as input
dock_instance.checkElement("name", "fname").send_keys("John")

# Checking whether an element with name = login is present & then clicking the element 
dock_instance.checkElement("name", "login").click()

# Checking the title of the webpage
dock_instance.checkTitle("Dock Selenium")
```