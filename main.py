import requests
import warnings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from pystyle import Center, Colors, Colorate
import os
import time


warnings.filterwarnings("ignore", category=DeprecationWarning)


def print_announcement():
    try:
        r = requests.get("pepe", headers={"Cache-Control": "no-cache"})
        announcement = r.content.decode('utf-8').strip()
        print(announcement)
    except:
        print("")


def main():
    print_announcement()

    os.system("title Twitch Cooker - Twitch Viewer Bot")

    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
████████╗██╗    ██╗██╗████████╗ ██████╗██╗  ██╗     ██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗██████╗ 
╚══██╔══╝██║    ██║██║╚══██╔══╝██╔════╝██║  ██║    ██╔════╝██╔═══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗
   ██║   ██║ █╗ ██║██║   ██║   ██║     ███████║    ██║     ██║   ██║██║   ██║█████╔╝ █████╗  ██████╔╝
   ██║   ██║███╗██║██║   ██║   ██║     ██╔══██║    ██║     ██║   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
   ██║   ╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║    ╚██████╗╚██████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║
   ╚═╝    ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝""")))
    announcement = print_announcement()
    print("")
    print("")
    print("")
    

    proxy_servers = {
        1: "https://www.blockaway.net",
        2: "https://www.croxyproxy.com",
        3: "https://www.croxyproxy.rocks",
        4: "https://www.croxy.network",
        5: "https://www.croxy.org",
        6: "https://www.youtubeunblocked.live",
        7: "https://www.croxyproxy.net",
    }

    # Selecting proxy server
    print(Colors.green,"Proxy Server 1 Is Recommended")
    print(Colorate.Vertical(Colors.green_to_blue,"Please select a proxy server(1,2,3..):"))
    for i in range(1, 8):
        print(Colorate.Vertical(Colors.red_to_blue,f"Proxy Server {i}"))
    
    while True:
        try:
            user_input = input("> ")
            if not user_input:  # Handle EOF or empty input
                print(Colorate.Vertical(Colors.red_to_blue,"Using default proxy server 1"))
                proxy_choice = 1
                break
            
            user_input = user_input.strip()
            proxy_choice = int(user_input)
            
            if 1 <= proxy_choice <= 7:
                break
            else:
                print(Colorate.Vertical(Colors.red_to_blue,"Please enter a number between 1 and 7"))
        except ValueError:
            print(Colorate.Vertical(Colors.red_to_blue,"Please enter a valid number"))
        except EOFError:  # Handle piped input
            print(Colorate.Vertical(Colors.red_to_blue,"Using default proxy server 1"))
            proxy_choice = 1
            break
    
    proxy_url = proxy_servers.get(proxy_choice)

    try:
        twitch_username = input(Colorate.Vertical(Colors.green_to_blue, "Enter your channel name (e.g brentonandtheboys): "))
        if not twitch_username.strip():
            raise EOFError
    except EOFError:
        # Read from autosettings.txt as fallback
        try:
            with open('autosettings.txt', 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    twitch_username = lines[1].strip()
                    print(Colorate.Vertical(Colors.green_to_blue, f"Using channel: {twitch_username}"))
                else:
                    print(Colorate.Vertical(Colors.red_to_blue, "Error: Could not read channel from autosettings.txt"))
                    return
        except FileNotFoundError:
            print(Colorate.Vertical(Colors.red_to_blue, "Error: autosettings.txt not found"))
            return

    try:
        proxy_count = input(Colorate.Vertical(Colors.cyan_to_blue, "How many proxy sites do you want to open? (Viewer to send)"))
        if not proxy_count.strip():
            raise EOFError
        proxy_count = int(proxy_count)
        if proxy_count <= 0:
            raise ValueError("Viewer count must be positive")
    except (ValueError, EOFError):
        # Read from autosettings.txt as fallback
        try:
            with open('autosettings.txt', 'r') as f:
                lines = f.readlines()
                if len(lines) >= 3:
                    proxy_count_str = next((line.strip() for line in lines if line.strip().isdigit()), None)
                    if proxy_count_str is None:
                        raise ValueError("No valid viewer count found in autosettings.txt")
                    proxy_count = int(proxy_count_str)
                    if proxy_count <= 0:
                        raise ValueError("Viewer count must be positive")
                    print(Colorate.Vertical(Colors.cyan_to_blue, f"Using viewer count: {proxy_count}"))
                else:
                    print(Colorate.Vertical(Colors.red_to_blue, "Error: Could not read viewer count from autosettings.txt"))
                    return
        except (FileNotFoundError, ValueError) as e:
            print(Colorate.Vertical(Colors.red_to_blue, f"Error: Could not read valid viewer count - {str(e)}"))
            return

    # Ask for repeat mode
    try:
        repeat_mode = input(Colorate.Vertical(Colors.cyan_to_blue, "Do you want to run in repeat mode? (y/n): ")).strip().lower()
        repeat = repeat_mode.startswith('y')
    except EOFError:
        repeat = False

    os.system("cls")
    print(Colorate.Vertical(Colors.green_to_cyan, Center.XCenter("""
████████╗██╗    ██╗██╗████████╗ ██████╗██╗  ██╗     ██████╗ ██████╗  ██████╗ ██╗  ██╗███████╗██████╗ 
╚══██╔══╝██║    ██║██║╚══██╔══╝██╔════╝██║  ██║    ██╔════╝██╔═══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗
   ██║   ██║ █╗ ██║██║   ██║   ██║     ███████║    ██║     ██║   ██║██║   ██║█████╔╝ █████╗  ██████╔╝
   ██║   ██║███╗██║██║   ██║   ██║     ██╔══██║    ██║     ██║   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
   ██║   ╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║    ╚██████╗╚██████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║
   ╚═╝    ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝""")))
    print('')
    print('')
    print(Colors.red, Center.XCenter("Viewers Sent. Please don't hurry. If the viewers does not arrive, turn it off and on and do the same operations"))


    chrome_path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    driver_path = 'chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument('--disable-dev-shm-usage')
    #ADBLOCK EXT
    extension_path = 'adblock.crx'
    chrome_options.add_extension(extension_path)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(proxy_url)

    for i in range(proxy_count):
        driver.execute_script("window.open('" + proxy_url + "')")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(proxy_url)

        text_box = driver.find_element(By.ID, 'url')
        text_box.send_keys(f'www.twitch.tv/{twitch_username}')
        text_box.send_keys(Keys.RETURN)

    if repeat:
        print(Colorate.Vertical(Colors.green_to_blue, "Running in repeat mode. Press Ctrl+C to stop."))
        try:
            while True:
                time.sleep(3600)  # Wait for 1 hour
                driver.refresh()  # Refresh all tabs
        except KeyboardInterrupt:
            print(Colorate.Vertical(Colors.red_to_blue, "\nStopping repeat mode..."))
    else:
        print(Colorate.Vertical(Colors.red_to_blue, "Viewers have all been sent. Withdrawing views and closing program..."))
        time.sleep(2)  # Give user time to read the message
    
    driver.quit()


if __name__ == '__main__':
    main()
