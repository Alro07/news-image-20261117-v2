#!/usr/bin/env python3
"""news-image-20261117-v2 entry (Python 3.13, standard library only).

The front page is drawn by tools/gen_image.py (Pillow, run locally at
build time) and committed here as entry.png; this program only copies
that committed image to /output/entry.png. Deterministic: the same
bytes on every run, no network, no fonts needed at grade time.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    with open(src, "rb") as fh:
        if fh.read(8) != b"\x89PNG\r\n\x1a\n":
            raise SystemExit("entry.png is not a PNG file")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
