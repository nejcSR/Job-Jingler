import os
import requests
from dotenv import load_dotenv

from agent.schemas import Posting, Decision

load_dotenv()

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")


def _post(text: str) -> None:
    if not WEBHOOK_URL:
        return
        
    response = requests.post(WEBHOOK_URL, json={"content": text}, timeout=10)

    # Raise or loudly print if Discord rejects it
    if response.status_code not in (200, 204):
        print(f"❌ Discord alert failed [{response.status_code}]: {response.text}")
    else:
        print("Successfully posted to Discord.")


def send_alert(posting: Posting, decision: Decision, note: dict | None = None) -> None:
    """Send one job + the agent's verdict to Discord, plus the cover note if there is one."""

    if not WEBHOOK_URL:
        print("No DISCORD_WEBHOOK_URL found in .env, skipping alert.")
        return

    # Optional: If you want an actual sound/ping notification, you can prepend your user ID 
    # e.g., ping_tag = "<@YOUR_DISCORD_USER_ID>\n" but keeping it clean for now:
    
    main_message = (
        f"**{decision.decision.value.upper()}** ({decision.fit_score}): "
        f"{posting.title} at {posting.company}\n"
        f"{decision.reasoning}\n"
        f"{posting.url}"
    )
    _post(main_message)

    if note:
        # Ensure the body doesn't break Discord's 2000 char limit inside code blocks
        body = note['body']
        if len(body) > 1800:
            body = body[:1800] + "\n[...truncated due to length...]"

        note_message = f"**Cover note draft**\n**Subject:** {note['subject']}\n```text\n{body}\n```"
        _post(note_message)