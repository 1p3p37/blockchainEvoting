#!/usr/bin/python3
import os
from brownie import Vote, accounts, network
from distutils.util import strtobool


def main():
    # dev = accounts.add(os.getenv('PRIVATE_KEY'))
    dev = accounts[0]
    print(network.show_active())
    # publish_source = True if os.getenv("ETHERSCAN_TOKEN") else False
    from brownie.network.gas.strategies import GasNowScalingStrategy
    gas_strategy = GasNowScalingStrategy("standard", "fast", 1.2)
    deploy_args = [
    ]
    print('Deploy args:\n', deploy_args)
    if input("Deploy Vote? y/[N]: ").lower() != "y":
        return

    contract = Vote.deploy(
       *deploy_args, publish_source=publish_source
    )
    print('Deployed contract', contract.address)