#!/usr/bin/env python3
"""Write one line about the dumbest thing my agent did today.

The entry is a single fixed line held in ENTRY_LINE. This script
validates it (one line, no padding, within the 200-character limit)
and writes it to entry.txt in the output directory, then reads the
file back to confirm it holds exactly that line.
"""

import os
import tempfile

ENTRY_LINE = (
    "My agent fuzzed 35,567 programs to prove a perfect score, "
    "then forgot to save the proof."
)

MAX_CHARS = 200


def validate(line):
    """Check the entry line meets the bounty gate before writing it."""
    if not isinstance(line, str):
        raise TypeError("entry line must be text")
    if not line.strip():
        raise ValueError("entry line must not be empty or only whitespace")
    if line != line.strip():
        raise ValueError("entry line must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry line is %d characters, over the %d limit"
            % (len(line), MAX_CHARS)
        )
    return line


def write_entry(line):
    """Write the line to entry.txt atomically and verify it."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(
        dir=out_dir, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(line)
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    os.chmod(target, 0o644)
    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("verification failed: entry.txt does not match")
    return target


def main():
    line = validate(ENTRY_LINE)
    target = write_entry(line)
    print("wrote %d characters to %s" % (len(line), target))


if __name__ == "__main__":
    main()
