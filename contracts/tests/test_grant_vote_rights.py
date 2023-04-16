import pytest
from brownie import Voting, accounts, reverts, web3

# import web3
from brownie.network.state import Chain
import brownie


@pytest.fixture
def vote():
    yield Voting.deploy({"from": accounts[0]})


def test_grant_vote_rights(vote):
    # Deploy the contract and create a vote
    vote.createVote(
        "Test Vote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option A", "Option B"],
        [accounts[1]],
        [accounts[0]],
    )

    # Attempt to grant voting rights before the voting period has started
    vote.grantVoteRights("Test Vote", [accounts[2]], {"from": accounts[0]})

    # Advance the blockchain timestamp to the start of the voting period
    Chain().sleep(3600)

    # Attempt to grant voting rights after the voting period has ended
    # assert vote.grantVoteRights("Test Vote", [accounts[2]], {'from': accounts[0]})

    # Grant voting rights to an account
    with reverts("Voting has ended"):
        vote.grantVoteRights("Test Vote", [accounts[2]], {"from": accounts[0]})

    # Ensure the account can cast a vote
    with reverts("Voting has ended"):
        vote.castVote("Test Vote", "Option A", {"from": accounts[2]})
    with reverts("You don't have permission to this vote"):
        assert vote.getScore("Test Vote", "Option A") == 1
