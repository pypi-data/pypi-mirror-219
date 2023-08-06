"""Add a health check."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

router = APIRouter(tags=["util"], responses={404: {"description": "Not found"}})


## Define filter for pings to /healthy
#  https://stackoverflow.com/a/70810102
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/health"


## Add "healthy" ping filter to logger, don't log healthchecks
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


@router.get("/health")
async def healthy() -> str:
    return "healthy"
