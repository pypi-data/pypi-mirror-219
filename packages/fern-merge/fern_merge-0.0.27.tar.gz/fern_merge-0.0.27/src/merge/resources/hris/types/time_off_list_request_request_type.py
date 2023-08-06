# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class TimeOffListRequestRequestType(str, enum.Enum):
    BEREAVEMENT = "BEREAVEMENT"
    JURY_DUTY = "JURY_DUTY"
    PERSONAL = "PERSONAL"
    SICK = "SICK"
    VACATION = "VACATION"
    VOLUNTEER = "VOLUNTEER"

    def visit(
        self,
        bereavement: typing.Callable[[], T_Result],
        jury_duty: typing.Callable[[], T_Result],
        personal: typing.Callable[[], T_Result],
        sick: typing.Callable[[], T_Result],
        vacation: typing.Callable[[], T_Result],
        volunteer: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is TimeOffListRequestRequestType.BEREAVEMENT:
            return bereavement()
        if self is TimeOffListRequestRequestType.JURY_DUTY:
            return jury_duty()
        if self is TimeOffListRequestRequestType.PERSONAL:
            return personal()
        if self is TimeOffListRequestRequestType.SICK:
            return sick()
        if self is TimeOffListRequestRequestType.VACATION:
            return vacation()
        if self is TimeOffListRequestRequestType.VOLUNTEER:
            return volunteer()
