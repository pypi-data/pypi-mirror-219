# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import pydantic
import typing_extensions

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....environment import MergeEnvironment
from ...types.paginated_scorecard_list import PaginatedScorecardList
from ...types.scorecard import Scorecard
from ...types.scorecards_list_request_expand import ScorecardsListRequestExpand
from ...types.scorecards_retrieve_request_expand import ScorecardsRetrieveRequestExpand


class ScorecardsClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: SyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    def list(
        self,
        *,
        application_id: typing.Optional[str] = None,
        created_after: typing.Optional[str] = None,
        created_before: typing.Optional[str] = None,
        cursor: typing.Optional[str] = None,
        expand: typing.Optional[ScorecardsListRequestExpand] = None,
        include_deleted_data: typing.Optional[bool] = None,
        include_remote_data: typing.Optional[bool] = None,
        interview_id: typing.Optional[str] = None,
        interviewer_id: typing.Optional[str] = None,
        modified_after: typing.Optional[str] = None,
        modified_before: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        remote_fields: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
        remote_id: typing.Optional[str] = None,
        show_enum_origins: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
    ) -> PaginatedScorecardList:
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/scorecards"),
            params={
                "application_id": application_id,
                "created_after": created_after,
                "created_before": created_before,
                "cursor": cursor,
                "expand": expand,
                "include_deleted_data": include_deleted_data,
                "include_remote_data": include_remote_data,
                "interview_id": interview_id,
                "interviewer_id": interviewer_id,
                "modified_after": modified_after,
                "modified_before": modified_before,
                "page_size": page_size,
                "remote_fields": remote_fields,
                "remote_id": remote_id,
                "show_enum_origins": show_enum_origins,
            },
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(PaginatedScorecardList, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def retrieve(
        self,
        id: str,
        *,
        expand: typing.Optional[ScorecardsRetrieveRequestExpand] = None,
        include_remote_data: typing.Optional[bool] = None,
        remote_fields: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
        show_enum_origins: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
    ) -> Scorecard:
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", f"api/ats/v1/scorecards/{id}"),
            params={
                "expand": expand,
                "include_remote_data": include_remote_data,
                "remote_fields": remote_fields,
                "show_enum_origins": show_enum_origins,
            },
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Scorecard, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncScorecardsClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: AsyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    async def list(
        self,
        *,
        application_id: typing.Optional[str] = None,
        created_after: typing.Optional[str] = None,
        created_before: typing.Optional[str] = None,
        cursor: typing.Optional[str] = None,
        expand: typing.Optional[ScorecardsListRequestExpand] = None,
        include_deleted_data: typing.Optional[bool] = None,
        include_remote_data: typing.Optional[bool] = None,
        interview_id: typing.Optional[str] = None,
        interviewer_id: typing.Optional[str] = None,
        modified_after: typing.Optional[str] = None,
        modified_before: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        remote_fields: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
        remote_id: typing.Optional[str] = None,
        show_enum_origins: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
    ) -> PaginatedScorecardList:
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/scorecards"),
            params={
                "application_id": application_id,
                "created_after": created_after,
                "created_before": created_before,
                "cursor": cursor,
                "expand": expand,
                "include_deleted_data": include_deleted_data,
                "include_remote_data": include_remote_data,
                "interview_id": interview_id,
                "interviewer_id": interviewer_id,
                "modified_after": modified_after,
                "modified_before": modified_before,
                "page_size": page_size,
                "remote_fields": remote_fields,
                "remote_id": remote_id,
                "show_enum_origins": show_enum_origins,
            },
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(PaginatedScorecardList, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def retrieve(
        self,
        id: str,
        *,
        expand: typing.Optional[ScorecardsRetrieveRequestExpand] = None,
        include_remote_data: typing.Optional[bool] = None,
        remote_fields: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
        show_enum_origins: typing.Optional[typing_extensions.Literal["overall_recommendation"]] = None,
    ) -> Scorecard:
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", f"api/ats/v1/scorecards/{id}"),
            params={
                "expand": expand,
                "include_remote_data": include_remote_data,
                "remote_fields": remote_fields,
                "show_enum_origins": show_enum_origins,
            },
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(Scorecard, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
