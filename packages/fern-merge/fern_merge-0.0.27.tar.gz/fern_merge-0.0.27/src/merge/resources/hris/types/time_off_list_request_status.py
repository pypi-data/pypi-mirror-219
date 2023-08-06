# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class TimeOffListRequestStatus(str, enum.Enum):
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
    DECLINED = "DECLINED"
    DELETED = "DELETED"
    REQUESTED = "REQUESTED"

    def visit(
        self,
        approved: typing.Callable[[], T_Result],
        cancelled: typing.Callable[[], T_Result],
        declined: typing.Callable[[], T_Result],
        deleted: typing.Callable[[], T_Result],
        requested: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is TimeOffListRequestStatus.APPROVED:
            return approved()
        if self is TimeOffListRequestStatus.CANCELLED:
            return cancelled()
        if self is TimeOffListRequestStatus.DECLINED:
            return declined()
        if self is TimeOffListRequestStatus.DELETED:
            return deleted()
        if self is TimeOffListRequestStatus.REQUESTED:
            return requested()
