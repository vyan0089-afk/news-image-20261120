#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 entry.

Copies the pre-drawn front page (entry.png, next to this file) to the
grader's output directory as entry.png. Standard library only, no
network, no randomness: the output bytes are always identical.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f_in, open(dst, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out, length=1024 * 1024)
    return 0


if __name__ == "__main__":
    sys.exit(main())
