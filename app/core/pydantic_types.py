from web3 import Web3


class ChecksumAddress(str):
    """
    Ethereum address validation.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("String required")

        if not Web3.is_address(v):
            raise ValueError("Not Ethereum address")

        return cls(Web3.to_checksum_address(v))

    def __repr__(self):
        return f"ChecksumAddress({super().__repr__()})"
