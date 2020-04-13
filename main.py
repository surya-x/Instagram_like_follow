'''
This bot is supported by this main file and other distributions
'''
# TODO : add sys.exit() where it went wrong with pausing cmd
# TODO : terminate the script without closing the cmd in case of error
from app.excel_methods import *
from app.web_methods import *

try:
    print("Checking excel attachments...")

    (path, follow_limit, time_limit) = retrieve_file_parameter()
    nrows = get_nrows(path)

    check_rows(nrows)
    check_ok_status(path)
except Exception as e:
    print(e)                                                                    # Quit here
    print("Not checking the excel file in the begining ( add log )")            # LOG
    sys.exit()


# while True:       # TODO : enable while true

driver = connecting_with_chrome()
login_insta(driver)

# BOT will login into the id till here

count = follow_limit
(username_list, ok_list) = read_usernames(path)

for username, status, row in zip(username_list, ok_list, range(2, nrows+1)):
    if status is None:
        print("\nWorking on user :- " + username)
        driver.get("https://www.instagram.com/" + username)

        time.sleep(2)

        if not is_available(driver):
            # Check for the availabily of username, if not then continue
            continue

        ### Two conditions from here, one for private id, another for public id

        if is_private(driver):
            print(username + " is Private, following the user...")
            if follow_private_user(driver):
                count = count - 1
                # putting "OK" in excel
                write_ok_status(path, row)

        elif not is_private(driver):
            # Checking Number of posts

            if num_posts(driver) == 0:                                 # Number of posts = 0
                print("No Posts available to Like,")
                if follow_user(driver):
                    count = count - 1
                    # putting "OK" in excel
                    write_ok_status(path, row)

            elif num_posts(driver) == 1:

                if click_and_open(driver):
                    click_like(driver)

                if follow_user(driver):
                    count = count - 1
                    # putting "OK" in excel
                    write_ok_status(path, row)

            elif num_posts(driver) == 2:

                if click_and_open(driver):
                    click_like(driver)
                    click_arrow(driver)
                    click_like(driver)

                if follow_user(driver):
                    count = count - 1
                    # putting "OK" in excel
                    write_ok_status(path, row)

            elif num_posts(driver) > 2:

                if click_and_open(driver):
                    click_like(driver)
                    click_arrow(driver)

                    click_like(driver)
                    click_arrow(driver)

                    click_like(driver)

                if follow_user(driver):
                    count = count - 1
                    # putting "OK" in excel
                    write_ok_status(path, row)
