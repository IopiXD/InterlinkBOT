# InterlinkBOT

InterlinkBOT is a Python-based automation tool designed to interact with the Interlink Labs API for automated token claiming. It supports both proxy and non-proxy configurations, allowing users to log in via email or Telegram and claim tokens every 4 hours.

## Regis
https://interlinklabs.ai/ or Download via play store / Apps Store

## Features
- **Auto Claim**: Automatically claims tokens every 4 hours.
- **Proxy Support**: Option to use proxies for enhanced privacy and reliability.
- **Non-Proxy Support**: Works without proxies for simpler setups.
- **Authentication Options**: Supports login via email or Telegram with OTP verification.
- **Multi-Account Support**: Allows token collection for multiple accounts.

## Installation

Follow these steps to set up InterlinkBOT on your system:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/IopiXD/InterlinkBOT.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd InterlinkBOT
   ```

3. **Install Requirements**:
   Ensure you have Python 3 installed, then install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   The required packages are:
   - `requests`
   - `pytz`
   - `colorama`

## How to Run

You can run the bot with or without proxy support, depending on your needs:

- **Without Proxy**:
  ```bash
  python main.py
  ```

- **With Proxy**:
  Ensure you have a `proxies.txt` file populated with proxy addresses (one per line) in the project directory, then run:
  ```bash
  python mainproxy.py
  ```

## How to Get Tokens

To obtain JWT tokens for your accounts, follow these steps:

1. **Run the Script**:
   Start the bot using either `python main.py` or `python mainproxy.py`.

2. **Select Login Method**:
   From the menu, choose:
   - **Option 1**: Login with Email
   - **Option 2**: Login with Telegram

3. **Enter Credentials**:
   - Input your **Login ID** and **Passcode** when prompted.
   - Wait for the OTP code to be sent to your email or Telegram.
   - Enter the **OTP code** when prompted.

4. **Token Storage**:
   - Upon successful authentication, the JWT token will be saved to `data.txt`.
   - Press any key to return to the main menu.

5. **Repeat for Multiple Accounts**:
   If you have multiple accounts, repeat the process for each account to collect tokens one by one.

------**Token Exp 30 days, pliss get new tokens every 30 days**------

## How to Perform Daily Claims

To start the automated token claiming process:

1. Select **Option 3** from the main menu to initiate the daily claim loop.
2. The bot will process all tokens stored in `data.txt`, checking and claiming tokens for each account if available.
3. The bot will then sleep until the next claim window (every 4 hours)

## Notes
- Ensure `data.txt` is writable for storing JWT tokens.
- For proxy usage, populate `proxies.txt` with valid proxy addresses (format: `http://<proxy_ip>:<port>` or similar).
- The bot includes retry logic for failed requests and proxy checks to ensure reliability.
- Tokens are processed sequentially, and the bot displays detailed logs with timestamps and status updates.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
Use this tool responsibly and in compliance with Interlink Labs' terms of service. The developers are not responsible for any misuse or consequences arising from the use of this tool.
