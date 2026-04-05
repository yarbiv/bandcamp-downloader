import search 
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def get_cookie():
    # First GET to grab any initial cookies
    load_dotenv()
    SESSION = requests.Session()
    SESSION.get("https://rutracker.org/forum/login.php")
    username = os.getenv("RU_USER")
    password = os.getenv("RU_PASS")

    r = SESSION.post("https://rutracker.org/forum/login.php", data={
        "login_username": username,
        "login_password": password,
        "login": "вход",
        "redirect": "index.php",
    })
    
    if "IS_GUEST: !!''" in r.text:  # logged in users have empty string here
        print("Login successful")
        bb_session = SESSION.cookies.get("bb_session", domain=".rutracker.org")
        return bb_session
    elif "cap_code" in r.text:
        print("CAPTCHA required")
    print(r.text)
    raise Exception("Login failed")
    