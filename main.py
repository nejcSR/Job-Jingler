from tools.scraper import scrape_remoteok
from agent.orchestrator import decide
from agent.writer import write_outreach
from db.crud import save_posting, save_decision, save_note, posting_exists
from tools.notifier import send_alert

MIN_FLAG_SCORE = 0.5  #flags scoring below this are saved but not sent to Discord


def run(limit: int = 10) -> None:
    """One full cycle: scrape -> skip seen jobs -> judge -> save -> alert."""

    postings = scrape_remoteok(limit=limit)
    print(f"Scraped {len(postings)} postings")

    new_count = 0

    for posting in postings:
        if posting_exists(posting.url):
            continue

        new_count += 1
        posting.id = save_posting(posting)

        result = decide(posting)
        save_decision(result)

        note = None
        if result.decision.value == "draft":
            try:
                note = write_outreach(posting, result.reasoning)
                save_note(posting.id, note)
            except Exception as e:
                print(f"Could not write a note for {posting.title}: {e}")

        should_alert = result.decision.value == "draft" or (
            result.decision.value == "flag" and (result.fit_score or 0) >= MIN_FLAG_SCORE
        )
        if should_alert:
            send_alert(posting, result, note)

        print(f"{result.decision.value:5} | {result.fit_score} | {posting.title} ({posting.company})")

    print(f"Done. {new_count} new postings processed.")


if __name__ == "__main__":
    run()