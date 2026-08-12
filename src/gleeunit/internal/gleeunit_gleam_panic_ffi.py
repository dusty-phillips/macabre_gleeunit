from gleam_builtins import (
    Error,
    GleamList,
    GleamPanic as GleamPanicError,
    Ok,
    to_gleam_list,
)

from gleeunit.internal.gleam_panic import (
    GleamPanic as GleamPanicRecord,
    Panic as PanicKind,
    Todo as TodoKind,
    LetAssert as LetAssertKind,
    Assert as AssertKind,
    BinaryOperator,
    FunctionCall,
    OtherExpression,
    AssertedExpression,
    Literal,
    Expression,
    Unevaluated,
)


def _to_py_list(a):
    out = []
    while isinstance(a, GleamList):
        out.append(a.value)
        a = a.tail
    return out


def from_dynamic(data):
    if not isinstance(data, dict):
        return Error(None)

    gleam_error = data.get("gleam_error")
    if gleam_error == "panic":
        kind = PanicKind()
    elif gleam_error == "todo":
        kind = TodoKind()
    elif gleam_error == "let_assert":
        kind = LetAssertKind(
            data["start"], data["end"], data["pattern_start"],
            data["pattern_end"], data["value"],
        )
    elif gleam_error == "assert":
        kind = AssertKind(
            data["start"], data["end"], data["expression_start"],
            _assert_kind(data),
        )
    else:
        return Error(None)

    return Ok(GleamPanicRecord(
        data["message"], data["file"], data["module"], data["function"],
        data["line"], kind,
    ))


def _assert_kind(data):
    kind = data["kind"]
    if kind == "binary_operator":
        return BinaryOperator(
            data["operator"], _expression(data["left"]),
            _expression(data["right"]),
        )
    if kind == "function_call":
        return FunctionCall(to_gleam_list([
            _expression(arg) for arg in _to_py_list(data["arguments"])
        ]))
    return OtherExpression(_expression(data["expression"]))


def _expression(data):
    kind = data["kind"]
    if kind == "literal":
        return AssertedExpression(data["start"], data["end"],
                                  Literal(data["value"]))
    if kind == "expression":
        return AssertedExpression(data["start"], data["end"],
                                  Expression(data["value"]))
    return AssertedExpression(data["start"], data["end"], Unevaluated())
