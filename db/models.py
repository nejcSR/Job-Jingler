from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class PostingModel(Base):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    url = Column(String, nullable=False)
    description = Column(String)
    source = Column(String)
    scraped_at = Column(DateTime, default=datetime.now)


class DecisionModel(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True)
    posting_id = Column(Integer, nullable=False)
    decision = Column(String, nullable=False)
    reasoning = Column(String)
    fit_score = Column(Float)
    decided_at = Column(DateTime, default=datetime.now)


# ADDED: one saved cover note per row, linked to its posting by posting_id
class NoteModel(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    posting_id = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(String, nullable=False)
    status = Column(String, default="new")  # for later, e.g. "new" / "applied"
    created_at = Column(DateTime, default=datetime.now)