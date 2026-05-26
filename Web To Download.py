# ====================
#        Imports
# ====================

import os
import sys
import requests
import tkinter as tk
from tkinter import filedialog, messagebox
from urllib.parse import urlparse


# ====================
#        ASCII Title
# ====================

ASCII_TITLE = r"""
 __          __  _               __     _____                      _                 _ 
 \ \        / / | |              \ \   |  __ \                    | |               | |
  \ \  /\  / /__| |__    ______   \ \  | |  | | _____      ___ __ | | ___   __ _  __| |
   \ \/  \/ / _ \ '_ \  |______|   > > | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |
    \  /\  /  __/ |_) |           / /  | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |
     \/  \/ \___|_.__/           /_/   |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|
"""


# ====================
#        Settings
# ====================

CMD_TITLE = "Web Download"
TIMEOUT_SECONDS = 25

GAME_DOWNLOADS = {
    "1": {
        "name": "8 Ball Pool",
        "url": "https://raw.githubusercontent.com/Dilliam4444/Dodgy-School-Games/main/improved_8_ball_pool_beta.html",
        "filename": "8_ball_pool.html"
    },
    "2": {
        "name": "Neon Drift 3D Beta",
        "url": "https://raw.githubusercontent.com/Dilliam4444/Dodgy-School-Games/main/neon_drift_3d.html",
        "filename": "neon_drift_3d_beta.html"
    }
}


# ====================
#        Popups
# ====================

def popup_info(title, message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(title, message)
    root.destroy()


def popup_error(title, message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showerror(title, message)
    root.destroy()


# ====================
#        CMD Tools
# ====================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    print()
    input("Press Enter to continue...")


def show_title():
    clear_screen()
    print(ASCII_TITLE)
    print("=" * 88)


# ====================
#        URL Tools
# ====================

def clean_url(url):
    url = url.strip()

    if not url:
        return None

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.netloc:
        return None

    return url


def get_default_filename(url):
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    domain = domain.replace(".", "_")

    if not domain:
        return "downloaded_website.html"

    return f"{domain}.html"


# ====================
#        Download Tools
# ====================

def download_text(url):
    session = requests.Session()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.9",
        "Connection": "keep-alive"
    }

    response = session.get(
        url,
        headers=headers,
        timeout=TIMEOUT_SECONDS,
        allow_redirects=True
    )

    response.raise_for_status()
    return response.text


def choose_save_path(default_name):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    save_path = filedialog.asksaveasfilename(
        title="Save File",
        initialfile=default_name,
        defaultextension=".html",
        filetypes=[
            ("HTML File", "*.html"),
            ("Text File", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    root.destroy()
    return save_path


def save_html_file(content, default_name):
    save_path = choose_save_path(default_name)

    if not save_path:
        print("Save cancelled.")
        return False

    try:
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(content)

        print("Saved.")
        print(save_path)
        popup_info("Complete", "Complete")
        return True

    except Exception as error:
        popup_error("Error", f"Could not save the file.\n\n{error}")
        return False


# ====================
#        Error Handler
# ====================

def handle_download_error(error):
    if isinstance(error, requests.exceptions.Timeout):
        popup_error("Error", "The website took too long to respond.")

    elif isinstance(error, requests.exceptions.ConnectionError):
        popup_error("Error", "Could not connect. It may be blocked or offline.")

    elif isinstance(error, requests.exceptions.HTTPError):
        code = error.response.status_code

        if code == 403:
            popup_error("Error", "Access refused. The website blocked the request.")
        elif code == 404:
            popup_error("Error", "File or page not found.")
        elif code == 429:
            popup_error("Error", "Too many requests. Try again later.")
        else:
            popup_error("Error", f"The request failed.\n\nCode: {code}")

    else:
        popup_error("Error", f"Something went wrong.\n\n{error}")


# ====================
#        Game Downloads
# ====================

def download_game(choice):
    game = GAME_DOWNLOADS[choice]

    show_title()
    print(f"Downloading {game['name']}...")
    print()

    try:
        html = download_text(game["url"])
    except Exception as error:
        handle_download_error(error)
        pause()
        return

    print("Downloaded.")
    print("Opening Save As window...")
    print()

    save_html_file(html, game["filename"])
    pause()


# ====================
#        Web to HTML
# ====================

def web_to_html():
    show_title()
    print("Web -> HTML Downloader")
    print("=" * 88)
    print("Paste a website URL below.")
    print("This saves the page HTML only.")
    print("It will not bypass blocked websites.")
    print("=" * 88)
    print()

    url_input = input("Website URL: ")
    url = clean_url(url_input)

    if not url:
        popup_error("Error", "That URL is not valid.")
        pause()
        return

    print()
    print("Loading website...")
    print(url)
    print()

    try:
        html = download_text(url)
    except Exception as error:
        handle_download_error(error)
        pause()
        return

    print("Website loaded.")
    print("Opening Save As window...")
    print()

    default_name = get_default_filename(url)
    save_html_file(html, default_name)

    pause()


# ====================
#        Menu
# ====================

def show_menu():
    show_title()
    print("Choose an option:")
    print()
    print("[1] Download 8 Ball Pool")
    print("[2] Download Neon Drift 3D Beta")
    print("[3] Web -> Download HTML")
    print("[4] Exit")
    print()
    print("=" * 88)


def main():
    os.system(f"title {CMD_TITLE}")

    while True:
        show_menu()

        choice = input("Option: ").strip()

        if choice == "1":
            download_game("1")

        elif choice == "2":
            download_game("2")

        elif choice == "3":
            web_to_html()

        elif choice == "4":
            print("Closing...")
            sys.exit()

        else:
            popup_error("Error", "That is not a valid option.")
            pause()


# ====================
#        Start
# ====================

if __name__ == "__main__":
    main()