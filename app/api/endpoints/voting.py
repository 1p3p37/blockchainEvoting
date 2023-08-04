from typing import List, Dict
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core.redis_cache import cache_response

router = APIRouter()


@router.get("/", response_model=List[schemas.VoteInDB])
@cache_response()
async def get_all_votes(voting_name: str, db: Session = Depends(deps.get_db)):
    voting = crud.voting.get_by_name(db, name=voting_name)
    if not voting:
        raise HTTPException(status_code=404, detail="Voting not found")

    logging.info(f"Voting with name {voting.name} exists.")

    total_votes = crud.vote.get_all_votes_by_voting_name(db=db, voting_name=voting_name)
    return total_votes


@router.get("/total")
@cache_response()
async def get_number_votes(voting_name: str, db: Session = Depends(deps.get_db)):
    voting = crud.voting.get_by_name(db, name=voting_name)
    if not voting:
        raise HTTPException(status_code=404, detail="Voting not found")

    logging.info(f"Voting with name {voting.name} exists.")

    total_votes = crud.vote.get_total_values(db=db, voting=voting)
    return total_votes


@router.get("/score")
@cache_response()
async def get_voting_score(voting_name: str, db: Session = Depends(deps.get_db)):
    voting = crud.voting.get_by_name(db, name=voting_name)
    if not voting:
        raise HTTPException(status_code=404, detail="Voting not found")
    logging.info(f"Voting with name {voting.name} exists.")

    score = crud.vote.get_score_by_name(db=db, voting_name=voting_name)
    # total_votes = await crud.vote.get_total_values(db=db, voting=voting)
    return score


@router.get("/votings")
@cache_response()
async def get_all_votings(db: Session = Depends(deps.get_db)):
    return crud.voting.get_all_votings(db=db)
