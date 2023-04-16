from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from app.utils import decimal_to_str


class VoteInDB(BaseModel):
    id: int
    voting_id: int
    option_id: int
    voter_address: str
    block_number: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# '''
# id = Column(Integer, primary_key=True, index=True)
# voting_id = Column(Integer, ForeignKey("voting.id"))
# tx_hash = Column(String, unique=True, nullable=False, server_default=text("random()"))
# voting = relationship("Voting", back_populates="votes")
# option_id = Column(Integer, ForeignKey("option.id"))
# option = relationship("Option")
# voter_address = Column(String)
# voted_for = Column(String)
# is_revote = Column(Boolean, default=False)
# block_number = Column(Integer)
# '''
