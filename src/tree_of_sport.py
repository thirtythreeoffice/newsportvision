"""The Tree of Sport, drawn for the web.

A redrawing of the panel on page 1 of the manifesto PDF (a 1642 x 896 raster
with its caption, seal and lettering baked in), built as geometry so that it
is sharp at any size and CULTURE is real text. It is drawn in the raster's own
coordinates, so the two can be laid over each other and compared; the
proportions below were measured from it (crown 924 x ~440 — a 1.7:1 dome —
trunk ~70 wide flaring to ~108, fork at y~455, horizon at 584 under the trunk,
roots from x 171 to 1460, the seven letters' positions and cap height). No
pixel of it is traced: every shape is placed by rule from a fixed seed.

Layers, back to front:
  sky              the panel: a vertical blue gradient with the soft
                   white-cyan glow behind the crown, as in the PDF.
  label, seal      THE TREE OF SPORT top left, the yellow NSV seal top right.
  roots            a wide spread just under the horizon, wavy, and many fine
                   tapering tendrils downward, mirroring the crown in mass.
  horizon          the dark green arc through the foot of the trunk.
  trunk            short, thick, dark chocolate, flaring at the base.
  crown            rosy-brown limbs fanning from the upper trunk and dividing
                   into fine twigs, carrying small almond leaves in two greens —
                   lacy, with sky showing between them — inside a smooth wide
                   dome.
  culture-letters  C U L T U R E, peach-orange, rounded bold, widely spaced on
                   a shallow V.
  roots-over       a few tendrils passing in front of L, T and U.
"""

import math
import random

W, H = 1642, 896
TX = 812                      # trunk axis
FORK_Y = 455                  # where the limbs leave the trunk
HORIZON = [(118, 668), (151, 658), (257, 635), (337, 620), (417, 608), (497, 599), (577, 592), (657, 587),
           (737, 584), (826, 583), (916, 584), (996, 588), (1076, 593), (1156, 600), (1236, 610),
           (1316, 623), (1396, 639), (1483, 660), (1524, 672)]
DOME = (801, 456, 468, 432)   # cx, base y, half width, height

# Colours as the PDF shows them on screen (sampled from its render, not from
# the raw raster, whose values read darker and duller).
SKY_STOPS = [(0, "#74ADDD"), (.22, "#77B1E0"), (.5, "#79B2E1"), (.62, "#73AEDE"), (.72, "#64A3D9"),
             (.8, "#579BD4"), (.9, "#498ECB"), (1, "#4186C7")]
GLOW = "#B4DCF0"
LEAVES = ("#4B943C", "#5CA443")     # the PDF's two greens: deeper, lighter
LIMB = "#8C5A3E"                     # the PDF's rosy brown
BARK = "#643214"                     # the PDF's chocolate (trunk, roots)
HORIZON_C = "#1E5028"
ORANGE = "#F08C46"                   # peach-orange
INK = "#1D1D1B"
YELLOW = "#FAC51C"

LETTERS = "CULTURE"
LETTER_X = [195, 403, 604, 810, 1020, 1227, 1441]
LETTER_Y = [777, 815, 832, 839, 835, 815, 778]
LETTER_SIZE = 66
LETTER_WEIGHT = 700


def f(v):
    r = round(v, 1)
    return str(int(r)) if r == int(r) else str(r)


def horizon_y(x):
    pts = HORIZON
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def in_dome(x, y, k=1.0):
    cx, base, a, b = DOME
    if y > base + 8:
        return False
    return ((x - cx) / (a * k)) ** 2 + ((base - y) / (b * k)) ** 2 <= 1


def catmull(pts, closed=False, prec=None):
    """A smooth curve through pts as cubic Beziers (no M)."""
    g = prec or f
    n = len(pts)
    d = ""
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[i - 1] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += "C%s %s %s %s %s %s" % (g(c1[0]), g(c1[1]), g(c2[0]), g(c2[1]), g(p2[0]), g(p2[1]))
    return d


def fi(v):
    return str(int(round(v)))


