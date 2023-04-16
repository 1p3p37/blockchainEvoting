from enum import Enum


class Blockchain(Enum):
    bitcoin = "bitcoin"
    ethereum = "ethereum"


class EthereumNetwork(Enum):
    sepolia = "sepolia"
    mainnet = "mainnet"


class FeePriority(Enum):
    slow = "slow"
    standard = "standard"
    fast = "fast"
