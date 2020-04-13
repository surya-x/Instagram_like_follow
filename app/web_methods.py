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
        # uncomment this to make browser run in background
        # options.add_argument("-headless")
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print("Error : loading Chrome")
        print(e)
        sys.exit()                                                          # quit here


# This will login into instagram using credentials in "credentials.xlsx"
def login_insta(driver):
    try:
        # scrap username and password from (credentials.xlsx)
        workbook = openpyxl.load_workbook(r"assets\credentials.xlsx")
        sheet_login = workbook.worksheets[0]

        username = sheet_login["B1"].value
        password = sheet_login["B2"].value
        if len(str(password)) < 6:
            print("Error : The entered password is too short to login, check again")
            driver.quit()
            sys.exit()                                                      # QUIT HERE
    except Exception as e:
        print("Error : Fetching username/password from credentials.xlsx")
        print(e)
        driver.quit()

    try:
        # Write the username and password into input blocks and hits enter
        driver.get("https://www.instagram.com/accounts/login/")

        time.sleep(3)

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys(username)
        password_input.send_keys(password, Keys.RETURN)

        time.sleep(5)

    except NoSuchElementException:
        print("The Username or Password is incorrect, Try opening it after correcting \nMake sure you have active internet")
        print("\nIF NOT WORK after checking for above,\nInstagram may have updated its website, CONTACT the developer to update script")
        driver.quit()
        sys.exit()                                                                    # Quit HERE

    except TimeoutException:
        print("Make sure you have active internet connection")
        driver.quit()
        sys.exit()                                                                     # Quit HERE
    except Exception as e:
        print("Error : Login into instagram")
        print(e)
        driver.quit()
        sys.exit()                                                                     # Quit HERE


# TO Check is the id Private or Public
def is_private(driver):
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
        return True


# To check is the username and url is working or not,
# return True is working, False if not working
def is_available(driver):
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
        return False                                   # Return false if error in checking the username


# To give the no of posts user have uploaded
def num_posts(driver):
    try:
        num_posts = driver.find_element(By.CSS_SELECTOR, "ul li:nth-child(1)")
        num_posts = num_posts.text.strip("posts").replace(",", "")
        return int(num_posts)
    except Exception as e:
        print(e)                                       # LOGS
        return 3                                       # Return 3 as no. of posts if fail to load


# TO open the first post by clicking on it,,,
def click_and_open(driver):
    try:
        first_post = WebDriverWait(driver, 300).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='react-root']//article//a//div[2]")))
        first_post.click()
        return True
    except NoSuchElementException:
        print("Warning!")
        print("If this warning continue to show every time, CONTACT developer")
        return False
    except Exception as e:
        print(e)                                        # LOGS
        return False


# To click on Like icon on POST
def click_like(driver):
    try:
        like = WebDriverWait(driver, 300).until(EC.presence_of_element_located(
            (By.XPATH, "//section[1]/span[1]/button")))
        like.click()
    except TimeoutError:
        print("Connection is running slow...")
    except NoSuchElementException:
        print("Warning!")
        print("If this warning continue to show every time, CONTACT developer")
    except Exception as e:
        print(e)


# TO CLICK on next arrow to load next page
def click_arrow(driver):
    try:
        arrow = WebDriverWait(driver, 120).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[4]/div[1]/div/div/a")))
        arrow[-1].click()
    except TimeoutError:
        print("Connection is running slow...")
    except NoSuchElementException:
        print("Warning!")
        print("If this warning continue to show every time, CONTACT developer")
    except Exception as e:
        print(e)


# Check if any window is already opened, then will close that
def close_window(driver):
    try:
        if len(driver.find_elements(By.XPATH, "//div[4]/div[3]/button")) > 0:
            cross_button = driver.find_element(By.XPATH, "//div[4]/div[3]/button")
            cross_button.click()
    except Exception as e:
        print(e)                                                # LOGS


# This method is used to follow any user
def follow_user(driver):
    # Check if any window is already opened
    close_window(driver)
    try:
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section//span/span[1]/button")
        if follow.text == "Follow":
            follow.click()
            time.sleep(2)
            return True
        else:
            print("You are already following the user")
            return False
    except NoSuchElementException:
        print("Error : in following this user\nIf the problem continues instagram may have updated its website")
        print("CONTACT developer.")
        return False
    except Exception as e:
        print("Error : in following this user")
        print(e)
        return False


# This method is used to follow the PRIVATE USER
def follow_private_user(driver):
    try:
        follow = driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/button")
        if follow.text == "Follow":
            follow.click()
            time.sleep(2)
            return True
        elif follow.text == "Requested":
            print("You already sent request to follow")
            return False
        else:
            print("You are already following the user")
            return False
    except NoSuchElementException:
        follow_user(driver)

    except Exception as e:
        print("Error : in following this user")
        print(e)
