# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import pydantic

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....core.jsonable_encoder import jsonable_encoder
from .....environment import MergeEnvironment
from ...types.method_enum import MethodEnum
from ...types.multipart_form_field_request import MultipartFormFieldRequest
from ...types.remote_response import RemoteResponse
from ...types.request_format_enum import RequestFormatEnum

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class PassthroughClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: SyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    def create(
        self,
        *,
        method: MethodEnum,
        path: str,
        base_url_override: typing.Optional[str] = OMIT,
        data: typing.Optional[str] = OMIT,
        multipart_form_data: typing.Optional[typing.List[MultipartFormFieldRequest]] = OMIT,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        request_format: typing.Optional[RequestFormatEnum] = OMIT,
        normalize_response: bool,
    ) -> RemoteResponse:
        _request: typing.Dict[str, typing.Any] = {
            "method": method,
            "path": path,
            "normalize_response": normalize_response,
        }
        if base_url_override is not OMIT:
            _request["base_url_override"] = base_url_override
        if data is not OMIT:
            _request["data"] = data
        if multipart_form_data is not OMIT:
            _request["multipart_form_data"] = multipart_form_data
        if headers is not OMIT:
            _request["headers"] = headers
        if request_format is not OMIT:
            _request["request_format"] = request_format
        _response = self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/hris/v1/passthrough"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(RemoteResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncPassthroughClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: AsyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    async def create(
        self,
        *,
        method: MethodEnum,
        path: str,
        base_url_override: typing.Optional[str] = OMIT,
        data: typing.Optional[str] = OMIT,
        multipart_form_data: typing.Optional[typing.List[MultipartFormFieldRequest]] = OMIT,
        headers: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        request_format: typing.Optional[RequestFormatEnum] = OMIT,
        normalize_response: bool,
    ) -> RemoteResponse:
        _request: typing.Dict[str, typing.Any] = {
            "method": method,
            "path": path,
            "normalize_response": normalize_response,
        }
        if base_url_override is not OMIT:
            _request["base_url_override"] = base_url_override
        if data is not OMIT:
            _request["data"] = data
        if multipart_form_data is not OMIT:
            _request["multipart_form_data"] = multipart_form_data
        if headers is not OMIT:
            _request["headers"] = headers
        if request_format is not OMIT:
            _request["request_format"] = request_format
        _response = await self._client_wrapper.httpx_client.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/hris/v1/passthrough"),
            json=jsonable_encoder(_request),
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(RemoteResponse, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
