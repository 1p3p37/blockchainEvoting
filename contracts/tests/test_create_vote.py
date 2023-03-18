import pytest
from brownie import MultiOptionStringVote, accounts, reverts, web3


@pytest.fixture
def vote():
    yield MultiOptionStringVote.deploy({'from': accounts[0]})


def test_create_vote(vote):
    # Test successful vote creation
    assert vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
    
    # Test vote creation with same name as existing vote
def test_create_exists_vote(vote):
    assert vote.createVote("MyVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [accounts[0]])

    # Test vote creation with empty options list
def test_empty_options_vote(vote):
    assert vote.createVote("EmptyOptionsVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, [], [accounts[1]], [accounts[0]])

    # Test vote creation with empty votePermissions list
def test_empty_vote_permissions_vote(vote):
    assert vote.createVote("EmptyVotePermissionsVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [], [accounts[0]])

    # Test vote creation with empty ownerPermissions list
def test_empty_owner_permissions_vote(vote):
    assert vote.createVote("EmptyOwnerPermissionsVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 3600, ["Option1", "Option2"], [accounts[1]], [])

    # Test vote creation with endTime before startTime
def test_end_time_before_start(vote):
    assert vote.createVote("EndTimeBeforeStartTimeVote", web3.eth.get_block('latest').timestamp + 3600, web3.eth.get_block('latest').timestamp, ["Option1", "Option2"], [accounts[1]], [accounts[0]])

    # Test vote creation with voting period too short
def test_short_voting_period_vote(vote):
    assert vote.createVote("ShortVotingPeriodVote", web3.eth.get_block('latest').timestamp, web3.eth.get_block('latest').timestamp + 1, ["Option1", "Option2"], [accounts[1]], [accounts[0]])
