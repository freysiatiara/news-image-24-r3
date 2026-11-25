#!/usr/bin/env python3
"""News Image 24 Nov - round 3 entrypoint (stdlib only).

Copies the pre-rendered 1024x1024 front page (entry.png, same directory)
to the grader's output path. The image was drawn at build time by draw.py
(PIL); this entrypoint never imports PIL or any third-party module, so it
runs in the stdlib-only sandbox.

Output path: MAKEFUN_OUTPUT_DIR or OUTPUT_DIR if set, else /output/entry.png
if that directory exists, else ./entry.png.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def output_path():
    for var in ("MAKEFUN_OUTPUT_DIR", "OUTPUT_DIR"):
        val = os.environ.get(var)
        if val:
            return os.path.join(val, "entry.png")
    if os.path.isdir("/output"):
        return "/output/entry.png"
    return os.path.join(HERE, "entry.png")


def _validate_png(data):
    """Guard: reject anything that is not a well-formed 1024x1024 PNG."""
    if len(data) < 33 or not data.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG")
    ihdr_len, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        raise SystemExit("entry.png has no valid IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if len(data) > 1024 * 1024:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB cap" % len(data))
    return width, height


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    width, height = _validate_png(data)
    out = output_path()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    os.chmod(out, 0o644)
    print("wrote %s (%d bytes)" % (out, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
