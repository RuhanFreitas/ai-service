from fastapi import Header

from app.core.config import settings
from app.core.exceptions import UnauthorizedError


def verify_internal_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    if x_api_key != settings.internal_api_key:
        raise UnauthorizedError()
