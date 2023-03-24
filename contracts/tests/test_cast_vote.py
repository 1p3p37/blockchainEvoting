import pytest
from brownie import MultiOptionStringVote, accounts, reverts, web3


@pytest.fixture
def vote():
    yield MultiOptionStringVote.deploy({"from": accounts[0]})


def test_cast_vote(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Cast a vote for Option 1
    vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    # Check that the vote count for Option 1 is now 1
    assert vote.getScore("MyVote", "Option1", {"from": accounts[1]}) == 1

    # Try to cast a vote for an option that does not exist


def test_cast_vote_invalid_option(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Try to cast a vote for Option 3 which does not exist
    with reverts("This option doesn't exist"):
        vote.castVote("MyVote", "Option3", {"from": accounts[1]})

    # Try to cast a vote without permission


def test_cast_vote_without_permission(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Try to cast a vote without permission
    with reverts("You don't have permission to vote"):
        vote.castVote("MyVote", "Option1", {"from": accounts[2]})

    # Try to cast a vote after the vote has ended


def test_cast_vote_inactive_vote(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp + 3600,
        web3.eth.get_block("latest").timestamp + 7200,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Try to cast a vote after the vote has ended
    with reverts("Voting has not yet started"):
        vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    # Test vote creation with endTime before startTime


def test_short_voting_period_vote(vote):
    assert vote.createVote(
        "ShortVotingPeriodVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 1,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )
