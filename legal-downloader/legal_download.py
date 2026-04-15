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
    torrent_link = search.search_rutracker(artist, album, cookie)
    print(torrent_link)
    if torrent_link is None:
        raise Exception(f"No torrent found for {album} by {artist}")
    magnet = search.get_magnet(torrent_link["topic_id"])
    torrent_id = torbox.create_torrent(magnet, torbox_api_key).get("torrent_id")
    url = torbox.get_torrent_url(torrent_id, torbox_api_key)
    torbox.download_and_extract_torrent(url)

    datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # beet import -m ~/music/ -q -l ~/log/<path> ~/bandcamp-downloader/music/downloads
    subprocess.run(["beet", "import", "-m", "~/music/", "-q", "-l", f"~/log/{datetime_str}", "~/bandcamp-downloader/music/downloads"])

    # Check that beets actually managed to import the album
    #  beet ls -af '$album - $albumartist' 
    result = subprocess.check_output(["beet", "ls", "-af", "$album - $albumartist", album, artist], text=True)
    # this is newline separated, so split it and check if the length is 1, then we drop the empty string
    album_artist_strings = [s for s in result.split("\n") if s]
    if len(album_artist_strings) == 1:
        return f"{album_artist_strings[0]} ({torrent_link['pretty_size']})"
    elif len(album_artist_strings) == 0:
        raise Exception(f"Requested download ({album} by {artist}) failed to download or import.")
    else:
        raise Exception(f"Multiple albums found for {album} by {artist} after import: {album_artist_strings}. That's weird!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--artist", required=True, help="Artist name to search for")
    parser.add_argument("--album", required=True, help="Album name to search for")
    args = parser.parse_args()

    if not args.artist or not args.album:
        print("Artist and album are required")
        exit(1)
    download(args.artist, args.album)