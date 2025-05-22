import requests
import time
import datetime
import pytz
import os
from colorama import init, Fore, Style
import uuid

# Initialize colorama
init(autoreset=True)

# Configuration
BASE_URL = "https://prod.interlinklabs.ai/api/v1"
WIB = pytz.timezone("Asia/Jakarta")
MAIN_HEADERS = {
    "accept": "*/*",
    "user-agent": "okhttp/4.12.0",
    "accept-encoding": "gzip",
    "content-type": "application/json"
}
MAX_RETRIES = 3
INITIAL_BACKOFF = 1
BACKOFF_FACTOR = 2
DATA_FILE = "data.txt"

# Utility Functions
def get_timestamp():
    return datetime.datetime.now(datetime.timezone.utc).astimezone(WIB).strftime("%Y-%m-%d %H:%M:%S")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    banner = """
    ██╗ ██████╗ ██████╗ ██╗
    ██║██╔═══██╗██╔══██╗██║
    ██║██║   ██║██████╔╝██║
    ██║██║   ██║██╔═══╝ ██║
    ██║╚██████╔╝██║     ██║
    ╚═╝ ╚═════╝ ╚═╝     ╚═╝
    Is Her :)    
    Interlink Auto Tool
    """
    print(Fore.MAGENTA + banner)

