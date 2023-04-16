import asyncio
import logging
from json import JSONDecodeError
from typing import TypeVar
from urllib.parse import urljoin

from aiohttp import ClientSession
from pydantic import BaseModel, ValidationError

from app.services.api import defaults
from app.services.api.errors import (
    BadResponse,
    RequestOutsideContextManager,
    ResponseValidationError,
)

ResponseSchema = TypeVar("ResponseSchema", bound=BaseModel)


class API:
    def __init__(
        self,
        base_url: str,
        retries: int,
        retries_interval: int,
        timeout: int = defaults.TIMEOUT,
        headers: dict | None = None,
    ) -> None:
        self.base_url = base_url
        self.retries = retries
        self.retries_interval = retries_interval
        self.timeout = timeout
        self.headers = headers
        self._session = None

    def __init_subclass__(cls, **kwargs) -> None:
        cls.logger = logging.getLogger(cls.__name__)

    async def __aenter__(self):
        self._session = ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    @property
    def session(self):
        if not self._session:
            raise RequestOutsideContextManager("Use context manager to make requests")

        return self._session

    def _async_retry(f):
        async def wrapper(self, *args, **kwargs):
            attempts = 0
            while True:
                attempts += 1
                try:
                    return await f(self, *args, **kwargs)
                except Exception as e:
                    if attempts >= self.retries:
                        raise e

                    if not isinstance(e, BadResponse):
                        raise e

                    self.logger.info(f"Retry after {repr(e)}")
                    await asyncio.sleep(self.retries_interval)

        return wrapper

    @_async_retry
    async def request(
        self,
        response_schema: type[ResponseSchema],
        aiohttp_method,
        *args,
        **kwargs,
    ) -> ResponseSchema:
        async with aiohttp_method(*args, **kwargs) as response:
            try:
                response_dict = await response.json(content_type=None)
                self.logger.debug(f"Response: {response}")
            except JSONDecodeError:
                raise BadResponse(
                    f"Couldn't decode the response into json for {response.url}"
                )

            if not response.ok:
                raise BadResponse(
                    f"Bad response status for {response.url}: {response_dict}"
                )

            try:
                return response_schema(**response_dict)
            except ValidationError:
                raise ResponseValidationError(
                    f"Invalid response schema for {response.url}"
                )

    def construct_uri(self, path: str | list[str] | tuple[list] | None) -> str:
        if isinstance(path, list) or isinstance(path, tuple):
            return "/".join([self.base_url, "/".join(path)])
        elif isinstance(path, str):
            return urljoin(self.base_url, path)
        elif path is None:
            return self.base_url
        else:
            raise TypeError("Cannot parse path")

    async def get(
        self,
        *,
        path: str | list[str] | tuple[list] | None = None,
        response_schema: type[ResponseSchema],
    ) -> ResponseSchema:
        self.logger.debug(f"Making GET request: path={path}")
        return await self.request(
            response_schema,
            self.session.get,
            self.construct_uri(path),
            headers=self.headers,
            timeout=self.timeout,
        )

    async def post(
        self,
        *,
        path: str | list[str] | tuple[list] | None = None,
        body: dict,
        response_schema: type[ResponseSchema],
    ) -> ResponseSchema:
        self.logger.debug(f"Making POST request: path={path}, body={body}")
        return await self.request(
            response_schema,
            self.session.post,
            self.construct_uri(path),
            json=body,
            headers=self.headers,
            timeout=self.timeout,
        )
