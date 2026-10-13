# -*- coding: utf-8 -*-
"""
FSF2026 — the one file to edit when photographs and videos arrive.

Nothing else has to change: the page, the lightbox and the grid read this.

PHOTOGRAPHS
    1. Put the file in  static/media/fsf2026/   (JPEG, PNG or WebP; about
       2000px on the long side is plenty).
    2. Add one entry to PHOTOS below:

           {"src": "hall-opening.jpg",
            "alt":     {"en": "What the picture shows.", "it": "Cosa mostra la foto."},
            "caption": {"en": "Optional line under it.",  "it": "Riga facoltativa."}},

       alt is for people who cannot see the picture and is required;
       caption is optional. Width and height are read from the file itself.
    3. Optional, for lighter phone downloads: run  python3 src/gen_fsf2026.py
       on a Mac. It writes -480 / -800 / -1200 copies beside each original
       and the page starts using them on its own.

VIDEOS
    A file of your own:
           {"file": "opening.mp4", "poster": "opening-poster.jpg",
            "title": {"en": "...", "it": "..."}}
    or one hosted on YouTube / Vimeo (nothing is loaded from them, and no
    cookie is set, until the visitor presses play):
           {"youtube": "VIDEO_ID", "poster": "talk-poster.jpg",
            "title": {"en": "...", "it": "..."}}
           {"vimeo": "VIDEO_ID", "poster": "...", "title": {...}}
    The poster is a still of your own in static/media/fsf2026/.

THE DAY
    CHAPTERS is the order of the day. Each entry:
           {"time": "10:00", "title": {"en": "...", "it": "..."},
            "text":  {"en": "...", "it": "..."}}
    time and text are optional.

While PHOTOS and VIDEOS are both empty the page shows a finished "archive in
preparation" passage instead of a gallery, and while CHAPTERS is empty it
shows no timeline at all. Each part switches on by itself with its first real
entry. Nothing here is invented: no schedule, speaker, number or quotation
appears on the page unless it is written below.
"""

CHAPTERS = [
]

PHOTOS = [
]

VIDEOS = [
]
