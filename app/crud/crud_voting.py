from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.crud.base import CRUD
from app import models
from app import schemas


class CRUDVoting(CRUD):
    def get_by_name(self, db: Session, name: str) -> models.Voting | None:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_all_votings(self, db: Session) -> List[Dict[str, any]]:
        votings = db.query(models.Voting).all()
        result = []
        for voting in votings:
            pre_result = []
            options = (
                db.query(models.Option.name)
                .filter(models.Option.voting_id == voting.id)
                .all()
            )
            option_names = [option.name for option in options]

            # Convert the SQLAlchemy Voting model to a Pydantic Voting model
            pydantic_voting = schemas.VotingInDB.from_orm(voting)

            pre_result.append(pydantic_voting.dict())
            pre_result.append({"options": option_names})
            result.append(pre_result)
        return result


class CRUDVote(CRUD):
    def get_by_votingId_and_address(
        self, db: Session, voting_id: int, voter_address: str
    ) -> models.Vote | None:
        return (
            db.query(self.model)
            .filter(
                self.model.voting_id == voting_id,
                self.model.voter_address == voter_address,
            )
            .first()
        )

    def get_total_values(self, db: Session, voting: models.Voting) -> int | None:
        total_votes = (
            db.query(models.Vote).filter(models.Vote.voting_id == voting.id).count()
        )
        return total_votes

    def get_all_votes_by_voting_name(
        self, db: Session, voting_name: str
    ) -> List[Dict[str, any]]:
        votes = (
            db.query(models.Vote)
            .join(models.Option, models.Option.id == models.Vote.option_id)
            .join(models.Voting, models.Voting.id == models.Option.voting_id)
            .filter(models.Voting.name == voting_name)
            .order_by(
                models.Vote.is_revote.desc(),
                models.Vote.voted_for,
                models.Vote.block_number,
            )
            .all()
        )

        # Convert the SQLAlchemy Vote models to a list of Pydantic VoteInDB models
        pydantic_votes = [schemas.VoteInDB.from_orm(vote).dict() for vote in votes]

        return pydantic_votes

    def get_score_by_name(self, db: Session, voting_name: str) -> List:
        voting = (
            db.query(models.Voting).filter(models.Voting.name == voting_name).first()
        )
        if not voting:
            return []

        options = (
            db.query(models.Option).filter(models.Option.voting_id == voting.id).all()
        )

        scores = []
        for option in options:
            votes_count = (
                db.query(models.Vote)
                .filter(
                    models.Vote.voting_id == voting.id,
                    models.Vote.option_id == option.id,
                )
                .count()
            )
            scores.append({option.name: votes_count})

        return scores


"""    
from app.api.endpoints.voting import *
db = Session(Depends(deps.get_db))
crud.vote.get_all_votes_by_voting_name(db,"s")
"""
voting = CRUDVoting(models.Voting)
vote = CRUDVote(models.Vote)
option = CRUD(models.Option)
