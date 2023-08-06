# DOCK SELENIUM

## Python only

This is a startup directory to write the selenium scripts in python along with some customization.

### Steps.
1. Clone [this](https://github.com/iambstha/dockSelenium) repository.
2. Edit `test_script.py`. To make changes, write selenium scripts inside the run function defination.
3. Always bind any selenium script with `d` while writing test scripts. For example `driver.find_element()` should be written as `d.driver.find_element()`


## Features

1. Setting a custom wait time for the webdriver `test.wait(5)`
2. Settting the number of times a test should be performed `test.rerun(3, lambda: run())`
3. Getting the title of the page `test.getTitle()`
4. Checking whether the button or input type submit is clickable `test.checkClick("button")` or `test.checkClick("input")`
5. Checking the presence of an element in a webpage `test.checkElement("CLASS_NAME","container")`


<mark> Note that, this project is still experimental and hence does not support the full render wait time for any test actions. </mark>