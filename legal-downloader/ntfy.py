import json
import os

from dotenv import load_dotenv
import requests

import legal_download

import threading

load_dotenv()

listen_code = os.getenv("NTFY_LISTEN")
notify_code = os.getenv("NTFY_NOTIFY")
simple_auth = os.getenv("NTFY_AUTH")

def download_album(artist, album):
    try:
        album_artist_string = legal_download.download(artist, album)
        requests.post(f"https://ntfy.sh/{notify_code}", data=f"{album_artist_string} is now available on Navidrome",
                        headers={"Content-Type": "text/plain; charset=utf-8"})
        print(f"Download of {album_artist_string} completed successfully")
    except Exception as e:
        print(f"Error downloading {artist} - {album}: {str(e)}")
        requests.post(f"https://ntfy.sh/{notify_code}", data=f"Failed to download {artist} - {album}: {str(e)}")

def listen():
    resp = requests.get(f"https://ntfy.sh/{listen_code}/json", stream=True)
    for line in resp.iter_lines(decode_unicode=True):
        if not line:
            continue
        line = json.loads(line)
        print(line)
        msg_str = line.get("message", "")
        if not msg_str:
            print("No message field in notification, ignoring")
            continue
        msg = json.loads(msg_str)
        token = msg.get("simple_auth", "")
        print(msg)
        if token != simple_auth:
            print("Unauthorized notification received, ignoring")
            continue
        print("Authorized notification received, processing...")
        artist = msg.get("artist", "")
        album = msg.get("album", "")
        if not artist or not album:
            print("Artist or album field missing in notification, ignoring")
            continue
        print(f"Downloading {artist} - {album}...")
        threading.Thread(target=download_album, args=(artist, album)).start()

while True:
    try:
        listen()
    except Exception as e:
        print(f"Error in listen loop: {str(e)}")