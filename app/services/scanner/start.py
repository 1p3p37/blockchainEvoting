from app import logs
from app.core.config import settings
from app.services.scanner.scanner import EventScanner

if __name__ == "__main__":
    logs.init()
    EventScanner(
        settings.ethereum,
        settings.ethereum.voting_contract.w3_contract.events.VotingCreated(),
        settings.ethereum.voting_contract.handle_voting_created_event,
    ).start()
    EventScanner(
        settings.ethereum,
        settings.ethereum.voting_contract.w3_contract.events.VoteCasted(),
        settings.ethereum.voting_contract.handle_vote_casted,
    ).start()
