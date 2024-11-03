from os import access
import pyotp
import time
import datetime
import json
import glob
import requests

from time import sleep
from ..helper.helper_module import Helper
from backend.utils.logging_utils import *
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from kiteconnect import KiteConnect, KiteTicker
from backend.modules.connection.kiteconnect_offline import KiteConnectOffline
from backend.aws.SecretsManager.aws_secrets_manager import get_secret


class Connection:
    def __init__(self):
        self.secret_keys = self.get_secret_keys()
        self.api_subscription_inactive = False

    def get_secret_keys(self):
        secret_keys = json.loads(get_secret(SECRET_NAME, REGION_NAME))
        return secret_keys

    def connect_to_broker(self):
        kite = None
        kite_ticker = None
        access_token = None

        api_key = self.secret_keys.get('api_key')
        auth_date = datetime.datetime.now().strftime('%d%H')
        access_token_file = f"{ACCESS_TOKEN_PATH + '_' + auth_date}"
        encrypt_token_file = f"{ENCRYPT_TOKEN_PATH + '_' + auth_date}"

        # API SUBSCRIPTION ONLINE
        if os.path.isfile(access_token_file):
            kite, kite_ticker, access_token = self.establish_old_connection(api_key)
        else:
            self.remove_old_tokens('access')
            self.remove_old_tokens('request')
            kite, kite_ticker, access_token = self.establish_new_connection()

        # connection object
        if kite is None and kite_ticker is None:
            self.api_subscription_inactive = True
        else:
            connection_object = {
                "kite": kite,
                "kiteticker": kite_ticker,
                "authorize": access_token
            }

        # API SUBSCRIPTION OFFLINE (LIMITED)
        if self.api_subscription_inactive:
            if os.path.isfile(encrypt_token_file):
                kite = self.establish_offline_connection()
            else:
                self.remove_old_tokens('encrypt')
                kite = self.establish_offline_connection()

            # connection object (Limited)
            if kite:
                connection_object = {
                    "kite": kite
                }

        return connection_object

    def establish_offline_connection(self):
        kite = self.broker_login()
        return kite

    def establish_old_connection(self, api_key):
        auth_date = datetime.datetime.now().strftime('%d%H')
        access_token_file = f"{ACCESS_TOKEN_PATH + '_' + auth_date}"

        if os.path.isfile(access_token_file):
            access_token = open(ACCESS_TOKEN_PATH + '_' + auth_date, 'r').read()
            kite = KiteConnect(api_key)
            kite_ticker = KiteTicker(api_key, access_token)
            kite.set_access_token(access_token)
            log_info(INFO.CONNECT_KITE_COMPLETE)
        return kite, kite_ticker, access_token

    def establish_new_connection(self):
        kite, kite_ticker, access_token = self.broker_login(KiteConnect, KiteTicker)
        if kite and kite_ticker and access_token:
            kite.set_access_token(access_token)
            log_info(INFO.NEW_CONNECTION_REQUEST_COMPLETE)
        return kite, kite_ticker, access_token

    def remove_old_tokens(self, token_type="all"):
        """
        Removes old token files based on the specified token type or removes all if 'all' is chosen.

        Args:
            token_type (str, optional): The type of token to remove. Defaults to "all". Can be "access", "request", or "encrypt" for specific removal.
        """

        token_paths = {
            "access": ACCESS_TOKEN_PATH,
            "request": REQUEST_TOKEN_PATH,
            "encrypt": ENCRYPT_TOKEN_PATH
        }

        if token_type not in token_paths and token_type != "all":
            raise ValueError("Invalid token_type. Valid options are 'access', 'request', 'encrypt', or 'all'.")

        # Use a list comprehension to combine removal patterns for all token types if 'all' is chosen
        removal_patterns = []
        if token_type == "all":
            removal_patterns = [token_paths[token_type] + "*" for token_type in token_paths]
        else:
            removal_pattern = token_paths[token_type] + "*"
            removal_patterns.append(removal_pattern)

        old_token_files = []
        for removal_pattern in removal_patterns:
            old_token_files.extend(glob.glob(removal_pattern))

        for old_token_file in old_token_files:
            os.remove(old_token_file)

        if token_type == "all":
            log_info(f"Removed old tokens of all types successfully.")
        else:
            log_info(f"Removed old {token_type.upper()} tokens successfully.")

    def remove_file(self, file_path):
        try:
            os.remove(file_path)
        except Exception as error:
            log_error(ERROR.REMOVE_FILE_ERROR, file_path)

    def get_encrypt_token(self, userid, password, twofa):
        encrypt_token = None
        auth_date = datetime.datetime.now().strftime('%d%H')
        encrypt_token_file = f"{ENCRYPT_TOKEN_PATH + '_' + auth_date}"

        # Check if the encrypt token file exists
        if os.path.isfile(encrypt_token_file):
            encrypt_token = open(ENCRYPT_TOKEN_PATH + '_' + auth_date, 'r').read()
            return encrypt_token

        if encrypt_token is None:
            session = requests.Session()
            response = session.post('https://kite.zerodha.com/api/login', data={
                "user_id": userid,
                "password": password
            })
            response = session.post('https://kite.zerodha.com/api/twofa', data={
                "request_id": response.json()['data']['request_id'],
                "twofa_value": twofa,
                "user_id": response.json()['data']['user_id']
            })

            encrypt_token = response.cookies.get('enctoken')
            Helper().write_token_output('.zerodha_encrypt_token' + '_' + auth_date, encrypt_token)

        return encrypt_token

    def is_totp_login_successful(self, url):
        """Checks if the URL indicates a successful login."""
        url_parts = url.split('request_token=')
        if len(url_parts) > 1:
            return True

    def broker_login(self, KiteConnect=None, KiteTicker=None):
        # Assign properties
        auth_date = datetime.datetime.now().strftime('%d%H')
        api_key = self.secret_keys.get('api_key')
        secret_key = self.secret_keys.get('secret_key')
        user_id = self.secret_keys.get('user_id')
        user_pass = self.secret_keys.get('user_pass')
        mfa_token = self.secret_keys.get('mfa_token')

        authkey = pyotp.TOTP(mfa_token)
        twofa = authkey.now()

        # Initialize browser service
        if self.api_subscription_inactive:
            enctoken = self.get_encrypt_token(user_id, user_pass, twofa)
            kite = KiteConnectOffline(enctoken)
            login_url = 'https://kite.zerodha.com/'

            return kite

            # No need to login for offline API
            # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            # driver.get(login_url)      
        else:
            kite = KiteConnect(api_key=api_key)
            response = requests.get(kite.login_url())
            if response.status_code == 200:

                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
                driver.get(kite.login_url())
            else:
                return None, None, None

        try:

            # Username input
            username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="userid"]'))
            )
            username.send_keys(user_id)

            # Password input
            password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
            )
            password.send_keys(user_pass)

            # Submit button
            if self.api_subscription_inactive:
                submit = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div/div/form/div[4]/button'))
                )
            else:
                submit = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div/div/div[2]/form/div[4]/button'))
                )

            submit.click()

            # MFA / external TOTP
            totp = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div/div/form/div[1]/input'))
            )

            try:
                authkey = pyotp.TOTP(mfa_token)
                totp.send_keys(authkey.now())
                time.sleep(3)
                url = driver.current_url
                # Check for successful login 
                login_successful = self.is_totp_login_successful(url)

            except ValueError:
                user_entered_code = input("Automatic TOTP failed. Please Enter Google Authenticator Code: ")
                totp.send_keys(user_entered_code)
                try:
                    time.sleep(3)
                    url = driver.current_url
                    # Check for successful login
                    login_successful = self.is_totp_login_successful(url)

                except Exception as error:
                    print("Error submitting code:", error)

            # Request token generation
            if not self.api_subscription_inactive:

                if login_successful:

                    url = driver.current_url
                    url_parts = url.split('request_token=')
                    if len(url_parts) > 1:
                        initial_token = url_parts[1].split('&')[0]
                        token_str = str(initial_token)
                        Helper().write_token_output('.zerodha_request_token' + '_' + auth_date, token_str)
                        log_info("Generate Kite Request Token ...COMPLETE!")
                    else:
                        log_error("Kite Request Token Not Found")

                    # Access token generation
                    data = kite.generate_session(initial_token, api_secret=secret_key)
                    access_token = data['access_token']
                    token_str = str(access_token)
                    Helper().write_token_output('.zerodha_access_token' + '_' + auth_date, token_str)
                    log_info("Generate Kite Access Token ...COMPLETE!")

                    # Kite Ticker Subscription
                    kite_ticker = KiteTicker(api_key, access_token)

                    return kite, kite_ticker, access_token

                else:
                    log_error("MFA autentication failed, Please try again after some time!")
                    exit()

            else:
                return kite

        except Exception as error:
            log_error(f"Error during broker login: {error}")
            raise error

        finally:
            if driver:
                driver.quit()
