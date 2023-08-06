# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import pydantic

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....core.jsonable_encoder import jsonable_encoder
from .....environment import MergeEnvironment
from ...types.linked_account_selective_sync_configuration import LinkedAccountSelectiveSyncConfiguration
from ...types.linked_account_selective_sync_configuration_request import LinkedAccountSelectiveSyncConfigurationRequest
from ...types.paginated_condition_schema_list import PaginatedConditionSchemaList

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class SelectiveSyncClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: SyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    def configurations_list(self) -> typing.List[LinkedAccountSelectiveSyncConfiguration]:
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/selective-sync/configurations"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[LinkedAccountSelectiveSyncConfiguration], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def configurations_update(
        self, *, sync_configurations: typing.List[LinkedAccountSelectiveSyncConfigurationRequest]
    ) -> typing.List[LinkedAccountSelectiveSyncConfiguration]:
        _response = self._client_wrapper.httpx_client.request(
            "PUT",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/selective-sync/configurations"),
            json=jsonable_encoder({"sync_configurations": sync_configurations}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[LinkedAccountSelectiveSyncConfiguration], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def meta_list(
        self,
        *,
        common_model: typing.Optional[str] = None,
        cursor: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
    ) -> PaginatedConditionSchemaList:
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/selective-sync/meta"),
            params={"common_model": common_model, "cursor": cursor, "page_size": page_size},
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(PaginatedConditionSchemaList, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncSelectiveSyncClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: AsyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    async def configurations_list(self) -> typing.List[LinkedAccountSelectiveSyncConfiguration]:
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/selective-sync/configurations"),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[LinkedAccountSelectiveSyncConfiguration], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def configurations_update(
        self, *, sync_configurations: typing.List[LinkedAccountSelectiveSyncConfigurationRequest]
    ) -> typing.List[LinkedAccountSelectiveSyncConfiguration]:
        _response = await self._client_wrapper.httpx_client.request(
            "PUT",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/selective-sync/configurations"),
            json=jsonable_encoder({"sync_configurations": sync_configurations}),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(typing.List[LinkedAccountSelectiveSyncConfiguration], _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def meta_list(
        self,
        *,
        common_model: typing.Optional[str] = None,
        cursor: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
    ) -> PaginatedConditionSchemaList:
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/selective-sync/meta"),
            params={"common_model": common_model, "cursor": cursor, "page_size": page_size},
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(PaginatedConditionSchemaList, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
