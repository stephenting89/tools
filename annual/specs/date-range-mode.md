# Date Range Mode

> Add a two-date mode to `annual` so users can calculate annualized return over a date range.

## Overview

Add a two-date mode to `annual` so users can calculate annualized return over a historical date range. The existing 3-arg form (`annual <premium> <collateral> <expiry>`) is unchanged. A new 4-arg form (`annual <premium> <collateral> <from> <to>`) computes days as `to - from` instead of `expiry - today`.

## Requirements

1. `annual <premium> <collateral> <expiry>` — existing behavior unchanged; days = `expiry - today`
2. `annual <premium> <collateral> <from> <to>` — new mode; days = `to - from`
3. All dates (both modes) use `parse_expiry` — `M/D`, `M/D/YY`, or `M/D/YYYY`; if no year given, assumes current year; no auto-advance (5/1 always means this year's May 1)
4. If arg count is not 3 or 4, print usage and exit with an error
5. If `to - from` is zero or negative, print an error and exit
6. Output format is the same as existing mode

## Constraints

- Pure stdlib — no third-party dependencies (`sys`, `datetime`, `time` only)
- Single file: `annual.py`
- Python 3.10+ (uses `date | None` union type hint)

## Data Model

No persistent state — inputs are CLI args, output is a single printed line.

## Behavior

**3-arg mode (unchanged):**
- Parse `<expiry>` via `parse_expiry`
- `days = expiry - today`
- `annualized = (premium / collateral) * (365 / days) * 100`
- Print result line

**4-arg mode (new):**
- Parse `<from>` and `<to>` each via `parse_expiry`
- `days = to - from`
- Same annualized formula
- Same output format

## Edge Cases

1. `to - from` is zero or negative — error and exit
2. Arg count not 3 or 4 — print usage and exit
3. Non-numeric premium or collateral — existing error handling covers this
4. Unparseable date string for either `from` or `to` — error and exit

## Acceptance Criteria

1. `annual 350 10000 5/15` — works as before
2. `annual 350 10000 5/1 5/15` — calculates annualized return over 14 days
3. `annual 350 10000 5/1 4/15` — errors with "to date must be after from date"
4. `annual 350 10000 5/1 5/1` — errors (zero days)
5. `annual 350 10000 5/1 5/15 6/1` — errors with usage message (too many args)
6. `annual 350 10000 abc 5/15` — errors on unparseable from date

## Out of Scope

- No changes to output formatting
- No support for additional date formats
- No interactive mode or config file

## Decisions Log

- Reuse `parse_expiry` for range mode dates rather than writing a new parser — keeps behavior consistent and avoids duplication
- Removed auto-advance logic from `parse_expiry` — dates are always literal; use M/D/YY to specify a different year explicitly
- Zero days treated as an error — 0 DTE annualized return is meaningless

## Open Questions

None.
