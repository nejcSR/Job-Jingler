from playwright.sync_api import sync_playwright
import json

from agent.schemas import Posting

SEARCH_URLS = [
    "https://remoteok.com/remote-python-jobs",
    "https://remoteok.com/remote-ai-jobs",
    "https://remoteok.com/remote-backend-jobs",
]


#this function scrapes ONE page.
def _scrape_page(page, url: str, limit: int) -> list[Posting]:
    """Scrape one RemoteOK listing page and return up to `limit` postings."""

    postings = []

    page.goto(url)
    page.wait_for_selector(
        "tr.job script[type='application/ld+json']", state="attached", timeout=20000
    )

    rows = page.query_selector_all("tr.job")
    skipped = 0

    for row in rows:
        if len(postings) >= limit:
            break

        script = row.query_selector("script[type='application/ld+json']")
        href = row.get_attribute("data-href")

        #href check, so a row with no link can't crash the run
        if not script or not href:
            skipped += 1
            continue

        try:
            data = json.loads(script.inner_text())
        except json.JSONDecodeError:
            skipped += 1
            continue

        postings.append(Posting(
            title=data.get("title", "Unknown title"),
            company=data.get("hiringOrganization", {}).get("name", "Unknown company"),
            url="https://remoteok.com" + href,
            description=data.get("description", ""),
            source="remoteok",
        ))

    print(f"{url}: {len(rows)} rows, {len(postings)} kept, {skipped} skipped")
    return postings


def scrape_remoteok(limit: int = 5, urls: list[str] | None = None) -> list[Posting]:
    """Scrape every page in SEARCH_URLS. `limit` is now the max PER PAGE."""

    urls = urls or SEARCH_URLS
    all_postings = []
    seen_urls = set()  #remembers jobs we already have, since one job can be on two pages

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(60000)

        for url in urls:
            try:
                found = _scrape_page(page, url, limit)
            except Exception as e:
                print(f"Could not scrape {url}: {e}")
                continue

            for posting in found:
                if posting.url not in seen_urls:
                    seen_urls.add(posting.url)
                    all_postings.append(posting)

        browser.close()

    return all_postings
