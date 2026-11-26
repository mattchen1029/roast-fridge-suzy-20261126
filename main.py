"""One line roasting the smart fridge.

Writes one line of plain text (at most 200 characters) to
$MAKEFUN_OUTPUT_DIR/entry.txt (or /output/entry.txt by default).
"""

import os

MIN_CHARS = 1
MAX_CHARS = 200
OUTPUT_NAME = "entry.txt"

TEXT = (
    "My smart fridge has Wi-Fi, a touchscreen, and a camera inside — "
    "yet its smartest move in five years was beeping at me for eating "
    "ice cream at 2 a.m. like a disappointed parent."
)


def validate_line(line: str) -> str:
    """Enforce the competition gate: 1-200 chars, single line, non-blank."""
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        raise ValueError(
            f"line is {len(line)} chars, must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    return line


def write_entry(output_dir: str) -> str:
    """Write the validated line to <output_dir>/entry.txt."""
    line = validate_line(TEXT)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_NAME)
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    return path


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(output_dir)
    print(f"wrote {len(TEXT)} chars to {path}")


if __name__ == "__main__":
    main()
