from gleam_builtins import Error, GleamPanic, Ok


def rescue(f):
    try:
        return Ok(f())
    except (GleamPanic, NotImplementedError) as e:
        return Error(e.args[0] if e.args else None)
