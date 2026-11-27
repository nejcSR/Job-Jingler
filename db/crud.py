from db.database import SessionLocal
from db.models import PostingModel, DecisionModel, NoteModel
from agent.schemas import Posting, Decision


def posting_exists(url: str) -> bool:
    """Check the database for a posting with this url."""
    session = SessionLocal()
    found = session.query(PostingModel).filter(PostingModel.url == url).first()
    session.close()
    return found is not None


def save_posting(posting: Posting) -> int:
    """Save a Posting into the database, and return its new database id."""
    session = SessionLocal()

    db_posting = PostingModel(
        title=posting.title,
        company=posting.company,
        url=posting.url,
        description=posting.description,
        source=posting.source,
    )

    session.add(db_posting)
    session.commit()
    session.refresh(db_posting)

    new_id = db_posting.id
    session.close()
    return new_id


def save_decision(decision: Decision) -> None:
    """Save a Decision into the database."""
    session = SessionLocal()

    db_decision = DecisionModel(
        posting_id=decision.posting_id,
        decision=decision.decision.value,
        reasoning=decision.reasoning,
        fit_score=decision.fit_score,
    )

    session.add(db_decision)
    session.commit()
    session.close()


#saves one cover note ({"subject": ..., "body": ...}) for a posting
def save_note(posting_id: int, note: dict) -> None:
    """Save a cover note into the database."""
    session = SessionLocal()

    db_note = NoteModel(
        posting_id=posting_id,
        subject=note["subject"],
        body=note["body"],
    )

    session.add(db_note)
    session.commit()
    session.close()
