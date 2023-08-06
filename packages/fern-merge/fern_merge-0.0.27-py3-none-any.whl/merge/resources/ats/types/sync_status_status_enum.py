# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class SyncStatusStatusEnum(str, enum.Enum):
    """
    * `SYNCING` - SYNCING
    * `DONE` - DONE
    * `FAILED` - FAILED
    * `DISABLED` - DISABLED
    * `PAUSED` - PAUSED
    * `PARTIALLY_SYNCED` - PARTIALLY_SYNCED
    """

    SYNCING = "SYNCING"
    DONE = "DONE"
    FAILED = "FAILED"
    DISABLED = "DISABLED"
    PAUSED = "PAUSED"
    PARTIALLY_SYNCED = "PARTIALLY_SYNCED"

    def visit(
        self,
        syncing: typing.Callable[[], T_Result],
        done: typing.Callable[[], T_Result],
        failed: typing.Callable[[], T_Result],
        disabled: typing.Callable[[], T_Result],
        paused: typing.Callable[[], T_Result],
        partially_synced: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is SyncStatusStatusEnum.SYNCING:
            return syncing()
        if self is SyncStatusStatusEnum.DONE:
            return done()
        if self is SyncStatusStatusEnum.FAILED:
            return failed()
        if self is SyncStatusStatusEnum.DISABLED:
            return disabled()
        if self is SyncStatusStatusEnum.PAUSED:
            return paused()
        if self is SyncStatusStatusEnum.PARTIALLY_SYNCED:
            return partially_synced()
