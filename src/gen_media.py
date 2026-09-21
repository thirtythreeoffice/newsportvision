# -*- coding: utf-8 -*-
"""Generate responsive variants (avif / webp / jpg at 480, 800, 1200, 1600)
   from the live Wix originals, using their transform + content-negotiation
   endpoints.

   The ladder is set by the screens that matter most: a phone column is ~390
   CSS px, which is 780 device px at 2x and 1170 at 3x — so 800 and 1200 exist
   so that a phone never has to take the 1600 file. Quality 75 is visually
   indistinguishable from 86 on these photographs at a third less weight."""
import urllib.request, os, sys, time
sys.path.insert(0, os.path.dirname(__file__))
from content import MEDIA

ORIGIN = {
 "skate-architecture.jpg": "40c3f785a6434c7f96c8beec010b7c36.jpg",
 "leap-street.jpg":        "b9cdd1cd97184fa590d48fb6e8628956.jpg",
 "guides-three.jpg":       "7ae5d6_dfef041edd3c4448867825e9c201808f~mv2_d_5472_3648_s_4_2.jpg",
 "guide-open.jpg":         "7ae5d6_2f0543ae92cf4700a6954f83a5aec2ee~mv2_d_5472_3648_s_4_2.jpg",
 "court-lines.jpg":        "1c3c8bba147747ad8d1dc9e652b3306a.jpg",
 "desk-editorial.jpg":     "035244_881cbe4617f449cab844cb6a48b5fbeb~mv2_d_2475_2475_s_4_2.jpeg",
 "basket-youth.jpg":       "95a124ec19b54ac3bf1b934302293e26.jpg",
 "basket-hoop.jpg":        "90d82a7070a44e1393caea64b2967a60.jpg",
 "coach-youth.jpg":        "99d3f0df10794b1e92c8fe0792b7775b.jpg",
 "school-bus.jpg":         "1b9dfbb7c16f4f83a7a86b613e09e2a2.jpg",
 "summit-room.jpg":        "5a2ce0eccfe64763b4a354eed7aa0f02.jpg",
 "finish-line.jpg":        "5702428b4f4e45faa10e14ba7ed8b24e.jpg",
 "course-room.jpg":        "d1c5cd0055c94e3bb1acee9e2fda9f0e.jpg",
 "gathering.jpg":          "f4978962a2b147999e396ec664c46c45.jpg",
}
ACCEPT = {
 "avif": "image/avif,image/webp,image/*,*/*;q=0.8",
 "webp": "image/webp,image/*,*/*;q=0.8",
 "jpg":  "image/jpeg,image/*;q=0.8",
}
WIDTHS = (480, 800, 1200, 1600)
QUALITY = 75
OUT = os.path.join(os.path.dirname(__file__), "..", "static", "media")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

total = 0
for key, m in MEDIA.items():
    if m.get("mark"):
        continue
    src = m["src"]; stem = src.rsplit(".", 1)[0]
    oid = ORIGIN[src]
    ar = m["h"] / m["w"]
    for w in WIDTHS:
        h = int(round(w * ar))
        base = "https://static.wixstatic.com/media/%s/v1/fill/w_%d,h_%d,al_c,q_%d,enc_auto/%s" % (oid, w, h, QUALITY, oid)
        for ext, acc in ACCEPT.items():
            out = os.path.join(OUT, "%s-%d.%s" % (stem, w, ext))
            if os.path.exists(out) and os.path.getsize(out) > 1500:
                total += os.path.getsize(out); continue
            req = urllib.request.Request(base, headers={"User-Agent": UA, "Accept": acc})
            try:
                d = urllib.request.urlopen(req, timeout=60).read()
                open(out, "wb").write(d)
                total += len(d)
            except Exception as e:
                print("ERR", out, e)
            time.sleep(0.05)
    print("%-24s ok" % stem)
print("total %.1f MB across %d files" % (total/1048576, len(os.listdir(OUT))))
