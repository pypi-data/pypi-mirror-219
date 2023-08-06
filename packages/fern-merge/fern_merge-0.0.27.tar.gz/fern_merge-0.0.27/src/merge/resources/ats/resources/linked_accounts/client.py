# This file was auto-generated by Fern from our API Definition.

import typing
import urllib.parse
from json.decoder import JSONDecodeError

import pydantic

from .....core.api_error import ApiError
from .....core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .....environment import MergeEnvironment
from ...types.linked_accounts_list_request_category import LinkedAccountsListRequestCategory
from ...types.paginated_account_details_and_actions_list import PaginatedAccountDetailsAndActionsList


class LinkedAccountsClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: SyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    def list(
        self,
        *,
        category: typing.Optional[LinkedAccountsListRequestCategory] = None,
        cursor: typing.Optional[str] = None,
        end_user_email_address: typing.Optional[str] = None,
        end_user_organization_name: typing.Optional[str] = None,
        end_user_origin_id: typing.Optional[str] = None,
        end_user_origin_ids: typing.Optional[str] = None,
        id: typing.Optional[str] = None,
        ids: typing.Optional[str] = None,
        include_duplicates: typing.Optional[bool] = None,
        integration_name: typing.Optional[str] = None,
        is_test_account: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        status: typing.Optional[str] = None,
    ) -> PaginatedAccountDetailsAndActionsList:
        _response = self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/linked-accounts"),
            params={
                "category": category,
                "cursor": cursor,
                "end_user_email_address": end_user_email_address,
                "end_user_organization_name": end_user_organization_name,
                "end_user_origin_id": end_user_origin_id,
                "end_user_origin_ids": end_user_origin_ids,
                "id": id,
                "ids": ids,
                "include_duplicates": include_duplicates,
                "integration_name": integration_name,
                "is_test_account": is_test_account,
                "page_size": page_size,
                "status": status,
            },
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(PaginatedAccountDetailsAndActionsList, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncLinkedAccountsClient:
    def __init__(
        self, *, environment: MergeEnvironment = MergeEnvironment.PRODUCTION, client_wrapper: AsyncClientWrapper
    ):
        self._environment = environment
        self._client_wrapper = client_wrapper

    async def list(
        self,
        *,
        category: typing.Optional[LinkedAccountsListRequestCategory] = None,
        cursor: typing.Optional[str] = None,
        end_user_email_address: typing.Optional[str] = None,
        end_user_organization_name: typing.Optional[str] = None,
        end_user_origin_id: typing.Optional[str] = None,
        end_user_origin_ids: typing.Optional[str] = None,
        id: typing.Optional[str] = None,
        ids: typing.Optional[str] = None,
        include_duplicates: typing.Optional[bool] = None,
        integration_name: typing.Optional[str] = None,
        is_test_account: typing.Optional[str] = None,
        page_size: typing.Optional[int] = None,
        status: typing.Optional[str] = None,
    ) -> PaginatedAccountDetailsAndActionsList:
        _response = await self._client_wrapper.httpx_client.request(
            "GET",
            urllib.parse.urljoin(f"{self._environment.value}/", "api/ats/v1/linked-accounts"),
            params={
                "category": category,
                "cursor": cursor,
                "end_user_email_address": end_user_email_address,
                "end_user_organization_name": end_user_organization_name,
                "end_user_origin_id": end_user_origin_id,
                "end_user_origin_ids": end_user_origin_ids,
                "id": id,
                "ids": ids,
                "include_duplicates": include_duplicates,
                "integration_name": integration_name,
                "is_test_account": is_test_account,
                "page_size": page_size,
                "status": status,
            },
            headers=self._client_wrapper.get_headers(),
            timeout=60,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(PaginatedAccountDetailsAndActionsList, _response.json())  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
