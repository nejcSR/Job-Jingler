import json
import os
from groq import Groq
from dotenv import load_dotenv
from agent.schemas import Posting, Decision, DecisionType
from agent.prompts import SYSTEM_PROMPT, build_user_prompt

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def _strip_code_fences(text: str) ->str:
    """Models sometimes wrap JSON in ```json ... ``` even when told not to."""
    text = text.strip()
    if text.startswith("'''"):
        text=text.split("'''")[0]
        if text.startswith("json"):
            text=text[4:]
    return text.strip()

def decide(posting: Posting) -> Decision:
    """Send a posting to the LLM and return its decision as a validated Decision object."""
    
    response= client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(posting)},
        ],
    )
    
    raw_text=response.choices[0].message.content
    cleaned_text=_strip_code_fences(raw_text)
    
    try:
        data=json.loads(cleaned_text)
    except json.JSONDecodeError:
        raise ValueError(f"Model did not return valid JSON:\n{raw_text}")
    return Decision(
        posting_id=posting.id or 0,
        decision=DecisionType(data["decision"]),
        reasoning=data["reasoning"],
        fit_score=data.get("fit_score"),
    )
