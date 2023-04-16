from __future__ import annotations

import os
import secrets
from dataclasses import field
from functools import cached_property
from typing import TYPE_CHECKING

import yaml
from pydantic import AnyHttpUrl, PostgresDsn, condecimal
from pydantic.dataclasses import dataclass
from web3 import Web3

from app import custom_types
from eth_typing.evm import ChecksumAddress


if TYPE_CHECKING:
    from app.services.contracts.voting import VotingContract

DB_URL = "postgres://{user}:{password}@{hostname}:{port}/{db}".format(
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    hostname=os.getenv("POSTGRES_HOST", "127.0.0.1"),
    db=os.getenv("POSTGRES_DB", "postgres"),
    port=os.getenv("POSTGRES_PORT", 5432),
)

evm_uint256 = condecimal(max_digits=len(str(2**256)), decimal_places=18)


@dataclass
class BlockchainSettings:
    cold_storage_address: str
    min_deposit_amount: evm_uint256
    min_withdrawal_amount: evm_uint256
    confirmations_count: int
    fee_priority: custom_types.FeePriority
    private_key: str


@dataclass
class EthereumSettings(BlockchainSettings):
    hot_wallet_address: str
    broadcast_interval: int
    network: custom_types.EthereumNetwork
    rpc_url: str
    rpc_connection_timeout: int
    voting_contract_address: str
    always_restart_interval: int
    confirmation_blocks: int
    scanning_blocks_max: int
    polling_interval: int
    speedy_polling_interval: int

    @cached_property
    def w3(self) -> Web3:
        return Web3(
            Web3.HTTPProvider(
                self.rpc_url, request_kwargs={"timeout": self.rpc_connection_timeout}
            )
        )

    # @cached_property
    # def reward_contract(self) -> "RewardContract":
    #     from app.services.contracts.reward import RewardContract

    #     return RewardContract(self)

    @cached_property
    def voting_contract(self) -> "VotingContract":
        from app.services.contracts.voting import VotingContract

        return VotingContract(self)

    @cached_property
    def account_address(self) -> ChecksumAddress:
        return self.w3.eth.account.from_key(self.private_key).address


@dataclass
class Settings:
    project_name: str
    redis_host: str
    redis_port: int
    ethereum: EthereumSettings
    is_debug: bool = False
    api_string: str = "/api"
    api_debug_str: str = "/api/debug"
    secret_key: str = secrets.token_urlsafe(32)
    api_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int = 60 * 24 * 7  # 7 days
    backend_cors_origins: list[AnyHttpUrl] = field(default_factory=list)
    password_length: int = 12
    is_test: bool = os.getenv("IS_TEST", False)

    @cached_property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            path=f"/{os.getenv('POSTGRES_DB') or ''}",
        )

    @cached_property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"


with open(os.environ["CONFIG"], "r") as f:
    config_data = yaml.safe_load(f)


settings = Settings(**config_data)
