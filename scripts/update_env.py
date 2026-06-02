from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: update_env.py <file> <key> <value>")

    path = Path(sys.argv[1])
    key = sys.argv[2]
    value = sys.argv[3]

    lines = path.read_text().splitlines() if path.exists() else []
    prefix = f"{key}="
    updated = False
    next_lines: list[str] = []
    for line in lines:
        if line.startswith(prefix):
            next_lines.append(f"{key}={value}")
            updated = True
        else:
            next_lines.append(line)

    if not updated:
        next_lines.append(f"{key}={value}")

    path.write_text("\n".join(next_lines) + "\n")


if __name__ == "__main__":
    main()

