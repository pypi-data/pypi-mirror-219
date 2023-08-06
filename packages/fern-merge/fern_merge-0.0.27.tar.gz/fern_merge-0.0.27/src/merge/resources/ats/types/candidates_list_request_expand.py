# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class CandidatesListRequestExpand(str, enum.Enum):
    APPLICATIONS = "applications"
    APPLICATIONS_ATTACHMENTS = "applications,attachments"
    ATTACHMENTS = "attachments"

    def visit(
        self,
        applications: typing.Callable[[], T_Result],
        applications_attachments: typing.Callable[[], T_Result],
        attachments: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is CandidatesListRequestExpand.APPLICATIONS:
            return applications()
        if self is CandidatesListRequestExpand.APPLICATIONS_ATTACHMENTS:
            return applications_attachments()
        if self is CandidatesListRequestExpand.ATTACHMENTS:
            return attachments()
