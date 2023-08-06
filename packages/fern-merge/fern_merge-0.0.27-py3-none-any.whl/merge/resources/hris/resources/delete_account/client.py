# This file was auto-generated by Fern from our API Definition.

import urllib.parse
from json.decoder import JSONDecodeError

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....environment import MergeEnvironment


class DeleteAccountClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: SyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    def create(self) -> None:
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/hris/v1/delete-account"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncDeleteAccountClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: AsyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    async def create(self) -> None:
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/hris/v1/delete-account"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
