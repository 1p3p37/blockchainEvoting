from app import models
from app.crud.base import CRUD
from collections import defaultdict
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Voting, Option, Vote
from typing import Dict, List, Tuple
from app.schemas import VoteInDB


class CRUDVoting(CRUD):
    def get_by_name(self, db: Session, name: str) -> Voting | None:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_all_votings(self, db: Session):
        votings = db.query(models.Voting).all()
        result = []
        for voting in votings:
            pre_result = []
            options = db.query(Option.name).filter(Option.voting_id == voting.id).all()
            option_names = [option.name for option in options]
            pre_result.append(voting)
            pre_result.append({"options": option_names})
            result.append(pre_result)
        return result


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

    def get_total_values(self, db: Session, voting: models.Voting) -> int | None:
        total_votes = db.query(Vote).filter(Vote.voting_id == voting.id).count()
        return total_votes

    def get_all_votes_by_voting_name(
        self, db: Session, voting_name: str
    ) -> List[models.Vote]:
        return (
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

    # def get_all_votes_by_voting_name(self,
    #         db: Session, voting_name: str
    # ) -> Tuple[Dict[str, Dict[str, List[VoteInDB]]], Dict[str, Dict[str, List[VoteInDB]]]]:
    #     votes = (
    #         db.query(models.Vote)
    #         .join(models.Option, models.Option.id == models.Vote.option_id)
    #         .join(models.Voting, models.Voting.id == models.Option.voting_id)
    #         # .join(models.Block, models.Block.number == models.Vote.block_number)
    #         .filter(models.Voting.name == voting_name)
    #         .order_by(models.Vote.is_revote.desc(), models.Vote.voted_for, models.Vote.block_number)
    #         .all()
    #     )

    #     result = {"is_vote": {}, "is_revote": {}}

    #     for vote in votes:
    #         vote_data = {
    #             "tx_hash": vote.tx_hash,
    #             "voting_id": vote.voting_id,
    #             "voter_address": vote.voter_address,
    #             "is_revote": vote.is_revote,
    #             "option_id": vote.option_id,
    #             "voted_for": vote.voted_for,
    #             "block_number": vote.block_number,
    #         }

    #         if vote.is_revote:
    #             if vote.voted_for not in result["is_revote"]:
    #                 result["is_revote"][vote.voted_for] = {}

    #             result["is_revote"][vote.voted_for][vote.block_number] = vote_data
    #         else:
    #             if vote.voted_for not in result["is_vote"]:
    #                 result["is_vote"][vote.voted_for] = {}

    #             result["is_vote"][vote.voted_for][vote.block_number] = vote_data

    #     return result


"""    
from app.api.endpoints.voting import *
db = Session(Depends(deps.get_db))
crud.vote.get_all_votes_by_voting_name(db,"s")
"""
voting = CRUDVoting(Voting)
vote = CRUDVote(Vote)
option = CRUD(Option)
