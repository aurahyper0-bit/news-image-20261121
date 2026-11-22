#!/usr/bin/env python3
"""Copy the bundled news image to the make.fun output directory.

Reads entry.png next to this script and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when unset).
Standard library only, no network, deterministic.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    # Validate the source before writing: it must be a real PNG under 1 MiB.
    with open(src, "rb") as f:
        header = f.read(8)
    if header != b"\x89PNG\r\n\x1a\n":
        print(f"error: {src} is not a valid PNG", file=sys.stderr)
        return 1
    if os.path.getsize(src) >= 1024 * 1024:
        print(f"error: {src} is 1 MiB or larger", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
