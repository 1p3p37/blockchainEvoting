// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/structs/EnumerableSet.sol";

contract MultiOptionStringVote {
    using EnumerableSet for EnumerableSet.AddressSet;

    event VotingCreated();
    event votedEvent(string voteName, address voter); 

    struct Vote {
        uint256 startTime;
        uint256 endTime;
        string[] options;
        EnumerableSet.AddressSet voters;
        mapping(string => uint256) voteCounts;
        mapping(address => bool) ownerPermissions;
        mapping(address => bool) votePermissions;
        mapping(address => string) votedFor;
    }

    mapping(string => Vote) private votes;

    function createVote(
        string memory voteName, 
        uint256 startTime, 
        uint256 endTime, 
        string[] memory options, 
        address[] memory votePermissionList, 
        address[] memory ownerPermissionList
        ) public {
        require(startTime < endTime, "End time must be after start time");
        require(votes[voteName].endTime == 0, "Vote with same name already exists");

        votes[voteName].startTime = startTime;
        votes[voteName].endTime = endTime;
        votes[voteName].options = options;
        votes[voteName].ownerPermissions[msg.sender] = true;

        for (uint i = 0; i < options.length; i++) {
            votes[voteName].voteCounts[options[i]] = 0;
        }

        for (uint i = 0; i < ownerPermissionList.length; i++) {
            votes[voteName].ownerPermissions[ownerPermissionList[i]] = true;
        }

        for (uint i = 0; i < votePermissionList.length; i++) {
            votes[voteName].votePermissions[votePermissionList[i]] = true;
        }

        emit VotingCreated();
    }

    function castVote(string memory voteName, string memory option) public {
        require(votes[voteName].endTime > block.timestamp, "Voting has ended");
        require(votes[voteName].startTime <= block.timestamp, "Voting has not yet started");
        require(votes[voteName].votePermissions[msg.sender], "You don't have permission to vote");
        require(!votes[voteName].voters.contains(msg.sender), "You have already voted");

        votes[voteName].voteCounts[option]++;
        votes[voteName].voters.add(msg.sender);
        votes[voteName].votedFor[msg.sender] = option;
        
        emit votedEvent(voteName, msg.sender);
    }

    function revote(string memory voteName, string memory option) public {
        require(votes[voteName].endTime > block.timestamp, "Voting has ended");
        require(votes[voteName].startTime <= block.timestamp, "Voting has not yet started");
        require(votes[voteName].votePermissions[msg.sender], "You don't have permission to vote");
        require(votes[voteName].voters.contains(msg.sender), "You haven't voted yet");

        string memory lastOption = votes[voteName].votedFor[msg.sender];

        votes[voteName].voteCounts[lastOption]--;
        votes[voteName].voteCounts[option]++;
    
        emit votedEvent(voteName, msg.sender);
    }

    function getOptions(string memory voteName) public view returns (string[] memory) {
        require(votes[voteName].votePermissions[msg.sender], "You don't have permission to this vote");
        return votes[voteName].options;
    }

    function getScore(string memory voteName, string memory option) public view returns (uint) {
        require(votes[voteName].votePermissions[msg.sender], "You don't have permission to this vote");
        return votes[voteName].voteCounts[option];
    }

    function hasVoted(string memory voteName) public view returns (bool) {
        require(votes[voteName].votePermissions[msg.sender], "You don't have permission to this vote");
        return votes[voteName].voters.contains(msg.sender);
    }

    function getVoters(string memory voteName) public view returns (address[] memory) {
        require(votes[voteName].votePermissions[msg.sender], "You don't have permission to this vote");
        uint256 numVoters = votes[voteName].voters.length();
        address[] memory votersArray = new address[](numVoters);

        for (uint256 i = 0; i < numVoters; i++) {
            votersArray[i] = votes[voteName].voters.at(i);
        }

        return votersArray;
    }

    function grantVoteRights(string memory voteName, address[] memory votePermissionList) public {
        require(votes[voteName].endTime > block.timestamp, "Voting has ended");
        require(votes[voteName].startTime <= block.timestamp, "Voting has not yet started");
        require(votes[voteName].ownerPermissions[msg.sender], "You don't have permission to vote");
        
        for (uint i = 0; i < votePermissionList.length; i++) {
            votes[voteName].votePermissions[votePermissionList[i]] = true;
        }
    }

}
