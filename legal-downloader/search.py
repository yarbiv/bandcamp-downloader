import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()

def search_rutracker(artist, album, cookie):
    SESSION.cookies.set("bb_session", cookie, domain="rutracker.org")
    query = f"{artist} {album}"
    r = SESSION.post("https://rutracker.org/forum/tracker.php", data={"nm": query})
    soup = BeautifulSoup(r.text, "html.parser")

    results = []

    # Only filter live albums if the artist or album doesn't contain 'live'
    filter_out_live = "live" not in artist.lower() and "live" not in album.lower()

    for row in soup.select("tr.hl-tr"):
        topic_id = row.get("data-topic_id")
        title_tag = row.select_one("a.tLink")
        seeds_tag = row.select_one("td b.seedmed")
        size_tag = row.select_one("a.tr-dl")

        number, format, _ = size_tag.text.strip().split() if size_tag else ("0", "B")
        if format == "GB":
            size = 1e9 * float(number)
        elif format == "MB":
            size = 1e6 * float(number)
        elif format == "KB":
            size = 1e3 * float(number)

        if topic_id and title_tag:
            title = title_tag.text.strip()
            if filter_out_live and "live" in title.lower():
                print(f"Skipping live album: {title}")
                continue
            if "tracks" not in title.lower():
                print(f"Skipping non-tracks: {title}")
                continue
            results.append({
                "name": title_tag.text.strip(),
                "topic_id": topic_id,
                "seeds": seeds_tag.text.strip() if seeds_tag else "0",
                "size": size,
                "pretty_size": number + format
            })

    return min(results, key=lambda r: r["size"]) if results else None

def get_magnet(topic_id):
    r = SESSION.get(f"https://rutracker.org/forum/viewtopic.php?t={topic_id}")
    soup = BeautifulSoup(r.text, "html.parser")
    magnet = soup.select_one("a.magnet-link")
    return magnet["href"] if magnet else None

