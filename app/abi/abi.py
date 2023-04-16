import json
import os


def load_abi(name: str) -> list:
    with open(f"{name}") as f:
        json
        return json.load(f)


VOTING = load_abi("app/abi/VotingAbi.json")
