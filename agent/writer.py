import json
import os
from dotenv import load_dotenv
from groq import Groq

from agent.schemas import Posting
from agent.orchestrator import _strip_code_fences  # reuse the JSON clean-up we already wrote

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

YOUR_NAME = "Nejc"  # change this to the name you want at the bottom of emails

# CHANGED: three new rules in RULES below (complete first sentence, no "demonstrates/shows"
# or "agent" wording, and Google OAuth mentioned without explaining its purpose).
# The project facts are unchanged.
WRITER_PROMPT = f"""You write short, honest cover notes for a self-taught Python developer \
applying to Backend / AI Automation Engineer roles.

FACTS ABOUT THE CANDIDATE (use only these, never invent anything else)
- Name: {YOUR_NAME}
- GitHub: github.com/nejcSR
- Project 1, price-monitoring pipeline: Python, Playwright scraping with fallback \
logic for when a site's selectors break, FastAPI, PostgreSQL, Docker, alerts through webhooks.
- Project 2, email automation service (live on Render): async Python, LLM APIs to \
classify emails, Google OAuth, PostgreSQL, Docker, webhooks.
- Project 3, document intelligence system (live on Render): reads PDF, DOCX, TXT and \
images, Tesseract OCR, Llama via Groq for structured data extraction, FastAPI backend.

RULES
- 80 to 120 words. Plain, direct, no hype words like "passionate" or "excited".
- The first sentence must be a complete sentence that names the role and the company. \
Do not introduce the candidate by name at the start; the name only appears in the signature.
- Pick one or two projects that match this posting, and tie each to a specific \
requirement from the posting text.
- Describe each project separately, using only the technologies listed on that \
project's own line. Never write "both", "all" or "each" about several projects, and \
never move a technology from one project to another.
- Describe what each project does in plain factual terms. Never write sentences that \
start with "This demonstrates" or "This shows", and never call a project an "agent" \
or "AI agent".
- Mention Google OAuth only by name. Do not explain what it is used for.
- Do not claim the candidate is "comfortable with" or "experienced in" anything that \
is not named in the facts above.
- Do not mention measuring, testing, metrics, performance or improving models.
- Do not claim years of experience, degrees, or employers.
- Write two short paragraphs separated by a blank line. Then "Best regards," on its own \
line and the name on the next line.

OUTPUT FORMAT
Respond with ONLY a JSON object, no other text:
{{"subject": "<string>", "body": "<string>"}}
"""


def write_outreach(posting: Posting, reasoning: str) -> dict:
    """Write a cover note for one posting. Returns {"subject": ..., "body": ...}."""

    user_text = (
        f"Job: {posting.title} at {posting.company}\n"
        f"Why it fits (from the screening step): {reasoning}\n"
        f"Posting text: {posting.description[:3000]}"  # cut long postings to save tokens
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": WRITER_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )

    raw_text = response.choices[0].message.content
    cleaned = _strip_code_fences(raw_text)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        raise ValueError(f"Writer did not return valid JSON:\n{raw_text}")

    return {"subject": data["subject"], "body": data["body"]}