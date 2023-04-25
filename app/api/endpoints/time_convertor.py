from app.services.time_convertor import time_parser

from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/")
def time_convertor(time_: str):
    time = time_parser(time_)
    if not time:
        raise HTTPException(status_code=404, detail="Parse process was failed")
    else:
        import logging
        logging.warning(f"Parsed time: {time} ")

    return time

