import pytest
from brownie import MultiOptionStringVote, accounts, reverts, web3
# import web3
from brownie.network.state import Chain
import brownie


@pytest.fixture
def vote():
    yield MultiOptionStringVote.deploy({'from': accounts[0]})


def test_create_vote(vote):
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    assert vote.votes("MyVote").startTime == 0
    assert vote.votes("MyVote").endTime == 100
    assert vote.votes("MyVote").options == ["Option1", "Option2"]
    assert vote.votes("MyVote").ownerPermissions[accounts[0]]
    assert vote.votes("MyVote").votePermissions[accounts[1]]


def test_cast_vote(vote):
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    vote.castVote("MyVote", "Option1", {'from': accounts[1]})
    assert vote.votes("MyVote").voteCounts("Option1") == 1
    assert vote.votes("MyVote").voters.contains(accounts[1])


def test_revote(vote):
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    vote.castVote("MyVote", "Option1", {'from': accounts[1]})
    vote.revote("MyVote", "Option2", {'from': accounts[1]})
    assert vote.votes("MyVote").voteCounts("Option1") == 0
    assert vote.votes("MyVote").voteCounts("Option2") == 1


def test_get_options(vote):
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    assert vote.getOptions("MyVote", {'from': accounts[1]}) == ["Option1", "Option2"]


def test_get_score(vote):
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    vote.castVote("MyVote", "Option1", {'from': accounts[1]})
    assert vote.getScore("MyVote", "Option1", {'from': accounts[1]}) == 1


def test_has_voted(vote):
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    vote.castVote("MyVote", "Option1", {'from': accounts[1]})
    assert vote.hasVoted("MyVote", {'from': accounts[1]})


def test_get_voters(vote):
    vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    vote.castVote("MyVote", "Option1", {'from': accounts[1]})
    assert vote.getVoters("MyVote", {'from': accounts[1]}) == [accounts[1]]


# def test_grant_vote_rights(vote):
#     vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [], [accounts[0]])
#     vote.grantVoteRights("MyVote", [accounts[1]], {'from': accounts[0]})
#     assert vote.votes("MyVote").votePermissions[

def test_grant_vote_rights(vote):
    # Deploy the contract and create a vote
    vote.createVote("Test Vote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option A", "Option B"], [accounts[1]], [accounts[0]])

    # Attempt to grant voting rights before the voting period has started
    # with brownie.reverts("Voting has not yet started"):
    assert vote.grantVoteRights("Test Vote", [accounts[2]], {'from': accounts[0]})

    # Advance the blockchain timestamp to the start of the voting period
    Chain().sleep(3600)

    # Attempt to grant voting rights after the voting period has ended
    # with brownie.reverts("Voting has ended"):
    # assert vote.grantVoteRights("Test Vote", [accounts[2]], {'from': accounts[0]})

    # Grant voting rights to an account
    vote.grantVoteRights("Test Vote", [accounts[2]], {'from': accounts[0]})

    # Ensure the account can cast a vote
    vote.castVote("Test Vote", "Option A", {'from': accounts[2]})
    assert vote.getScore("Test Vote", "Option A") == 1


