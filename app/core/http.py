from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBasic
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN


class HTTPKey2FA(APIKeyHeader):
    async def __call__(self, request: Request) -> Optional[str]:
        auth_token = str(request.headers.get(self.model.name))
        if not auth_token:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )
        if not (auth_token.isdigit() and len(auth_token) == 6):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid authentication credentials",
            )
        return auth_token
