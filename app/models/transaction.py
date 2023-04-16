# import enum

# from sqlalchemy import Column, DateTime, Integer, String, func
# from sqlalchemy.dialects.postgresql import ARRAY, ENUM
# from sqlalchemy.ext.mutable import MutableList
# from sqlalchemy.sql import func

# from app.db.base_class import Base
# from app.db.custom_types import EvmUint256


# class TxStatus(enum.Enum):
#     WAITING_FOR_SEND = "WAITING_FOR_SEND"
#     CONTRACT_LOGIC_ERROR = "CONTRACT_LOGIC_ERROR"
#     VALUE_ERROR = "VALUE_ERROR"
#     PENDING = "PENDING"
#     SUCCESS = "SUCCESS"
#     FAIL = "FAIL"


# class Transaction(Base):
#     status = Column(
#         ENUM(TxStatus, create_type=False), default=TxStatus.WAITING_FOR_SEND
#     )
#     sent_at = Column(DateTime, server_default=func.now())
#     tx_hashes = Column(MutableList.as_mutable(ARRAY(String)), server_default="{}")
#     data = Column(String)
#     to = Column(String)
#     gas_price = Column(EvmUint256)
#     gas_limit = Column(EvmUint256)
#     nonce = Column(Integer)
