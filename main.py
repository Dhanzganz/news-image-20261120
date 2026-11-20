#!/usr/bin/env python3
"""Entry point for the news-image-20261120 make.fun submission.

The picture itself (entry.png, drawn by draw.py) sits next to this
file.  My job is deliberately small: check that the PNG is sane and
within the competition limits, then copy it byte-for-byte to the
output location -- $MAKEFUN_OUTPUT_DIR/entry.png when that variable
is set, otherwise /output/entry.png.

Standard library only, no network.  Python 3.13.
"""

import os
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
MAX_BYTES = 1_048_576  # 1 MiB


def read_png_size(data):
    """Return (width, height) parsed from the IHDR chunk."""
    if len(data) < 24 or not data.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file (bad signature)")
    if data[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def validate(data):
    """Raise ValueError if the image breaks any competition limit."""
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"entry.png is {len(data)} bytes, over the {MAX_BYTES} limit"
        )
    if not data.rstrip(b"\x00").endswith(b"IEND\xaeB`\x82"):
        raise ValueError("entry.png looks truncated (no IEND chunk)")
    width, height = read_png_size(data)
    if width == 0 or height == 0:
        raise ValueError("entry.png has a zero dimension")
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        raise ValueError(
            f"entry.png is {width}x{height}, over the "
            f"{MAX_WIDTH}x{MAX_HEIGHT} limit"
        )
    return width, height


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    with open(source, "rb") as fh:
        data = fh.read()

    width, height = validate(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    with open(target, "wb") as fh:
        fh.write(data)

    print(f"entry.png OK ({width}x{height}, {len(data)} bytes) -> {target}")
    return 0


def main():
    try:
        return run()
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
