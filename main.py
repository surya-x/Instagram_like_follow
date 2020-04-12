'''
This bot is supported by this main file and other distributions
'''
from app.excel_methods import *
from app.web_methods import *
import openpyxl
from selenium.common.exceptions import NoSuchElementException

try:
    path = retrieve_file_path()
    nrows = get_nrows(path)

    check_rows(nrows)
    check_ok_status(path)
except:
    print("Not checking the excel file in the begining ( add log )")
    # TODO : add this to log


while True:
    driver = connecting_with_chrome()
    login_insta(driver)





