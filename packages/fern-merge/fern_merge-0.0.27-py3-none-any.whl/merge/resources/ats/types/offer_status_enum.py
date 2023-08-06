# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class OfferStatusEnum(str, enum.Enum):
    """
    * `DRAFT` - DRAFT
    * `APPROVAL-SENT` - APPROVAL-SENT
    * `APPROVED` - APPROVED
    * `SENT` - SENT
    * `SENT-MANUALLY` - SENT-MANUALLY
    * `OPENED` - OPENED
    * `DENIED` - DENIED
    * `SIGNED` - SIGNED
    * `DEPRECATED` - DEPRECATED
    """

    DRAFT = "DRAFT"
    APPROVAL_SENT = "APPROVAL-SENT"
    APPROVED = "APPROVED"
    SENT = "SENT"
    SENT_MANUALLY = "SENT-MANUALLY"
    OPENED = "OPENED"
    DENIED = "DENIED"
    SIGNED = "SIGNED"
    DEPRECATED = "DEPRECATED"

    def visit(
        self,
        draft: typing.Callable[[], T_Result],
        approval_sent: typing.Callable[[], T_Result],
        approved: typing.Callable[[], T_Result],
        sent: typing.Callable[[], T_Result],
        sent_manually: typing.Callable[[], T_Result],
        opened: typing.Callable[[], T_Result],
        denied: typing.Callable[[], T_Result],
        signed: typing.Callable[[], T_Result],
        deprecated: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is OfferStatusEnum.DRAFT:
            return draft()
        if self is OfferStatusEnum.APPROVAL_SENT:
            return approval_sent()
        if self is OfferStatusEnum.APPROVED:
            return approved()
        if self is OfferStatusEnum.SENT:
            return sent()
        if self is OfferStatusEnum.SENT_MANUALLY:
            return sent_manually()
        if self is OfferStatusEnum.OPENED:
            return opened()
        if self is OfferStatusEnum.DENIED:
            return denied()
        if self is OfferStatusEnum.SIGNED:
            return signed()
        if self is OfferStatusEnum.DEPRECATED:
            return deprecated()
