from app import models
from app.crud.base import CRUD
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Voting, Option, Vote
from typing import Dict, List


class CRUDVoting(CRUD):
    def get_by_name(self, db: Session, name: str) -> Voting | None:
        return db.query(self.model).filter(self.model.name == name).first()


class CRUDVote(CRUD):
    def get_by_votingId_and_address(
        self, db: Session, voting_id: int, voter_address: str
    ) -> Vote | None:
        return (
            db.query(self.model)
            .filter(
                self.model.voting_id == voting_id,
                self.model.voter_address == voter_address,
            )
            .first()
        )

    # def get_total_values_by_voting_name(
    #     self, db: Session, voting_name: str
    # ) -> int | None:
    #     voting = (
    #         db.query(self.model.voting)
    #         .filter(self.model.voting.name == voting_name)
    #         .first()
    #     )
    #     if not voting:
    #         return None
    #     total_votes = db.query(Vote).filter(Vote.voting_id == voting.id).count()
    #     return total_votes

    def get_all_votes_by_voting_name(
        self, db: Session, voting_name: str
    ) -> List[models.Vote]:
        return (
            db.query(models.Vote)
            .join(models.Option, models.Option.id == models.Vote.option_id)
            .join(models.Voting, models.Voting.id == models.Option.voting_id)
            .filter(models.Voting.name == voting_name)
            .all()
        )


"""    
from app.api.endpoints.voting import *
db = Session(Depends(deps.get_db))
crud.vote.get_all_votes_by_voting_name(db,"s")
"""
voting = CRUDVoting(Voting)
vote = CRUDVote(Vote)
option = CRUD(Option)