def ribbon(pts, w0, w1):
    """A tapered stroke along the polyline pts, as one closed smooth shape."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    outline = left + right[::-1]
    return "M%s %s" % (fi(outline[0][0]), fi(outline[0][1])) + catmull(outline, closed=True, prec=fi if w0 > 2.5 else f) + "Z"


def wavy(start, ang, length, steps, wave, rng, curl=0.0):
    """A centreline that wanders: a heading that drifts a little each step."""
    pts = [start]
    x, y = start
    a = ang
    seg = length / steps
    ph = rng.uniform(0, 6.3)
    for i in range(1, steps + 1):
        a += curl + wave * math.sin(ph + i * 1.3) * .35
        x += math.cos(a) * seg
        y += math.sin(a) * seg
        pts.append((x, y))
    return pts


# --- crown ---------------------------------------------------------------------
def reach(x, y, a, k=.97):
    lo, hi = 0.0, 900.0
    for _ in range(30):
        m = (lo + hi) / 2
        if in_dome(x + math.cos(a) * m, y + math.sin(a) * m, k):
            lo = m
        else:
            hi = m
    return lo


def crown():
    """Limbs that curve out of the upper trunk and divide, and leaves spread
    evenly through the dome (never closer than ~21 apart) so the crown is
    lacy, with sky between the leaves; each leaf turns the way growth runs
    there, out from the heart of the tree."""
    rng = random.Random(1642)
    limbs = []

    def grow(p, a, length, w, depth):
        length = min(length, reach(p[0], p[1], a) * (.9 if depth >= 2 else .48))
        if length < 16:
            return
        steps = 5 if depth < 2 else 3
        # limbs leave the trunk flatter and turn upward as they go
        curl = (.07 if math.cos(a) < 0 else -.07) if depth == 0 else 0
        pts = wavy(p, a, length, steps, .28, rng, curl=curl)
        w1 = max(w * .5, .9)
        limbs.append((pts, w, w1, depth))
        if depth >= 3:
            return
        heading = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        for c, (t, da) in enumerate(((.55, -.5), (.8, .45), (1.0, rng.uniform(-.2, .2)))):
            if depth == 2 and c == 0 and rng.random() < .5:
                continue
            i = min(int(round(t * steps)), steps)
            grow(pts[i], heading + da * rng.uniform(.8, 1.2), length * rng.uniform(.55, .7), w1 * .85, depth + 1)

    # the leader, and limbs leaving the trunk between y 470 and 260
    limbs.append(([(TX, 470), (TX - 2, 420), (TX + 3, 360), (TX, 300), (TX - 4, 240)], 30, 10, 0))
    fan = [(-170, 470, 18), (-10, 470, 18), (-150, 452, 20), (-30, 452, 20), (-132, 425, 20),
           (-48, 425, 20), (-116, 395, 17), (-64, 392, 17), (-102, 330, 13), (-78, 322, 13), (-92, 262, 11)]
    for a, y, w in fan:
        ang = math.radians(a + rng.uniform(-3, 3))
        start = (TX + (-8 if a < -90 else 8), y)
        grow(start, ang, reach(start[0], start[1], ang), w, 0)

    # leaves: an even, jittered scatter through the dome
    leaves = []
    cx, base, A, B = DOME
    pts = []
    tries = 0
    while tries < 40000:
        tries += 1
        x = rng.uniform(cx - A, cx + A)
        y = rng.uniform(base - B, base + 6)
        if not in_dome(x, y, .985):
            continue
        u, v = (x - cx) / A, (base - y) / B
        # the low middle of the crown stays open, so the limbs read there
        if v < .38 and abs(u) < .5 - v * .6:
            continue
        if any((x - px) ** 2 + (y - py) ** 2 < 289 for px, py in pts):
            continue
        pts.append((x, y))
    for x, y in pts:
        out = math.degrees(math.atan2(y - (base + 60), x - cx))
        leaves.append((x, y, out + rng.choice((-1, 1)) * rng.uniform(25, 70), rng.uniform(1.0, 1.25)))
    return limbs, leaves


def leaf_d(x, y, a, s):
    """An almond leaf ~22 long, placed; relative curves so a tone is one path."""
    pts = [(5, -6), (14, -7), (22, 0), (14, 7), (5, 6), (0, 0)]
    ca, sa = math.cos(math.radians(a)) * s, math.sin(math.radians(a)) * s
    P = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    rel = lambda p, o: "%s %s" % (f(p[0] - o[0]), f(p[1] - o[1]))
    return "M%s %sc%s %s %sc%s %s %sz" % (f(x), f(y), rel(P[0], (x, y)), rel(P[1], (x, y)), rel(P[2], (x, y)),
                                         rel(P[3], P[2]), rel(P[4], P[2]), rel(P[5], P[2]))


# --- roots -----------------------------------------------------------------------
def in_roots(x, y):
    """The root mass: under the horizon, a shallow mirror of the crown."""
    if y < horizon_y(x) + 6:
        return False
    return ((x - TX) / 500) ** 2 + ((y - 596) / 285) ** 2 <= 1


def roots():
    """Roots grow from the foot like the crown turned over: a wide, wavy
    spread just under the horizon and many fine tendrils falling from it."""
    rng = random.Random(896)
    back, over = [], []

    def reach_r(x, y, a):
        lo, hi = 0.0, 900.0
        for _ in range(28):
            m = (lo + hi) / 2
            if in_roots(x + math.cos(a) * m, y + math.sin(a) * m):
                lo = m
            else:
                hi = m
        return lo

    def grow(p, a, length, w, depth, sink):
        length = min(length, reach_r(p[0], p[1], a) * rng.uniform(.6, .98))
        if length < 14:
            return
        steps = 6 if depth < 2 else 4
        bend = sink if depth else (.09 if math.cos(a) < -.8 else (-.09 if math.cos(a) > .8 else sink))
        pts = wavy(p, a, length, steps, .5, rng, curl=bend)
        pts = [(x, max(y, horizon_y(x) + 8)) for x, y in pts]
        w1 = max(w * .45, .8)
        back.append(ribbon(pts, w, w1))
        if depth >= 3:
            return
        heading = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        for t in (.35, .65, 1.0):
            if depth >= 2 and t < .6:
                continue
            i = min(int(round(t * steps)), steps)
            down = math.radians(90)
            na = heading + (down - heading) * (.45 if t < 1 else .12) + rng.uniform(-.25, .25)
            grow(pts[i], na, length * rng.uniform(.5, .7), w1 * (.9 if t == 1 else .65), depth + 1, sink)

    foot = (TX, 604)
    for a, w in ((176, 18), (168, 18), (152, 16), (128, 13), (102, 12),
                 (78, 12), (52, 13), (28, 16), (12, 18), (4, 18)):
        side = 1 if a > 90 else -1
        ang = math.radians(a + rng.uniform(-3, 3))
        grow(foot, ang, 600, w, 0, side * .03)

    # three tendrils passing in front of L, T and the second U
    for lx, ly, a in ((604, 742, 100), (810, 752, 78), (1020, 750, 101)):
        tp = wavy((lx + (16 if a > 90 else -16), ly - 70), math.radians(a), 104, 5, .4, rng)
        over.append(ribbon(tp, 4, .6))
    return back, over


def mast(x, y, size):
    """The NSV masthead, three lines, for the seal."""
    lh = size * .96
    return ('<g font-family="Archivo, Arial, sans-serif" font-weight="800" font-size="%s" letter-spacing=".04em" fill="%s">'
            '<text x="%s" y="%s">NEW</text><text x="%s" y="%s">SPORT</text><text x="%s" y="%s">VISION</text></g>'
            '<rect x="%s" y="%s" width="%s" height="%s" fill="#FFFFFF"/>' % (
                f(size), INK, f(x), f(y), f(x), f(y + lh), f(x), f(y + 2 * lh),
                f(x + size * 2.42), f(y - size * .36), f(size * 1.3), f(size * .14)))


def svg(title="", ident="tos", label="THE TREE|OF SPORT"):
    limbs, leaves = crown()
    back, over = roots()

    stops = "".join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in SKY_STOPS)
    sky = ('<g id="%s-sky"><linearGradient id="%s-g" x1="0" y1="0" x2="0" y2="1">%s</linearGradient>'
           '<radialGradient id="%s-glow" cx="800" cy="430" r="620" gradientUnits="userSpaceOnUse" '
           'gradientTransform="translate(800 430) scale(1 .78) translate(-800 -430)">'
           '<stop offset="0" stop-color="%s" stop-opacity=".95"/><stop offset=".55" stop-color="%s" stop-opacity=".35"/>'
           '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
           '<rect width="%d" height="%d" fill="url(#%s-g)"/><rect width="%d" height="%d" fill="url(#%s-glow)"/></g>'
           % (ident, ident, stops, ident, GLOW, GLOW, GLOW, W, H, ident, W, H, ident))

    l1, l2 = label.split("|")
    label_g = ('<g id="%s-label" aria-hidden="true" font-family="Archivo, Arial, sans-serif" font-weight="800" '
               'font-size="31" fill="%s"><text x="41" y="38">%s</text><text x="41" y="68">%s</text></g>' % (ident, INK, l1, l2))
    seal = ('<g id="%s-seal" aria-hidden="true"><rect x="1494" y="16" width="117" height="113" fill="%s"/>%s</g>'
            % (ident, YELLOW, mast(1510, 58, 21)))

    # each layer is one path: about a thousand shapes, a dozen elements
    roots_g = '<g id="%s-roots" class="tos-roots" fill="%s"><path d="%s"/></g>' % (ident, BARK, "".join(back))
    hz = "M%s %s" % (f(HORIZON[0][0]), f(HORIZON[0][1])) + catmull(HORIZON)
    horizon = ('<g id="%s-horizon"><path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/></g>'
               % (ident, hz, HORIZON_C))
    trunk = ('<g id="%s-trunk" class="tos-trunk" fill="%s"><path d="M772 470C776 520 774 560 764 586'
             'C756 597 738 605 716 609L908 609C886 605 868 597 860 586C850 560 848 520 852 470'
             'C852 440 844 410 836 384C828 366 818 356 812 350C806 356 796 366 788 384C780 410 772 440 772 470Z"/></g>' % (ident, BARK))

    rng = random.Random(3)
    tones = {0: [], 1: []}
    for x, y, a, s in leaves:
        if not in_dome(x, y, 1.03):
            continue
        u = (x - DOME[0]) / DOME[2]
        lit = (-.5 * u + (DOME[1] - y) / DOME[3] * .6 + rng.uniform(-.35, .35)) > .32
        tones[1 if lit else 0].append(leaf_d(x, y, a, s))
    limb_paths = '<path d="%s"/>' % "".join(ribbon(p, w0, w1) for p, w0, w1, d in limbs)
    crown_g = ('<g id="%s-crown" class="tos-crown"><g fill="%s">%s</g>'
               '<path class="tos-w0" fill="%s" d="%s"/><path class="tos-w1" fill="%s" d="%s"/></g>' % (
                   ident, LIMB, limb_paths, LEAVES[0], "".join(tones[0]), LEAVES[1], "".join(tones[1])))

    letters = ('<g id="%s-culture-letters" class="tos-culture" aria-label="CULTURE" fill="%s" '
               'font-family="Nunito, Arial Rounded MT Bold, sans-serif" font-weight="%d" font-size="%d" '
               'text-anchor="middle">%s</g>' % (ident, ORANGE, LETTER_WEIGHT, LETTER_SIZE, "".join(
                   '<text class="tos-letter" x="%d" y="%d" style="--i:%d">%s</text>' % (x, y, i, ch)
                   for i, (ch, x, y) in enumerate(zip(LETTERS, LETTER_X, LETTER_Y)))))
    roots_over = '<g id="%s-roots-over" class="tos-roots" fill="%s"><path d="%s"/></g>' % (ident, BARK, "".join(over))

    return ('<svg class="tos" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-labelledby="%s-t">'
            '<title id="%s-t">%s</title>%s%s%s%s%s%s%s%s%s</svg>' % (
                W, H, ident, ident, title, sky, label_g, seal, roots_g, horizon, trunk, crown_g, letters, roots_over))


def stats():
    limbs, leaves = crown()
    return {"limbs": len(limbs), "leaves": sum(1 for x, y, a, s in leaves if in_dome(x, y, 1.03))}


if __name__ == "__main__":
    import sys
    s = svg("The Tree of Sport")
    sys.stdout.write(s)
    sys.stderr.write("%d bytes %s\n" % (len(s.encode()), stats()))
