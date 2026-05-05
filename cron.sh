#!/bin/bash
set -e

LOGFILE="/var/log/bandcamp-downloader.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOGFILE"
}

log "=== Starting bandcamp sync ==="

/root/bandcamp-downloader/.venv/bin/python /root/bandcamp-downloader/bandcamp-downloader.py \
    --cookies /root/bandcamp-downloader/cookies/cookies.txt \
    --directory /root/bandcamp-downloader/music/downloads \
    --format mp3-320 \
    -v \
    --extract \
    --ntfy-topic slA41wTTTJj924eb \
    yarbiv >> "$LOGFILE" 2>&1

log "=== Starting beet import ==="

/root/bandcamp-downloader/.venv/bin/beet import -q /root/bandcamp-downloader/music/downloads >> "$LOGFILE" 2>&1

log "=== Done ==="