def print_section_header(title):
    timestamp = get_timestamp()
    print(f"{Fore.MAGENTA}{timestamp}{Style.RESET_ALL} | {Fore.CYAN}{'=' * 50}")
    print(f"{Fore.MAGENTA}{timestamp}{Style.RESET_ALL} | {Fore.CYAN}{title:^50}")
    print(f"{Fore.MAGENTA}{timestamp}{Style.RESET_ALL} | {Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def print_info(label, value, color=Fore.WHITE):
    timestamp = get_timestamp()
    print(f"{Fore.MAGENTA}{timestamp}{Style.RESET_ALL} | {Fore.YELLOW}{label:<15}: {color}{value}{Style.RESET_ALL}")

def print_separator():
    timestamp = get_timestamp()
    print(f"\n{Fore.MAGENTA}{timestamp}{Style.RESET_ALL} | {Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")

def read_jwt_tokens(file_path=DATA_FILE):
    try:
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r') as file:
            return [token.strip() for token in file.readlines() if token.strip()]
    except Exception as e:
        print_info("Error", f"Failed to read tokens: {e}", Fore.RED)
        return []

def save_jwt_token(token, file_path=DATA_FILE):
    try:
        with open(file_path, "a") as f:
            f.write(f"{token}\n")
        print_info("Token Saved", f"JWT token saved to {file_path}", Fore.GREEN)
    except Exception as e:
        print_info("Error", f"Failed to save token: {e}", Fore.RED)

# API Functions
def make_request(method, url, headers, data=None, retries=MAX_RETRIES):
    for attempt in range(retries):
        try:
            response = requests.request(method, url, headers=headers, json=data)
            if response.status_code in (200, 201):
                return response.json()
            else:
                print_info(f"Attempt {attempt + 1} Failed", f"Status: {response.status_code}", Fore.RED)
                time.sleep(INITIAL_BACKOFF * (BACKOFF_FACTOR ** attempt))
        except requests.RequestException as e:
            print_info(f"Attempt {attempt + 1} Error", str(e), Fore.RED)
            time.sleep(INITIAL_BACKOFF * (BACKOFF_FACTOR ** attempt))
    return None

def check_passcode(login_id, passcode):
    url = f"{BASE_URL}/auth/check-passcode"
    headers = MAIN_HEADERS.copy()
    payload = {"loginId": login_id, "passcode": passcode}
    return make_request("POST", url, headers, payload)

def send_otp_email(email, login_id, passcode):
    url = f"{BASE_URL}/auth/send-otp-email-verify-login"
    headers = MAIN_HEADERS.copy()
    payload = {"loginId": login_id, "passcode": passcode, "email": email}
    return make_request("POST", url, headers, payload)

def check_otp_email(login_id, otp):
    url = f"{BASE_URL}/auth/check-otp-email-verify-login"
    headers = MAIN_HEADERS.copy()
    payload = {"loginId": login_id, "otp": otp}
    return make_request("POST", url, headers, payload)

def send_otp_telegram(login_id, passcode, chat_id):
    url = f"{BASE_URL}/auth/send-otp-verify-telegram-login"
    headers = MAIN_HEADERS.copy()
    payload = {"loginId": login_id, "passcode": passcode, "chatId": chat_id}
    return make_request("POST", url, headers, payload)

def verify_otp_telegram(login_id, otp):
    url = f"{BASE_URL}/auth/verify-otp-telegram-login"
    headers = MAIN_HEADERS.copy()
    payload = {"loginId": login_id, "otp": otp}
    return make_request("POST", url, headers, payload)

def get_current_user(token):
    url = f"{BASE_URL}/auth/current-user"
    headers = MAIN_HEADERS.copy()
    headers['authorization'] = f'Bearer {token}'
    response = make_request("GET", url, headers)
    if response and response.get('statusCode') == 200:
        login_id = response['data']['loginId']
        username = response['data']['username']
        print_info("Login ID", login_id, Fore.GREEN)
        print_info("Username", username, Fore.GREEN)
        return login_id
    return None

def get_token_info(token):
    url = f"{BASE_URL}/token/get-token"
    headers = MAIN_HEADERS.copy()
    headers['authorization'] = f'Bearer {token}'
    response = make_request("GET", url, headers)
    if response and response.get('statusCode') == 200:
        amount = response['data']['interlinkGoldTokenAmount']
        print_info("Balance $ITLG", amount, Fore.GREEN)
        return amount
    return None

def check_is_claimable(token):
    url = f"{BASE_URL}/token/check-is-claimable"
    headers = MAIN_HEADERS.copy()
    headers['authorization'] = f'Bearer {token}'
    response = make_request("GET", url, headers)
    if response and response.get('statusCode') == 200:
        is_claimable = response['data']['isClaimable']
        status = "Claimable" if is_claimable else "Already Claimed"
        color = Fore.GREEN if is_claimable else Fore.YELLOW
        print_info("Claim Status", status, color)
        return is_claimable
    return None

def claim_airdrop(token):
    url = f"{BASE_URL}/token/claim-airdrop"
    headers = MAIN_HEADERS.copy()
    headers['authorization'] = f'Bearer {token}'
    response = make_request("POST", url, headers)
    if response and response.get('statusCode') == 200:
        status = "Airdrop claimed successfully!" if response['data'] else "Failed to claim airdrop"
        color = Fore.GREEN if response['data'] else Fore.RED
        print_info("Airdrop Claim", status, color)
        return response['data']
    return None

# Core Functionality
def login_email():
    clear_terminal()
    display_banner()
    print_section_header("Email Login")
    login_id = input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Enter login ID: {Style.RESET_ALL}").strip()
    passcode = input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Enter passcode: {Style.RESET_ALL}").strip()

    response = check_passcode(login_id, passcode)
    if not response or response.get("statusCode") != 200:
        print_info("Result", "Passcode check failed", Fore.RED)
        return

    email = response["data"].get("email")
    if not email:
        print_info("Result", f"No email found for login ID {login_id}", Fore.RED)
        return

    print_info("Email Found", email, Fore.GREEN)
    response = send_otp_email(email, login_id, passcode)
    if not response or response.get("statusCode") != 200:
        print_info("Result", f"Failed to send OTP to {email}", Fore.RED)
        return

    otp = input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Enter the OTP sent to {email}: {Style.RESET_ALL}").strip()
    response = check_otp_email(login_id, otp)
    if response and response.get("statusCode") == 200:
        jwt_token = response["data"]["jwtToken"]
        print_info("JWT Token", jwt_token, Fore.GREEN)
        save_jwt_token(jwt_token)
    else:
        print_info("Result", "OTP verification failed", Fore.RED)

def login_telegram():
    clear_terminal()
    display_banner()
    print_section_header("Telegram Login")
    login_id = input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Enter login ID: {Style.RESET_ALL}").strip()
    passcode = input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Enter passcode: {Style.RESET_ALL}").strip()

    response = check_passcode(login_id, passcode)
    if not response or response.get("statusCode") != 200:
        print_info("Result", "Passcode check failed", Fore.RED)
        return

    chat_id = response["data"]["verificationInfo"][0]["chatId"]
    print_info("Chat ID", chat_id, Fore.GREEN)
    response = send_otp_telegram(login_id, passcode, chat_id)
    if not response or response.get("statusCode") != 200:
        print_info("Result", f"Failed to send OTP to chat ID {chat_id}", Fore.RED)
        return

    otp = input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Enter the OTP sent to your Telegram: {Style.RESET_ALL}").strip()
    response = verify_otp_telegram(login_id, otp)
    if response and response.get("statusCode") == 200:
        jwt_token = response["data"]["jwtToken"]
        print_info("JWT Token", jwt_token, Fore.GREEN)
        save_jwt_token(jwt_token)
    else:
        print_info("Result", "OTP verification failed", Fore.RED)

def process_daily_claim():
    clear_terminal()
    display_banner()
    tokens = read_jwt_tokens()
    total_tokens = len(tokens)
    if total_tokens == 0:
        print_info("Result", "No tokens found in data.txt", Fore.RED)
        return

    for idx, token in enumerate(tokens, start=1):
        print_section_header(f"Processing Account {idx} of {total_tokens}")
        login_id = get_current_user(token)
        if login_id is None:
            continue
        get_token_info(token)
        if check_is_claimable(token):
            claim_airdrop(token)

def get_next_target_time():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_wib = now_utc.astimezone(WIB)
    claim_hours = [3, 7, 11, 15, 19, 23]
    
    for hour in claim_hours:
        target = now_wib.replace(hour=hour, minute=0, second=10, microsecond=0)
        if target > now_wib:
            return target
    
    tomorrow = now_wib + datetime.timedelta(days=1)
    return tomorrow.replace(hour=3, minute=0, second=10, microsecond=0)

def daily_claim_loop():
    while True:
        process_daily_claim()
        next_time = get_next_target_time()
        now = datetime.datetime.now(datetime.timezone.utc).astimezone(WIB)
        wait_seconds = (next_time - now).total_seconds()
        print_info("Next Claim At", next_time.strftime("%Y-%m-%d %H:%M:%S WIB"), Fore.CYAN)
        print_info("Sleeping for", f"{int(wait_seconds)} seconds", Fore.BLUE)
        time.sleep(wait_seconds)

def main():
    while True:
        clear_terminal()
        display_banner()
        print_section_header("Interlink Auto Tool Menu")
        print_info("Options", "1. Get Token Email Login", Fore.CYAN)
        print_info("", "2. Get Token Telegram Login", Fore.CYAN)
        print_info("", "3. Daily Claim", Fore.CYAN)
        print_info("", "4. Exit", Fore.CYAN)
        choice = input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Select an option (1-4): {Style.RESET_ALL}").strip()

        if choice == "1":
            login_email()
        elif choice == "2":
            login_telegram()
        elif choice == "3":
            daily_claim_loop()
        elif choice == "4":
            print_info("Result", "Exiting program", Fore.YELLOW)
            break
        else:
            print_info("Result", "Invalid option, please try again", Fore.RED)
        input(f"{Fore.MAGENTA}{get_timestamp()}{Style.RESET_ALL} | {Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()