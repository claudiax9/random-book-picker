import random
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests
import xml.etree.ElementTree as ET

# goodreads shelf link
GOODREADS_SHELF_URL = "https://www.goodreads.com/review/list/71547653-claudia?shelf=2026-tbr"

def shelf_url_to_rss_url(shelf_url: str) -> str:
    """Convert a Goodreads shelf URL to its RSS feed URL."""

    shelf_url = shelf_url.strip()
    parsed_url = urlparse(shelf_url)

    # convert /review/list/ to /review/list_rss/
    rss_path = parsed_url.path.replace("/review/list/", "/review/list_rss/", 1)

    # normalize to /review/list_rss/<user_id>
    match = re.match(r"^/review/list_rss/(\d+)(?:-[^/]+)?$", rss_path)
    if match:
        rss_path = f"/review/list_rss/{match.group(1)}"

    query_params = parse_qs(parsed_url.query)
    if "shelf" not in query_params:
        raise ValueError('The link does not contain the required "?shelf=..." parameter (e.g., shelf=2026-tbr).lf=tbr-2026).')

    rss_query = urlencode(query_params, doseq=True)

    scheme = parsed_url.scheme or "https"
    netloc = parsed_url.netloc or "www.goodreads.com"

    return urlunparse((scheme, netloc, rss_path, "", rss_query, ""))

def fetch_books_from_rss(rss_url: str) -> list[dict]:
    """Fetch and parse book entries from a Goodreads RSS feed."""

    headers = {
        "User-Agent": "Mozilla/5.0 (BookPicker/1.0; personal use)",
        "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.7",
    }
    response = requests.get(rss_url, headers=headers, timeout=20)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    channel = root.find("channel")
    if channel is None:
        raise RuntimeError(
            "Could not find <channel> in the RSS feed. You may have received a login page or an error response."
        )

    books = []
    for item in channel.findall("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        author_name = (item.findtext("author_name") or "").strip()

        if title and link:
            books.append({"title": title, "link": link, "author": author_name or None})

    return books

def pick_random_book_from_shelf(shelf_url: str) -> dict:
    """Pick a random book from a Goodreads shelf."""

    rss_url = shelf_url_to_rss_url(shelf_url)
    books = fetch_books_from_rss(rss_url)

    if not books:
        raise RuntimeError(
            "No books found in the feed. Please double-check the shelf URL and its access settings."
        )

    return random.choice(books)

if __name__ == "__main__":
    if GOODREADS_SHELF_URL == "PASTE_LINK_HERE":
        raise SystemExit(
            'Please paste your shelf link into GOODREADS_SHELF_URL (replace "PASTE_LINK_HERE").'
        )

    chosen_book = pick_random_book_from_shelf(GOODREADS_SHELF_URL)

    print("\n🎲 Randomly selected book:")
    if chosen_book.get("author"):
        print(f"  {chosen_book['title']} — {chosen_book['author']}")
    else:
        print(f"  {chosen_book['title']}")
    print(f"  Link: {chosen_book['link']}")
