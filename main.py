'''
This bot is supported by this main file and other distributions
'''
# TODO : add sys.exit() where it went wrong with pausing cmd

from app.excel_methods import *
from app.web_methods import *

try:
    print("Checking excel attachments...")
    (path, follow_limit, time_limit) = retrieve_file_path()
    nrows = get_nrows(path)

    check_rows(nrows)
    check_ok_status(path)
except Exception as e:
    print(e)
    print("Not checking the excel file in the begining ( add log )")
# TODO : add this to log

# print(follow_limit, time_limit)

# while True:       # TODO : enable while true

driver = connecting_with_chrome()
login_insta(driver)

# login into the id till here
count = follow_limit
(username_list, ok_list) = read_usernames(path)

for username, status, row in zip(username_list, ok_list, range(2,nrows+1)) :
    if status == None:
        print("\nWorking on user :- " + username)
        driver.get("https://www.instagram.com/" + username)

        if is_available(driver) == False:
            # Check for the availabily of username, if not then continue
            continue

        if (is_private(driver) == True):
            print("private and followed")
            follow_private_user(driver)
            count = count - 1

        elif (is_private(driver) == False):
            print("not private")
            # Checking Number of posts
            if num_posts(driver) == 0:
                print("no posts")
                follow_user(driver)
                count = count - 1

            elif num_posts(driver) == 1:
                print("==1")
                click_and_open(driver)
                click_like(driver)

                follow_user(driver)
                count = count - 1

            elif num_posts(driver) == 2:
                print("==2")
                click_and_open(driver)
                click_like(driver)

                click_arrow(driver)
                click_like(driver)

                follow_user(driver)
                count = count - 1

            elif num_posts(driver) > 2:
                print(">2")
                click_and_open(driver)
                click_like(driver)

                click_arrow(driver)
                click_like(driver)

                click_arrow(driver)
                click_like(driver)

                follow_user(driver)
                count = count - 1

        # putting "OK" in excel
        write_ok_status(path, row)















