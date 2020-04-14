from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *
import time
import openpyxl
import sys
import pause
import os

# This will establish connection with chrome driver
def connecting_with_chrome():
    try:
        logging.info("connecting with chrome called")
        options = webdriver.ChromeOptions()
        # comment/uncomment this to make browser run in background
        options.add_argument("-headless")

        # To run at my pc
        driver = webdriver.Chrome(options=options)

        # TO run at his pc
        # driver = webdriver.Chrome(options=options,executable_path="")

        return driver
    except Exception as e:
        print("Error : loading Chrome")
        print(e)
        logging.error(e)
        os.system("PAUSE")
        sys.exit()                                                          # quit here


# This will login into instagram using credentials in "credentials.xlsx"
def login_insta(driver):
    logging.info("login_insta called")
    try:
        # scrap username and password from (credentials.xlsx)
        workbook = openpyxl.load_workbook(r"assets\credentials.xlsx")
        sheet_login = workbook.worksheets[0]

        username = sheet_login["B1"].value
        password = sheet_login["B2"].value
        if len(str(password)) < 6:
            print("Error : The entered password is too short to login, check again")
            driver.quit()
            os.system("PAUSE")
            sys.exit()                                                      # QUIT HERE
    except Exception as e:
        print("Error : Fetching username/password from credentials.xlsx")
        print(e)
        logging.error(e)
        driver.quit()

    try:
        # Write the username and password into input blocks and hits enter
        driver.get("https://www.instagram.com/accounts/login/")

        pause.seconds(3)

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys(username)
        password_input.send_keys(password, Keys.RETURN)
    except NoSuchElementException as nse:
        print("The Username or Password is incorrect, Try opening it after correcting \nMake sure you have active internet")
        print("\nIF NOT WORK after checking for above,\nInstagram may have updated its website, CONTACT the developer to update script")

        logging.error(nse)
        driver.quit()
        os.system("PAUSE")
        sys.exit()                                                                   # Quit HERE
    except TimeoutException as te:
        print("Make sure you have active internet connection")
        logging.error(te)
        driver.quit()
        os.system("PAUSE")
        sys.exit()                                                                     # Quit HERE
    except Exception as e:
        print("Error : Login into instagram")
        print(e)
        logging.error(e)
        driver.quit()
        os.system("PAUSE")
        sys.exit()                                                                     # Quit HERE


# TO Check is the id Private or Public
def is_private(driver):
    logging.info("is_private called")
    try:
        isprivate = driver.find_elements(By.TAG_NAME, "h2")
        if len(isprivate) > 0:
            if isprivate[-1].text == 'This Account is Private':
                return True
            else:
                return False

        return False
    except Exception as e:
        print(e)
        logging.error(e)
        return True
        # consider as private account if error occurs while checking


# To check is the username and url is working or not,
# return True is working, False if not working
def is_available(driver):
    logging.info("is_available called")
    try:
        if len(driver.find_elements(By.TAG_NAME, "h2")) > 0:
            available = driver.find_element(By.TAG_NAME, "h2")

            if available.text == "Sorry, this page isn't available.":
                print("The username entered is not correct, User may have changed its username.")
                return False                           # 1 out of 2 condition, when return false
            else:
                return True

        return True
    except Exception as e:
        print(e)                                            # LOGS
        logging.error(e)
        return False                                   # Return false if error in checking the username


# To give the no of posts user have uploaded
def num_posts(driver):
    logging.info("num_posts called")
    try:
        num_posts = driver.find_element(By.CSS_SELECTOR, "ul li:nth-child(1)")
        num_posts = num_posts.text.strip("posts").replace(",", "")
        return int(num_posts)
    except Exception as e:
        print(e)                                       # LOGS
        logging.error(e)
        return 3                                       # Return 3 as no. of posts if fail to load


# TO open the first post by clicking on it,,,
def click_and_open(driver):
    logging.info("click and open called")
    try:
        first_post = WebDriverWait(driver, 300).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='react-root']//article//a//div[2]")))
        first_post.click()
        return True
    except NoSuchElementException as nse:
        print("Warning!")
        print("If this warning continue to show every time, CONTACT developer")
        logging.error(nse)
        return False
    except Exception as e:
        print(e)                                        # LOGS
        logging.error(e)
        return False


# To click on Like icon on POST
def click_like(driver):
    logging.info("click_like called")
    try:
        like = WebDriverWait(driver, 300).until(EC.presence_of_element_located(
            (By.XPATH, "//section[1]/span[1]/button")))
        like.click()
    except TimeoutError as te:
        print("Connection is running slow...")
        logging.error(te)
    except NoSuchElementException as nse:
        print("Warning!")
        print("If this warning continue to show every time, CONTACT developer")
        logging.error(nse)
    except Exception as e:
        print(e)
        logging.error(e)


# TO CLICK on next arrow to load next page
def click_arrow(driver):
    logging.info("click arrow called")
    try:
        arrow = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[4]/div[1]/div/div/a")))
        arrow[-1].click()
    except TimeoutError as te:
        print("Connection is running slow...")
        logging.error(te)
    except NoSuchElementException as nse:
        print("Warning!")
        print("If this warning continue to show every time, CONTACT developer")
        logging.error(nse)
    except Exception as e:
        print(e)
        logging.error(e)


# Check if any window is already opened, then will close that
def close_window(driver):
    logging.info("close window called")
    try:
        if len(driver.find_elements(By.XPATH, "//div[4]/div[3]/button")) > 0:
            cross_button = driver.find_element(By.XPATH, "//div[4]/div[3]/button")
            cross_button.click()
    except Exception as e:
        print(e)                                                # LOGS
        logging.error(e)

# This method is used to follow any user
def follow_user(driver):
    # Check if any window is already opened
    close_window(driver)
    logging.info("follow user called")
    try:
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section//span/span[1]/button")
        if follow.text == "Follow":
            webdriver.ActionChains(driver).move_to_element(follow).click(follow).perform()
            time.sleep(2)
            return True
        else:
            print("You are already following the user")
            return False
    except ElementClickInterceptedException as eci:
        logging.error(eci)
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section//span/span[1]/button")
        webdriver.ActionChains(driver).move_to_element(follow).click(follow).perform()
        return True
    except NoSuchElementException as nse:
        print("Error : in following this user\nIf the problem continues instagram may have updated its website")
        print("CONTACT developer.")
        logging.error(nse)
        return False
    except Exception as e:
        print("Error : in following this user")
        print(e)
        logging.error(e)
        return False


# This method is used to follow the PRIVATE USER
def follow_private_user(driver):
    logging.info("follow private user called")
    try:
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/button")
        if "Follow" in follow.text:
            webdriver.ActionChains(driver).move_to_element(follow).click(follow).perform()
            time.sleep(2)
            return True
        elif follow.text == "Requested":
            print("You already sent request to follow")
            return False
        else:
            print("You are already following the user")
            return False
    except ElementClickInterceptedException as eci:
        logging.error(eci)
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/button")
        webdriver.ActionChains(driver).move_to_element(follow).click(follow).perform()
        return True

    except NoSuchElementException as nse:
        follow_user(driver)
        logging.error(nse)
        logging.info("passing to follow_user")

    except Exception as e:
        print("Error : in following this user")
        print(e)
        logging.error(e)
        return False
