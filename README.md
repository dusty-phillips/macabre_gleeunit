# macabre_gleeunit

A simple test runner for Gleam.

This is a fork of [lpil/gleeunit](https://github.com/lpil/gleeunit)
(Apache-2.0) that adds Python externals for
[macabre](https://github.com/anomalyco/macabre)'s Python target. The fork
preserves the full upstream history. The only Gleam changes are the added
`@external(python, ...)` attributes and an `import gleeunit/internal/reporting`
in `src/gleeunit.gleam` (macabre compiles only modules reachable from the
project entry point, and the Python runner needs the `reporting` module
compiled). The Python implementations live in `src/gleeunit_ffi.py` and
`src/gleeunit/internal/gleeunit_gleam_panic_ffi.py` (mirroring `gleeunit_ffi.mjs`
and `gleeunit_gleam_panic_ffi.mjs`).

Because the module is still named `gleeunit`, existing test files keep working
with:

```gleam
// In test/yourapp_test.gleam
import gleeunit

pub fn main() {
  gleeunit.main()
}
```

Now any public function with a name ending in `_test` in the `test` directory
will be found and run as a test.

```gleam
pub fn some_function_test() {
  assert some_function() == "Hello!"
}
```

## Using it with macabre

Add the fork to a macabre project (macabre resolves dependencies from git),
along with `macabre_stdlib` (which provides the `gleam/*` modules):

```toml
[dependencies]
macabre_stdlib = { git = "git@github.com:dusty-phillips/macabre_stdlib.git", ref = "main" }
macabre_gleeunit = { git = "git@github.com:dusty-phillips/macabre_gleeunit.git", ref = "main" }
```

Compile the project (including its `test/` directory) with macabre and run the
output with Python:

```sh
python3 build/dev/python
```

The exit status is `0` when all tests pass and `1` otherwise.

## Differences from upstream

The Erlang and JavaScript targets are unchanged. On the Python target:

- `panic` and `todo` (and `let assert`) are reported as test failures, as on the
  other targets.
- Macabre's Python runtime raises panics as a bare exception carrying only the
  message, so the `file`/`line`/`module`/`function` panic metadata is not
  available and the reported location is empty. Tests that assert on the exact
  panic metadata (as in `test/gleam_panics_test.gleam`) only pass on Erlang and
  JavaScript.

## Development

Macabre targets Python, so the stock `gleam` compiler (which does not recognise
the `python` external target) cannot check or format this package. `./test.sh`
syntax-checks the Python FFI instead.

## License

Apache-2.0, matching upstream gleeunit.
