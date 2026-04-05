import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()

def search_rutracker(artist, album, cookie):
    SESSION.cookies.set("bb_session", cookie, domain="rutracker.org")
    query = f"{artist} {album}"
    r = SESSION.post("https://rutracker.org/forum/tracker.php", data={"nm": query})
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for row in soup.select("tr.hl-tr"):
        topic_id = row.get("data-topic_id")
        title_tag = row.select_one("a.tLink")
        seeds_tag = row.select_one("td b.seedmed")

        if topic_id and title_tag:
            results.append({
                "name": title_tag.text.strip(),
                "topic_id": topic_id,
                "seeds": seeds_tag.text.strip() if seeds_tag else "0",
            })

    return results

def get_magnet(topic_id):
    r = SESSION.get(f"https://rutracker.org/forum/viewtopic.php?t={topic_id}")
    soup = BeautifulSoup(r.text, "html.parser")
    magnet = soup.select_one("a.magnet-link")
    return magnet["href"] if magnet else None

