from gleam_builtins import Error, GleamPanic as GleamPanicError, Ok

from gleeunit.internal.gleam_panic import (
    GleamPanic as GleamPanicRecord,
    Panic as PanicKind,
    Todo as TodoKind,
)


def from_dynamic(data):
    if isinstance(data, NotImplementedError):
        return Ok(GleamPanicRecord(str(data), "", "", "", 0, TodoKind()))

    if isinstance(data, GleamPanicError):
        return Ok(GleamPanicRecord(str(data), "", "", "", 0, PanicKind()))

    return Error(None)
