from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

# This points at a single file called job_hunt.db, in your project root.
# SQLite creates this file automatically the first time it's used.
engine=create_engine("sqlite:///job_hunt.db")

# This actually builds the tables (postings, decisions) inside that file,
# based on the shapes we defined in models.py. Safe to run every time —
# it only creates tables that don't already exist, never overwrites data.
Base.metadata.create_all(engine)

# A "session" is how your code talks to the database — opening one lets
# you add, read, or update rows. SessionLocal is a factory for making one
# whenever you need it.
SessionLocal = sessionmaker(bind=engine)