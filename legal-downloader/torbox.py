CREATE_TORRENT_URL = "https://api.torbox.app/v1/api/torrents/createtorrent"
DOWNLOAD_TORRENT_URL = "https://api.torbox.app/v1/api/torrents/requestdl"

import os
import time
import uuid

import requests
import zipfile

def create_torrent(magnet_link, torbox_api_key):
    resp = requests.post(CREATE_TORRENT_URL, headers={"Authorization": f"Bearer {torbox_api_key}"}, data={"magnet": magnet_link})
    return resp.json().get("data", {})

def get_torrent_url(torrent_id, torbox_api_key):
    resp = requests.get(DOWNLOAD_TORRENT_URL, params={"token": torbox_api_key, "torrent_id": torrent_id, "zip_link": True})
    while resp.json().get("success") != True:
        print("Torrent not ready yet, retrying in 10 seconds...")
        time.sleep(10)
        resp = requests.get(DOWNLOAD_TORRENT_URL, params={"token": torbox_api_key, "torrent_id": torrent_id, "zip_link": True})
    return resp.json().get("data")

def download_and_extract_torrent(url, output_path=None):
    resp = requests.get(url, stream=True)
    if output_path is None:
        output_path ="music/downloads/"

    # UUID ensures multiple torrents don't clobber each other
    file = f"download_{uuid.uuid4()}.zip"

    with open(file, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(output_path)
    
    print(f"Torrent downloaded and extracted to {output_path}")

    os.remove(file)

