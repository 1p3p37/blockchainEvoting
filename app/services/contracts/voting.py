import logging

from sqlalchemy.orm import Session
from web3.contract import Contract, EventData

# inside crud is "voting = CRUD(models.Voting)"
from app import abi, crud, models
from app.core.config import EthereumSettings

# from app.crud.crud_voting import CRUDVoting
from app.models import Voting, Option, VotingOwner, Vote


class VotingContract:
    logger = logging.getLogger("voting_contract")

    def __init__(self, network: EthereumSettings) -> None:
        self.network = network
        self.w3_contract: Contract = self.network.w3.eth.contract(
            address=self.network.voting_contract_address,
            abi=abi.VOTING,
        )

    def handle_voting_created_event(self, db: Session, event: EventData):
        tx_hash = event["transactionHash"]
        args = event["args"]
        vote_name = args["voteName"]
        start_time = args["startTime"]
        end_time = args["endTime"]
        options_list = args["options"]
        owner_permission_list = args["ownerPermissionList"]

        # Check if voting already exists in database
        voting = db.query(Voting).filter_by(name=vote_name).first()

        # If voting doesn't exist, create a new one and add it to the database
        if not voting:
            voting = Voting(
                tx_hash=tx_hash,
                name=vote_name,
                start_time=start_time,
                end_time=end_time,
            )
            db.add(voting)
            db.commit()

            # Add options to voting
            for option_name in options_list:
                option = Option(name=option_name, voting_id=voting.id)
                db.add(option)

            # Add owners to voting
            for owner_address in owner_permission_list:
                owner = VotingOwner(owner_address=owner_address, voting_id=voting.id)
                db.add(owner)

            db.commit()
        else:
            self.logger.warning(f"Voting with name {vote_name} already exists.")

    def handle_vote_casted(self, db: Session, event: EventData):
        tx_hash = event["transactionHash"]
        args = event["args"]
        vote_name = args["voteName"]
        voter_address = args["voter"]
        voted_for = args["votedFor"]
        is_revote = args["isRevote"]
        block_number = event.blockNumber

        # check if the voting exists
        voting = crud.voting.get_by_name(db, name=vote_name)
        if not voting:
            self.logger.error(f"Voting {vote_name} not found")
            return

        # check if the option exists
        option = (
            db.query(Option)
            .filter(Option.name == voted_for, Option.voting_id == voting.id)
            .first()
        )
        if not option:
            self.logger.error(
                f"Option {voted_for} not found for voting {vote_name} and this voting id {voting.id}"
            )
            print(option)
            return

        # create or update the vote
        vote_data = {
            "voting_id": voting.id,
            "option_id": option.id,
            "tx_hash": str(tx_hash.hex()),
            "voter_address": voter_address,
            "voted_for": voted_for,
            "is_revote": is_revote,
            "block_number": block_number,
        }
        vote_in_db = crud.vote.get_by_votingId_and_address(
            db, voting_id=voting.id, voter_address=voter_address
        )
        if vote_in_db:
            # update the existing vote
            crud.vote.update(db, db_obj=vote_in_db, obj_in=vote_data)
        else:
            # create a new vote
            # vote = Vote(**vote_data)
            crud.vote.create(db, obj_in=vote_data)

        # update the vote counts for the option
        # option.vote_counts += 1
        # crud.option.update(db, db_obj=option)

        # commit the changes
        # db.commit()

        # for i in options_list:
        #     for i in owner_PermissionList:
        #         crud.voting.get_or_create(
        #             db,
        #             obj_in={

        #             }
        #         )

        # # address_list = args["_users"]
        # # voing_for_list = args["_amounts"]
        # for address, voting_for in zip(address_list, voing_for_list):
        #     crud.voting.get_or_create(
        #         db,
        #         obj_in={
        #             "user_address": address,
        #             "amount": voting_for,
        #             "tx_hash": tx_hash,
        #         },
        #     )

        """
        event VotingCreated(
        string voteName,
        uint256 startTime,
        uint256 endTime,
        string[] options,
        address[] ownerPermissionList
        """
