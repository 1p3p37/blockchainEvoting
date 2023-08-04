from datetime import datetime
from pydantic import BaseModel


class VoteInDB(BaseModel):
    id: int
    voting_id: int
    option_id: int
    tx_hash: str | None
    voter_address: str
    voted_for: str
    block_number: int
    created_at: datetime | None
    is_revote: bool

    class Config:
        orm_mode = True


class VotingInDB(BaseModel):
    tx_hash: str | None
    id: int
    name: str
    start_time: int
    end_time: int

    class Config:
        orm_mode = True
