import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, init
import time

init(autoreset=True)

def print_banner():
    try:
        with open("banner.txt", 'r', encoding='utf-8') as file:
            banner_content = file.read()
            print(f"{banner_content}")
    except FileNotFoundError:
        print(f"Error: File 'banner.txt' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print_banner()

def check_proxy(proxy):
    try:
        proxies = {'http': proxy, 'https': proxy}
        response = requests.get('https://www.google.com', proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True, response.elapsed.total_seconds()
        else:
            return False, None
    except Exception as e:
        return False, None

def main():
    filename = "proxies.txt"

    with open(filename, 'r') as file:
        proxy_list = [line.strip() for line in file.readlines()]

    total_proxies = len(proxy_list)
    print('[*] Total Proxies:', total_proxies)

    valid_proxies = []
    proxies_checked = 0

    print("[*] Checking proxies...\n")

    start_time = time.time()

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_proxy, proxy): proxy for proxy in proxy_list}

        for future in as_completed(futures):
            elapsed_time = time.time() - start_time

            if elapsed_time >= 5:
                print(f"[*] Progress: {proxies_checked}/{total_proxies} proxies checked.")
                start_time = time.time()

            proxy = futures[future]

            try:
                is_valid, _ = future.result()
                proxies_checked += 1

                if is_valid:
                    valid_proxies.append(proxy)
                    print(f"{Fore.GREEN}[+] Proxy: {proxy} is valid.")
                else:
                    print(f"{Fore.RED}[-] Proxy: {proxy} is invalid or unreachable. Removing from the list.")
            except Exception as e:
                print(f"{Fore.YELLOW}[*] Error checking proxy: {proxy}: {e}")

    with open(filename, 'w') as file:
        file.write('\n'.join(valid_proxies))

if __name__ == "__main__":
    main()
