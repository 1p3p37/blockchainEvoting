from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/")
def get_total_votes(voting_name: str, db: Session = Depends(deps.get_db)):
    voting = crud.voting.get_by_name(db, name=voting_name)
    if not voting:
        raise HTTPException(status_code=404, detail="Voting not found")
    else:
        import logging

        logging.warning(f"Voting with name {voting.name} exists.")

    total_votes = crud.vote.get_all_votes_by_voting_name(db=db, voting_name=voting_name)
    return total_votes

    # @router.get("/total_votes", response_model=Dict[str, int])
    # def get_total_votes(
    #     voting_name: str,
    #     db: Session = Depends(deps.get_db),
    # ):
    #     voting = crud.voting.get_by_name(db, name=voting_name)
    #     if not voting:
    #         raise HTTPException(status_code=404, detail="Voting not found")
    #     try:
    #        all_votes = crud.vote.get_all_votes_by_voting_name(db=db, voting_name=voting_name)
    #     except:
    #         raise HTTPException(status_code=404, detail="Shit happend")
    #     return all_votes

    # @router.get("/hello")
    # def hello():
    #     return "Hello"

    # @router.get("/total_votes", response_model="???????")
    # def get_total_votes(

    # )
    #     ...
    #     ...
    #     ...
    #     return crud.vote.get_all_votes_by_voting_name(
    #         db=db,
    #         voting_name=voting_name,
    #     )

    #     db: Session = Depends(deps.get_db),
    #     voting_name: str = 'Test1',
    #     # skip: int = 0,
    #     # limit: int = 100,
    # ) -> Any:
    return crud.vote.get_all_votes_by_voting_name(
        db=db,
        voting_name=voting_name,
    )
