# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class PayrollRunsListRequestRemoteFields(str, enum.Enum):
    RUN_STATE = "run_state"
    RUN_STATE_RUN_TYPE = "run_state,run_type"
    RUN_TYPE = "run_type"

    def visit(
        self,
        run_state: typing.Callable[[], T_Result],
        run_state_run_type: typing.Callable[[], T_Result],
        run_type: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is PayrollRunsListRequestRemoteFields.RUN_STATE:
            return run_state()
        if self is PayrollRunsListRequestRemoteFields.RUN_STATE_RUN_TYPE:
            return run_state_run_type()
        if self is PayrollRunsListRequestRemoteFields.RUN_TYPE:
            return run_type()
