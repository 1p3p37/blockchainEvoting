import pytest
from brownie import MultiOptionStringVote, accounts, reverts, web3


@pytest.fixture
def vote():
    yield MultiOptionStringVote.deploy({'from': accounts[0]})


def test_revote_success(vote):
    # Create a vote
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])

    # Cast initial vote
    vote.castVote("MyVote", "Option1", {'from': accounts[1]})

    # Re-vote for a different option
    vote.revote("MyVote", "Option2", {'from': accounts[1]})

    # Check that the vote count for the first option has decreased by 1 and the second option has increased by 1
    assert vote.getScore("MyVote", "Option1", {'from': accounts[1]}) == 0
    assert vote.getScore("MyVote", "Option2", {'from': accounts[1]}) == 1

def test_revote_without_permission(vote):
    # Create a vote
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])

    # Try to re-vote without permission
    with reverts("You don't have permission to vote"):
        vote.revote("MyVote", "Option2", {'from': accounts[2]})

def test_revote_before_casting_vote(vote):
    # Create a vote
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])

    # Try to re-vote before casting an initial vote
    with reverts("You haven't voted yet"):
        vote.revote("MyVote", "Option2", {'from': accounts[1]})

def test_revote_inactive_vote(vote):
    # Create a vote
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp + 3600, web3.eth.get_block('latest').timestamp + 7200, ["Option1", "Option2"], [accounts[1]], [accounts[0]])

    # Cast initial vote
    vote.castVote("MyVote", "Option1", {'from': accounts[1]})

    # Try to re-vote after the vote has ended
    with reverts("Voting has ended"):
        vote.revote("MyVote", "Option2", {'from': accounts[1]})
