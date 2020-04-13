from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        if len(str(password))<6:
            print("Error : The entered password is too short to login, check again")
            driver.quit()

    except Exception as e:
        print(e)
        print("Error : Fetching username/password from credentials.xlsx")
        driver.quit()

    try:
        # Write the username and password into input blocks and hits enter
        driver.get("https://www.instagram.com/accounts/login/")

        time.sleep(3)

        username_input = driver.find_element(By.NAME,"username")
        password_input = driver.find_element(By.NAME,"password")

        username_input.send_keys(username)
        password_input.send_keys(password, Keys.RETURN)

        time.sleep(5)

    except NoSuchElementException:
        # TODO : make sure the except statement is working on correct situation

        print("The Username or Password is incorrect, Try opening it after correcting \nMake sure you have active internet")
    except:
        print("Error : Login into instagram")
        driver.quit()


def is_private(driver):
    isprivate = driver.find_elements(By.TAG_NAME, "h2")
    if len(isprivate) > 0:
        if (isprivate[-1].text == 'This Account is Private'):
            return True
        else:
            return False

    return False

def is_available(driver):
    if len(driver.find_elements(By.TAG_NAME, "h2")) > 0:
        available = driver.find_element(By.TAG_NAME, "h2")

        if available.text == "Sorry, this page isn't available.":
            print("The username entered is not correct, User may have changed its username.")
            return False
        else:
            return True

    return True

def num_posts(driver):
    num_posts = driver.find_element(By.CSS_SELECTOR, "ul li:nth-child(1)")
    num_posts = num_posts.text.strip("posts").replace(",", "")
    return int(num_posts)


def click_and_open(driver):
    first_post = WebDriverWait(driver, 300).until(EC.presence_of_element_located(
        (By.XPATH, "//*[@id='react-root']//article//a//div[2]")))
    first_post.click()

def click_like(driver):
    try:
        like = WebDriverWait(driver, 300).until(EC.presence_of_element_located(
            (By.XPATH, "//section[1]/span[1]/button")))
        like.click()
    except TimeoutError:
        print("Connection is running slow...")

def click_arrow(driver):
    arrow = WebDriverWait(driver, 60).until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[4]/div[1]/div/div/a")))
    arrow[-1].click()

def close_window(driver):
    if len(driver.find_elements(By.XPATH, "//div[4]/div[3]/button")) > 0:
        cross = driver.find_element(By.XPATH, "//div[4]/div[3]/button")
        cross.click()

def follow_user(driver):
    close_window(driver)
    try:
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section//span/span[1]/button")
        if follow.text == "Follow":
            follow.click()
        else:
            print("You are already following the user")
    except Exception as e:
        print(e)

def follow_private_user(driver):
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section//button")
        if follow.text == "Follow":
            follow.click()
        else:
            print("You are already following the user")


