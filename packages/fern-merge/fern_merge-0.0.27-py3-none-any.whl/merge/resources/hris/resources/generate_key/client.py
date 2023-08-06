# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import pydantic

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....core.jsonable_encoder import jsonable_encoder
from .....environment import MergeEnvironment
from ...types.remote_key import RemoteKey

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class GenerateKeyClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: SyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    def create(self, *, name: str) -> RemoteKey:
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/hris/v1/generate-key"),
            json=jsonable_encoder({"name": name}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(RemoteKey, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncGenerateKeyClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: AsyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    async def create(self, *, name: str) -> RemoteKey:
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/hris/v1/generate-key"),
            json=jsonable_encoder({"name": name}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(RemoteKey, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
