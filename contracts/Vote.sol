pragma solidity ^0.8.12;

import "@openzeppelin/contracts/utils/Strings.sol";

contract Voting {
    //event for vote
    event votedEvent(address voter, uint voteId);
    //mapping of voters
    mapping(address => bool) public voters;
    //mapping of voted
    mapping(address => uint) public voted;
    //mapping of votes
    mapping(uint => uint) public votes;
    //array of options
    string[] public options;
    
    constructor(string[] memory _options) public {
        options = _options;
    }
// ["Trump","Biden","Putin"]
    //Function to grant voting rights
    function grantVotingRights(address _voter) public {
        require(msg.sender == msg.sender, "only owner can grant voting rights");
        voters[_voter] = true;
    }

    //Function to revoke voting rights
    function revokeVotingRights(address _voter) public {
        require(msg.sender == msg.sender, "only owner can revoke voting rights");
        voters[_voter] = false;
    }

    //Function to vote
    function vote(uint _voteId) public {
        require(voters[msg.sender] == true, "you must have voting rights to vote");
        require(voted[msg.sender] == 0, "you already voted");
        require(_voteId > 0 && _voteId <= options.length, "invalid vote option");
        votes[_voteId]++;
        voted[msg.sender] = _voteId;
        emit votedEvent(msg.sender, _voteId);
    }

    //Function to re-vote
    function revote(uint _voteId) public {
        require(voters[msg.sender] == true, "you must have voting rights to vote");
        require(voted[msg.sender] != 0, "you did not voted before");
        require(_voteId > 0 && _voteId <= options.length, "invalid vote option");
        votes[voted[msg.sender]]--;
        votes[_voteId]++;
        voted[msg.sender] = _voteId;
        emit votedEvent(msg.sender, _voteId);
    }

    // mapping(uint => uint) public votes;

    function getTotalVotes() public view returns (uint) {
        uint totalVotes = 0;
        for (uint i = 0; i < options.length; i++) {
            totalVotes = totalVotes + votes[i];
        }
        return totalVotes;
    }

    struct Result {
        // string memory name;
        string name;
        uint votes;
        uint percentage;
    }
    
    function getResults() public view returns (Result[] memory) {
        uint totalVotes = getTotalVotes();
        Result[] memory results = new Result[](options.length);
        for (uint i = 0; i < options.length; i++) {
            results[i] = Result({
                name: options[i],
                votes: votes[i],
                percentage: votes[i] * 100 / totalVotes
            });
        }
        return results;
    }

struct OptionInfo {
    uint index;
    string name;
}

function getAllOptions() public view returns (OptionInfo[] memory) {
    OptionInfo[] memory result = new OptionInfo[](options.length);
    for (uint i = 0; i < options.length; i++) {
        result[i] = OptionInfo(i, options[i]);
    }
    return result;
}


}
//  can you add a gas limit to my functions that use gas     ["Trump","Biden","Putin"]


