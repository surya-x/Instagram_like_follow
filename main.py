'''
This bot is supported by this main file and other distributions
'''
from app.excel_methods import *
from app.web_methods import *
import openpyxl
from selenium.common.exceptions import NoSuchElementException

nrows = get_nrows()
path = retrieve_file_path()

check_rows(nrows)
check_ok_status(path)

while True:
    driver = connecting_with_chrome()
    login_insta(driver)





