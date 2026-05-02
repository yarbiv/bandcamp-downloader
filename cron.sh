#!/bin/bash
set -e
/root/bandcamp-downloader/.venv/bin/python /root/bandcamp-downloader/bandcamp-downloader.py \
    --cookies /root/bandcamp-downloader/cookies/cookies.txt \
    --directory /root/bandcamp-downloader/music/downloads \
    --format mp3-320 \
    -v \
    --extract \
    --ntfy-topic slA41wTTTJj924eb \
    yarbiv

/root/bandcamp-downloader/.venv/bin/beet import -m /root/music/ -q /root/bandcamp-downloader/music/downloads
