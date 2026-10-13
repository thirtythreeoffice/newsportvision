# -*- coding: utf-8 -*-
"""Lighter copies of the FSF2026 photographs, for phones.

    python3 src/gen_fsf2026.py

For every photograph named in src/fsf2026_media.py this writes -480, -800 and
-1200 copies beside the original in static/media/fsf2026/, using the image
tool every Mac already has (sips). The page uses them on its own once they
exist; nothing has to be edited. Optional: without them the page simply
serves the original to everyone.
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import fsf2026_media as m

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "static", "media", "fsf2026")
made = 0
for ph in m.PHOTOS:
    src = os.path.join(DIR, ph["src"])
    if not os.path.isfile(src):
        sys.exit("missing: static/media/fsf2026/%s" % ph["src"])
    stem, ext = ph["src"].rsplit(".", 1)
    width = int(subprocess.check_output(["sips", "-g", "pixelWidth", src]).split()[-1])
    for w in (480, 800, 1200):
        out = os.path.join(DIR, "%s-%d.%s" % (stem, w, ext))
        if w < width and not os.path.exists(out):
            subprocess.check_call(["sips", "--resampleWidth", str(w), src, "--out", out],
                                  stdout=subprocess.DEVNULL)
            made += 1
print("wrote %d copies" % made)
