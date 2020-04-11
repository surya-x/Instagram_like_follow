from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import openpyxl
import sys

# This will establish connection with chrome driver
def connecting_with_chrome():
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument("-headless")
        driver = webdriver.Chrome(options=options)
        return driver
    except:
        print("Error : loading Chrome")

# This will login into instagram using credentials in "credentials.xlsx"
def login_insta(driver):
    try:
        # scrap username and password from (credentials.xlsx)
        workbook = openpyxl.load_workbook(r"assets\credentials.xlsx")
        sheet_login = workbook.worksheets[0]

        username = sheet_login["B1"].value
        password = sheet_login["B2"].value

    except:
        print("Error : Fetching username/password from credentials.xlsx")
        driver.quit()

    try:
        # Write the username and password into input blocks and hits enter
        driver.get("https://www.instagram.com/accounts/login/")
        username_input = driver.find_element(By.NAME,"username")
        password_input = driver.find_element(By.NAME,"password")

        username_input.send_keys(username)
        password_input.send_keys(password, Keys.RETURN)

        time.sleep(5)

    except NoSuchElementException:
        print("The Username or Password is incorrect, Try opening it after correcting \nMake sure you have active internet")
    except:
        print("Error : Login into instagram")
        driver.quit()

