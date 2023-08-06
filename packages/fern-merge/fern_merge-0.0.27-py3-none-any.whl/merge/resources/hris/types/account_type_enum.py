# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class AccountTypeEnum(str, enum.Enum):
    """
    * `SAVINGS` - SAVINGS
    * `CHECKING` - CHECKING
    """

    SAVINGS = "SAVINGS"
    CHECKING = "CHECKING"

    def visit(self, savings: typing.Callable[[], T_Result], checking: typing.Callable[[], T_Result]) -> T_Result:
        if self is AccountTypeEnum.SAVINGS:
            return savings()
        if self is AccountTypeEnum.CHECKING:
            return checking()
