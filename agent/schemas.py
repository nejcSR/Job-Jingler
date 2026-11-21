from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class DecisionType(str, Enum):
    FLAG = "flag"
    DRAFT = "draft"
    SKIP = "skip"
    
class Posting(BaseModel):
    id: Optional[int]=None
    title: str
    company: str
    url: str
    description: str
    source: str
    scraped_at: datetime = datetime.now()
    
class Decision(BaseModel):
    posting_id: int
    decision: DecisionType
    reasoning: str
    fit_score: Optional[float]=None
    decided_at: datetime = datetime.now()