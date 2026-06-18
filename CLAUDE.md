# Python Coding Style

This file defines how I want Python written. Follow it strictly. When generating
or editing code, match this style exactly. The guiding principle is: **the
simplest thing that is also elegant, with the smallest possible git diff.**

## Core philosophy

- C-style structure and clarity, while still using the real advantages of Python.
- Simplest possible solution that is still elegant. No cleverness for its own sake.
- Smallest possible diff when changing existing code. Touch only what must change.
- Code explains itself through structure, naming, and type hints. Not through prose.
- No premature abstraction. No speculative generality.

## Formatting

- No autoformatter. Formatting is done by hand (or by AI matching the existing style).
  Do not reflow or restructure regions that are not part of the change.
- No hard line-length limit. Do NOT wrap long lines to satisfy a column count.
- **Never** stack function parameters or call arguments vertically (one per line).
  Keep call signatures and call sites on one line even when long. If a call is
  genuinely unwieldy, refactor to remove the need rather than exploding it vertically.

## Blank lines

- Logically related constants: no blank line between them (they form one group).
- Different logical groups of constants: one blank line between groups.
- Between logical groups of statements inside a larger scope: 2 blank lines.
- Before/after class definitions: 2 blank lines.
- Between top-level functions: 1 blank line.
- Functions are placed above classes when a file contains both.

## File / module layout

Top to bottom, every file follows this order:

1. Imports (always at the very top).
2. Constants.
3. Functions.
4. Classes (below functions).
5. `main()` (small, often a loop) at the very bottom.
6. `if __name__ == "__main__":` guard last.

Dataclasses, Pydantic models, and shared types do **not** live inline in feature
files. They go in separate, global type/model modules and are imported, because
they are reused across multiple places.

## Imports

- Imports always at the top of the file.
- `import module` vs `from module import name` is decided case by case. Use whichever
  reads better; VSCode can jump to the source either way.
- **Never** write large `from x import a, b, c, d, e, f, ...` lists. If a module needs
  many names, `import module` and qualify with `module.name` instead.
- Prefer `import module` for stdlib namespaces where the prefix is informative
  (`os.`, `json.`, `subprocess.`).

## Naming

- Functions and variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `SCREAMING_SNAKE_CASE`.
- Use the leading-underscore `_private` convention for internal names. (Used often.)

## Type hints

Type hints are the most important documentation tool here — they replace most comments.

- Add type hints wherever they earn their place as tooling leverage: IDE hover,
  autocomplete, and code suggestions. This means function signatures, class fields,
  and any variable where hovering for the type is useful.
- Do NOT annotate obvious trivial locals where the hint adds nothing.
- On classes especially, annotate fully so autocomplete and suggestions work well.

## Data types

- Dataclasses are a primary, favored tool — treat them like C typedefs/structs.
- Pydantic models likewise, where validation/parsing matters.
- Do NOT use `frozen=True` by default.
- Define these in shared type/model modules, not inline (see file layout).

## Mutability and data flow

- Default: take data, return fresh data. Do not mutate caller-owned objects as a
  surprise side effect.
- Mutate in place only when that is the obvious, named purpose of the function
  (e.g. `normalize_entries(entries)`), or for large objects / state-tracking objects
  where copying is wasteful. Large objects and state trackers should be modified in
  place. Correct function naming is what signals this — the name must make the
  mutation obvious.

## Comprehensions and chaining

- Prefer explicit `for` loops with `.append()` over list/dict/set comprehensions.
- Very simple single-line comprehensions are acceptable (`[x.name for x in items]`),
  but anything with a condition or nesting becomes an explicit loop.
- Generator expressions inside `sum(...)`, `any(...)`, `all(...)`, `"".join(...)` are
  fine and often the simplest thing — keep those.
- Method chaining: at most 2 calls in a chain. Beyond that, break into named
  intermediate variables. Avoid `a().b().c()`-style chains.

## Strings

- f-strings everywhere for normal string building.
- **Exception:** logging uses `%s`-style deferred formatting, never f-strings:
  `logger.info("started %s", name)` — not `logger.info(f"started {name}")`.

## Error handling

- Real errors are raised. Let genuine faults propagate with a traceback (this is
  desirable in services — it lands in the journal and shows exactly what went wrong).
- For expected "this might not work" cases (e.g. parsing a string to a number that
  might not be valid), return `None` and check at the call site. Do not raise for
  routine expected-failure cases.

## Comments

Keep comments to a minimum. Code should explain itself. Comments must *add* something
the code cannot. Specifically, DO comment:

- **Sources:** if code came from somewhere, link/attribute it.
- **Borrowed ideas:** if an idea is taken from anywhere, document it.
- **Workarounds:** explain why the workaround exists.
- **Business logic:** rules that aren't derivable from the code itself.
- **Weird bugs / behavior:** non-obvious constraints or surprising behavior.

DO NOT comment default/obvious behavior. No narrating what the code plainly does.
No `# ===== SECTION =====` banners or comment-header blocks — use logical grouping
(blank lines + ordering) to separate concerns instead.

## Docstrings

- Do not use docstrings. They take up too much space. Type hints and names carry it.

## Services (systemd, long-running)

- Use the `logging` module (configured to stdout/journal) for debug output, not `print`.
- Keep `main()` small, often structured as a loop.

## Corrections (learned)

<!-- Append new rules here as they come up. Every "no, I meant..." becomes a permanent rule. Keep them specific and enforceable. -->

- **Aligned assignment blocks:** within a contiguous group of related assignments
  (e.g. a `Color` / `Spacing` block, or a run of class fields), pad with spaces so the
  `=` signs line up in one column. Alignment is scoped to the group — it resets at each
  blank line / group boundary, and each group is aligned to its own longest name.
  If the lines carry trailing `#` comments, align those into their own column too
  (padded past the group's longest value).

- **Filesystem paths use `pathlib.Path`, always.** Construct paths with the `/`
  operator and use `Path` methods (`.read_text()`, `.write_text()`, `.exists()`,
  `.parent`, etc.). Never fall back to `os` / `os.path` for path work, and never build
  paths by string concatenation or f-strings. Annotate path params/fields as `Path`.