import pytest

from brownie import Voting, accounts, reverts, web3
from brownie.network.state import Chain


@pytest.fixture
def vote():
    yield Voting.deploy({"from": accounts[0]})


def test_revote_success(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Cast initial vote
    vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    # Re-vote for a different option
    vote.revote("MyVote", "Option2", {"from": accounts[1]})

    # Check that the vote count for the first option has decreased by 1 and the second option has increased by 1
    assert vote.getScore("MyVote", "Option1", {"from": accounts[1]}) == 0
    assert vote.getScore("MyVote", "Option2", {"from": accounts[1]}) == 1


def test_revote_without_permission(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Try to re-vote without permission
    with reverts("You don't have permission to vote"):
        vote.revote("MyVote", "Option2", {"from": accounts[2]})


def test_revote_before_casting_vote(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Try to re-vote before casting an initial vote
    with reverts("You haven't voted yet"):
        vote.revote("MyVote", "Option2", {"from": accounts[1]})


def test_revote_inactive_vote(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp + 3600,
        web3.eth.get_block("latest").timestamp + 7200,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Cast initial vote
    with reverts("Voting has not yet started"):
        vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    Chain().sleep(7201)

    # Try to re-vote after the vote has ended
    with reverts("Voting has ended"):
        vote.revote("MyVote", "Option2", {"from": accounts[1]})


# def test_revote_same_option(vote):
#     # Create a vote
#     vote.createVote(
#         "MyVote",
#         web3.eth.get_block("latest").timestamp,
#         web3.eth.get_block("latest").timestamp + 3600,
#         ["Option1", "Option2"],
#         [accounts[1]],
#         [accounts[0]],
#     )

#     # Cast initial vote
#     vote.castVote("MyVote", "Option1", {"from": accounts[1]})

#     # Try to revote for the same option
#     with reverts("You already voted for this option"):
#         vote.revote("MyVote", "Option1", {"from": accounts[1]})


def test_revote_invalid_option(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Cast initial vote
    vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    # Try to revote for a non-existent option
    with reverts("This option doesn't exist"):
        vote.revote("MyVote", "Option3", {"from": accounts[1]})


def test_revote_after_voting_period(vote):
    # Create a vote
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Cast initial vote
    vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    # Wait for the revoting period to end
    Chain().sleep(3601)

    # Try to revote after the voting period has ended
    with reverts("Voting has ended"):
        vote.revote("MyVote", "Option2", {"from": accounts[1]})


# def test_revote_after_revoking_vote(vote):
#     # Create a vote
#     vote.createVote(
#         "MyVote",
#         web3.eth.get_block("latest").timestamp,
#         web3.eth.get_block("latest").timestamp + 3600,
#         ["Option1", "Option2"],
#         [accounts[1]],
#         [accounts[0]],
#     )

#     # Cast initial vote
#     vote.castVote("MyVote", "Option1", {"from": accounts[1]})

#     # Revoke initial vote
#     vote.revokeVote("MyVote", {"from": accounts[1]})

#     # Re-vote for a different option
#     vote.revote("MyVote", "Option2", {"from": accounts[1]})

#     # Check that the vote count for the first option has decreased by 1 and the second option has increased by 1
#     assert vote.getScore("MyVote", "Option1", {"from": accounts[1]}) == 0
#     assert vote.getScore("MyVote", "Option2", {"from": accounts[1]}) == 1


def test_revote_after_revoting_period(vote):
    # Create a vote with a revoting period of 1 hour
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Cast initial vote
    vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    # Wait for the revoting period to end
    Chain().sleep(3600)

    # Try to re-vote after the revoting period has ended
    with reverts("Voting has ended"):
        vote.revote("MyVote", "Option2", {"from": accounts[1]})


def test_revote_nonexistent_vote(vote):
    vote.createVote(
        "MyVote",
        web3.eth.get_block("latest").timestamp,
        web3.eth.get_block("latest").timestamp + 3600,
        ["Option1", "Option2"],
        [accounts[1]],
        [accounts[0]],
    )

    # Cast initial vote
    vote.castVote("MyVote", "Option1", {"from": accounts[1]})

    # Try to re-vote for a vote that doesn't exist
    with reverts("Voting has ended"):
        vote.revote("NonexistentVote", "Option1", {"from": accounts[1]})


# def test_revote_not_allowed(vote):
#     # Create a vote with no revoting allowed for the voter
#     vote.createVote(
#         "MyVote",
#         web3.eth.get_block("latest").timestamp,
#         web3.eth.get_block("latest").timestamp + 3600,
#         ["Option1", "Option2"],
#         [accounts[1]],
#         [],
#     )

#     # Cast initial vote
#     vote.castVote("MyVote", "Option1", {"from": accounts[1]})

#     # Try to re-vote when not allowed
#     with reverts("Revoting not allowed for this voter"):
#         vote.revote("MyVote", "Option2", {"from": accounts[1]})
