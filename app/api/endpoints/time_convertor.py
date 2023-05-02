import datetime

from app.services.time_convertor import time_parser, timestamp_to_datetime

from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/to_timestamp")
def time_to_timestamp(time_: str) -> int | None:
    time = time_parser(time_)
    if not time:
        raise HTTPException(status_code=404, detail="Parse process was failed")
    else:
        import logging

        logging.warning(f"Parsed time: {time} ")

    return time


@router.get("/to_datetime")
def to_datetime(timestamp: int) -> str | None:
    return timestamp_to_datetime(timestamp)
