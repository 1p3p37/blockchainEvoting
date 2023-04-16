from sqlalchemy import BigInteger, Column, Integer, String, UniqueConstraint

from app.db.base_class import Base


class EventScanner(Base):
    __table_args__ = (UniqueConstraint("contract_address", "event_name"),)
    id = Column(Integer, primary_key=True, index=True)
    last_processed_block_num = Column(BigInteger)
    contract_address = Column(String, index=True)
    event_name = Column(String, index=True)
