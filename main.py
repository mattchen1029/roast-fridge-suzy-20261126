#!/usr/bin/env python3
"""Roast Your Fridge — one line, one laugh.

Competition: a single line of plain text, at most 200 characters, that
roasts a smart fridge. This program validates the line against the
competition gate and writes it to entry.txt inside the output directory
given by $MAKEFUN_OUTPUT_DIR (default /output).

The line itself is fixed: it is the entry, not a template. Validation
exists so a future edit that breaks the 1-200 character, single-line
rule fails loudly instead of shipping a bad entry.
"""

import os
import sys
from pathlib import Path

# Competition gate: the entry must be one line of 1-200 characters.
MIN_CHARS = 1
MAX_CHARS = 200

# Output file name inside the output directory.
ENTRY_FILENAME = "entry.txt"

# Fallback output directory when $MAKEFUN_OUTPUT_DIR is unset.
DEFAULT_OUTPUT_DIR = "/output"

# The entry. One line, 176 characters, no trailing newline when written.
ENTRY_LINE = (
    "My smart fridge has Wi-Fi, a touchscreen, and a camera inside \u2014 "
    "yet its smartest move in five years was beeping at me for eating "
    "ice cream at 2 a.m. like a disappointed parent."
)


def char_count(line: str) -> int:
    """Count characters the way the competition does: code points."""
    return len(line)


def ensure_single_line(line: str) -> None:
    """Reject any line break or carriage return in the entry."""
    if any(ch in line for ch in ("\n", "\r")):
        raise ValueError("entry must be a single line (no line breaks)")


def validate_line(line: str) -> str:
    """Check the entry against the competition gate and return it.

    Raises ValueError when the line is blank, too short, too long, or
    spans more than one line.
    """
    if not line.strip():
        raise ValueError("entry must not be blank")
    ensure_single_line(line)
    count = char_count(line)
    if count < MIN_CHARS or count > MAX_CHARS:
        raise ValueError(
            f"entry is {count} characters; competition allows "
            f"{MIN_CHARS}-{MAX_CHARS}"
        )
    return line


def resolve_output_dir() -> Path:
    """Read the output directory from the environment, with a default."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return Path(raw)


def write_entry(output_dir: Path, line: str) -> Path:
    """Write the validated entry line to <output_dir>/entry.txt.

    Returns the path written. The file holds exactly the line, with no
    trailing newline, so the bytes on disk match the entry exactly.
    """
    checked = validate_line(line)
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / ENTRY_FILENAME
    target.write_text(checked, encoding="utf-8")
    return target


def main(argv=None) -> int:
    """Validate the entry and write it out; return a process exit code."""
    del argv  # no command-line arguments are defined for this program
    try:
        target = write_entry(resolve_output_dir(), ENTRY_LINE)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {char_count(ENTRY_LINE)} chars to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
