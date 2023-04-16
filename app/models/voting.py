import random
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, text
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime


class Voting(Base):
    # __tablename__ = "voting"
    tx_hash = Column(
        String, unique=True, nullable=False, server_default=text("random()")
    )
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_time = Column(Integer, default=int(datetime.now().timestamp()))
    end_time = Column(Integer)
    options = relationship("Option", back_populates="voting")
    votes = relationship("Vote", back_populates="voting")
    owners = relationship("VotingOwner", back_populates="voting")


class VotingOwner(Base):
    # __tablename__ = "voting_owner"
    id = Column(Integer, primary_key=True, index=True)
    voting_id = Column(Integer, ForeignKey("voting.id"))
    owner_address = Column(String)
    voting = relationship("Voting", back_populates="owners")


class Option(Base):
    # __tablename__ = "option"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    voting_id = Column(Integer, ForeignKey("voting.id"))
    voting = relationship("Voting", back_populates="options")


class Vote(Base):
    # __tablename__ = "vote"
    id = Column(Integer, primary_key=True, index=True)
    voting_id = Column(Integer, ForeignKey("voting.id"))
    tx_hash = Column(
        String, unique=True, nullable=False, server_default=text("random()")
    )
    voting = relationship("Voting", back_populates="votes")
    option_id = Column(Integer, ForeignKey("option.id"))
    option = relationship("Option")
    voter_address = Column(String)
    voted_for = Column(String)
    is_revote = Column(Boolean, default=False)
    block_number = Column(Integer)
