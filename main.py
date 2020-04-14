'''
This bot is supported by this main file and other distributions
'''
# TODO : add sys.exit() where it went wrong with pausing cmd
# TODO : terminate the script without closing the cmd in case of error
from app.excel_methods import *
from app.web_methods import *
from config import *
import pause
import datetime

try:
    print("\nStarting...\nChecking excel attachments...")
    logging.info("Checking excel attachments")

    (path, follow_limit, time_limit) = retrieve_file_parameter()
    nrows = get_nrows(path)

    check_rows(nrows)
    check_ok_status(path)

except Exception as e:
    print(e)  # Quit here
    logging.error("Not checking the excel file in the begining")
    logging.error(e)
    os.system("PAUSE")
    sys.exit()


while True:
    logging.info("inside while true!!!")
    print("Logging you in.")
    driver = connecting_with_chrome()
    login_insta(driver)

    # BOT will login into the id till here

    count = follow_limit
    (username_list, ok_list) = read_usernames(path)

    time.sleep(10)

    for username, status, row in zip(username_list, ok_list, range(2, nrows + 1)):
        if status is None:
            print("\nWorking on user :- " + username)
            logging.info("\nWorking on user :- " + username)
            driver.get("https://www.instagram.com/" + username)

            time.sleep(2)

            if not is_available(driver):
                # Check for the availabily of username, if not then continue
                wrong_status(path,row)
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

                if num_posts(driver) == 0:  # Number of posts = 0
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

        if count == 0:
            break

    if count > 0:
        # Completed for all usernames in "insta_search_found.xlsx" ...DONE
        rename_file(path)
        driver.quit()
        sys.exit()
    elif count == 0:
        # this will terminate the if no blank column left
        check_ok_status(path)

        # The script will run this part only if more blank columns are left
        driver.quit()

        print("\nThe Limit reached, waiting for %d minutes"%time_limit)
        till = datetime.timedelta(minutes=time_limit)
        till = datetime.datetime.now() + till
        print("Waiting till " + str(till))
        pause.minutes(time_limit)
