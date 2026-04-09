import argparse
import datetime
import os
import subprocess

from dotenv import load_dotenv

import login
import search
import torbox

def download(artist, album):
    load_dotenv()

    torbox_api_key = os.getenv("TORBOX_API_KEY")

    cookie = login.get_cookie()
    results = search.search_rutracker(artist, album, cookie)
    magnet = search.get_magnet(results[0]["topic_id"])
    torrent_id = torbox.create_torrent(magnet, torbox_api_key).get("torrent_id")
    url = torbox.get_torrent_url(torrent_id, torbox_api_key)
    torbox.download_and_extract_torrent(url)

    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # beet import -m ~/music/ -q -l ~/log/<path> ~/bandcamp-downloader/music/downloads
    subprocess.run(["beet", "import", "-m", "~/music/", "-q", "-l", f"~/log/{datetime_str}", "~/bandcamp-downloader/music/downloads"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artist", required=True, help="Artist name to search for")
    parser.add_argument("--album", required=True, help="Album name to search for")
    args = parser.parse_args()

    if not args.artist or not args.album:
        print("Artist and album are required")
        exit(1)
    download(args.artist, args.album)