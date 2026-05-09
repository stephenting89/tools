#!/usr/bin/env python3
"""Calculates the annualized return rate of a sold put option.

Usage:
    annual <premium> <collateral> <expiry>
    annual <premium> <collateral> <from> <to>

Examples:
    annual 350 10000 5/15
    annual 350 10000 5/15/27
    annual 350 10000 5/15/2027
    annual 350 10000 5/1 5/15
"""

import sys
import time
from datetime import date


DATE_FORMATS = ["%m/%d/%Y", "%m/%d/%y"]


# Parses a date string in M/D, M/D/YY, or M/D/YYYY format.
# If no year is given, injects the current year and retries.
# If the resulting date is today or in the past, advances to next year.
# Returns a date object, or None if parsing fails.
def parse_expiry(s: str) -> date | None:
    s_with_year = s if s.count("/") == 2 else f"{s}/{date.today().year}"

    for fmt in DATE_FORMATS:
        try:
            return date(*time.strptime(s_with_year, fmt)[:3])
        except ValueError:
            continue
    return None


# Computes annualized return: (premium / collateral) * (365 / days).
# Prints a single formatted result line.
def main() -> None:
    if len(sys.argv) not in (4, 5):
        print("Usage: annual <premium> <collateral> <expiry>")
        print("       annual <premium> <collateral> <from> <to>")
        sys.exit(1)

    try:
        premium = float(sys.argv[1])
    except ValueError:
        print(f"[ERROR] Invalid premium '{sys.argv[1]}' — must be a number")
        sys.exit(1)

    try:
        collateral = float(sys.argv[2])
    except ValueError:
        print(f"[ERROR] Invalid collateral '{sys.argv[2]}' — must be a number")
        sys.exit(1)

    if collateral <= 0:
        print("[ERROR] Collateral must be greater than zero")
        sys.exit(1)

    if premium < 0:
        print("[ERROR] Premium cannot be negative")
        sys.exit(1)

    if len(sys.argv) == 4:
        expiry = parse_expiry(sys.argv[3])
        if expiry is None:
            print(f"[ERROR] Could not parse date '{sys.argv[3]}' — use M/D, M/D/YY, or M/D/YYYY")
            sys.exit(1)

        today = date.today()
        days = (expiry - today).days
        if days <= 0:
            print(f"[ERROR] Expiry date {expiry} is in the past")
            sys.exit(1)
    else:
        from_date = parse_expiry(sys.argv[3])
        if from_date is None:
            print(f"[ERROR] Could not parse date '{sys.argv[3]}' — use M/D, M/D/YY, or M/D/YYYY")
            sys.exit(1)

        to_date = parse_expiry(sys.argv[4])
        if to_date is None:
            print(f"[ERROR] Could not parse date '{sys.argv[4]}' — use M/D, M/D/YY, or M/D/YYYY")
            sys.exit(1)

        days = (to_date - from_date).days
        if days <= 0:
            print(f"[ERROR] To date must be after from date")
            sys.exit(1)

    annualized = (premium / collateral) * (365 / days) * 100

    print(f"\033[1m{annualized:.1f}% annualized  ({days} days, ${premium:,.0f} on ${collateral:,.0f})\033[0m")


if __name__ == "__main__":
    main()
