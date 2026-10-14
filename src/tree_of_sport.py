"""The Tree of Sport, drawn for the web.

A hand-constructed SVG of the tree on page 1 of the manifesto PDF. Nothing in
it is a raster, an embedded image or a trace: every shape is built here from
geometry, placed by rule from a fixed seed, so the build always draws the same
tree. It is drawn in the PDF raster's own coordinate space (1642 x 896) so it
can be laid over the original and compared; proportions were measured from it
(crown ~924 x 440, a 1.7:1 dome; fork at y~455; trunk ~70 wide flaring to
~108; horizon at y 583 under the trunk; roots from x 171 to 1460; the seven
letters' positions and cap height).

The drawing has no background. It stands on the page's own sky (fsf.css).

Groups, in drawing order (each id is prefixed with the ident, "tos-"):
  horizon            the arc through the foot of the trunk, as two halves
                     from the centre outward; it runs far past the drawing
                     so it crosses the whole screen.
  roots-primary      roots leaving the foot, a wide spread under the horizon,
                     and the taproot under the T;
  roots-secondary    the roots they divide into;
  roots-tendrils     the fine tendrils that fall from those.
  trunk              short, thick, flaring into the roots; a darker sliver on
                     its shaded side.
  crown              branches-primary (the leader and six limbs),
                     branches-secondary, twigs, and the leaves in ten groups
                     by distance from the trunk (leaves-0 … leaves-9).
  culture-letters    C U L T U R E as text, on a shallow V among the roots.
  roots-front        three tendrils passing in front of L, T and U.

Leaves are six hand-drawn shapes (<symbol>, each with a midrib), set along
the twigs: more toward the crown's edge, fewer inside so the branches show,
never closer than a leaf's width, at a scale that varies by about a quarter,
turned with the twig they grow from.
"""

import math
import random

W, H = 1642, 896
TX = 812
FORK_Y = 455
HZ_APEX = (812, 583)
HZ_R = 2913                      # the horizon's radius, fitted to the PDF arc
DOME = (801, 456, 468, 432)      # cx, base y, half width, height
# where each part grows from, and how far: the growth is a circle opening from
# that point (in the drawing's coordinates), scaled by the page's CSS
CLIPS = {"hz": (812, 583, 2700), "r1": (812, 604, 640), "r2": (812, 604, 640), "r3": (812, 604, 660),
         "trunk": (812, 612, 240), "b1": (812, 470, 600), "b2": (812, 470, 600), "b3": (812, 470, 620)}

LEAF_LIGHT = "#62AA3E"           # the PDF's two greens, as it renders: yellow-green
LEAF_DEEP = "#46903A"            # and the deeper one
LIMB = "#8C5A3E"                 # rosy brown
TWIG = "#966448"                 # a step lighter, for the finest work
BARK = "#643214"                 # chocolate: trunk and roots
BARK_SHADE = "#552910"
HORIZON_C = "#1E5028"
ORANGE = "#F08C46"

LETTERS = "CULTURE"
LETTER_X = [195, 403, 604, 810, 1020, 1227, 1441]
LETTER_Y = [777, 815, 832, 839, 835, 815, 778]
LETTER_SIZE = 66

# six leaves, base at the origin, pointing along +x; each with its midrib
LEAF_SHAPES = [
    ("M0 0C6-6.5 16-7.5 24 0C16 7 6 6 0 0Z", "M2.5-.35L20 0 2.5.35Z"),           # almond
    ("M0 0C7-5 19-5.5 28 0C19 5 7 4.8 0 0Z", "M3-.3L24 0 3 .3Z"),                 # lanceolate
    ("M0 0C5-8 15-8.5 22 0C15 8 5 7.5 0 0Z", "M2.5-.4L18 0 2.5.4Z"),              # broad
    ("M0 0C6-7 17-8.5 25-1C17 6 7 6.5 0 0Z", "M2.5-.35L21-.8 2.5.35Z"),           # asymmetric
    ("M0 0C8-6 18-5 26-3C18 3 8 5 0 0Z", "M3-.3L22-2.4 3 .3Z"),                   # curved
    ("M0 0C5-6 13-7.5 20-1.2Q22 0 20 1.2C13 7.5 5 6 0 0Z", "M2.5-.35L18 0 2.5.35Z"),  # round-tipped
]


def f(v):
    r = round(v, 1)
    return str(int(r)) if r == int(r) else str(r)


def fi(v):
    return str(int(round(v)))


def horizon_y(x):
    return HZ_APEX[1] + (x - HZ_APEX[0]) ** 2 / (2 * HZ_R)


def in_dome(x, y, k=1.0):
    cx, base, a, b = DOME
    if y > base + 8:
        return False
    return ((x - cx) / (a * k)) ** 2 + ((base - y) / (b * k)) ** 2 <= 1


def catmull(pts, closed=False, prec=None):
    g = prec or f
    n = len(pts)
    d = ""
    for i in (range(n) if closed else range(n - 1)):
        p0 = pts[i - 1] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += "C%s %s %s %s %s %s" % (g(c1[0]), g(c1[1]), g(c2[0]), g(c2[1]), g(p2[0]), g(p2[1]))
    return d


def ribbon(pts, w0, w1):
    """A tapered filled limb along the polyline pts: thick at the base, thin
    at the tip, closed round the end."""
    n = len(pts)
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        t = i / (n - 1)
        w = (w0 + (w1 - w0) * t ** .8) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    outline = left + right[::-1]
    g = fi if w0 > 2.5 else f
    return "M%s %s" % (g(outline[0][0]), g(outline[0][1])) + catmull(outline, closed=True, prec=g) + "Z"


def wavy(start, ang, length, steps, wave, rng, curl=0.0):
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


def reach(x, y, a, inside, limit=900.0):
    lo, hi = 0.0, limit
    for _ in range(30):
        m = (lo + hi) / 2
        if inside(x + math.cos(a) * m, y + math.sin(a) * m):
            lo = m
        else:
            hi = m
    return lo


# --- crown -----------------------------------------------------------------------
def crown():
    """The leader and six limbs leave the upper trunk and divide three times;
    leaves are set along the twigs."""
    rng = random.Random(1642)
    limbs = []                                       # (pts, w0, w1, depth)
    inside = lambda x, y: in_dome(x, y, .97)

    def grow(p, a, length, w, depth):
        length = min(length, reach(p[0], p[1], a, inside) * (.97 if depth >= 2 else .6))
        if length < 14:
            return
        steps = 5 if depth < 2 else 3
        curl = (.06 if math.cos(a) < 0 else -.06) if depth == 0 else 0
        pts = wavy(p, a, length, steps, .26, rng, curl=curl)
        w1 = max(w * .52, .9)
        limbs.append((pts, w, w1, depth))
        if depth >= 3:
            return
        heading = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        forks = ((.45, -.55), (.72, .5), (1.0, 0)) if depth < 2 else ((.45, -.55), (.75, .5), (1.0, .1))
        for t, da in forks:
            i = min(int(round(t * steps)), steps)
            na = heading + (da if da else rng.uniform(-.18, .18)) * rng.uniform(.85, 1.15)
            grow(pts[i], na, length * rng.uniform(.56, .7), w1 * .88, depth + 1)

    leader = wavy((TX, 446), math.radians(-90), 230, 5, .12, rng)
    limbs.append((leader, 30, 11, 0))
    for t, side in ((.55, -1), (.8, 1), (1.0, -1), (1.0, 1)):
        i = min(int(round(t * 5)), 5)
        a = math.radians(-90 + side * (38 if t < 1 else 16))
        grow(leader[i], a, 260, 10, 1)
    # limbs leave from the trunk's edge, where it narrows toward the leader
    for a, y, w in ((-158, 462, 24), (-130, 440, 24), (-106, 414, 19), (-74, 414, 19), (-50, 440, 24), (-22, 462, 24)):
        ang = math.radians(a + rng.uniform(-2, 2))
        half = (22 + (y - 430) * .4) * .45
        start = (TX + (-half if a < -90 else half), y)
        grow(start, ang, 900, w, 0)

    # leaves along the twigs
    leaves = []
    taken = {}
    cx, base, A, B = DOME
    for pts, w0, w1, depth in limbs:
        if depth < 1:
            continue
        seglen = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
        start_t = .55 if depth == 1 else .15
        n = int(seglen * (1 - start_t) / 5)
        for k in range(n + 1):
            t = start_t + (1 - start_t) * k / max(n, 1)
            pos = t * (len(pts) - 1)
            i = min(int(pos), len(pts) - 2)
            u = pos - i
            x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * u
            y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * u
            if not in_dome(x, y, 1.03):
                continue
            nu, nv = (x - cx) / A, (base - y) / B
            r = math.hypot(nu, nv)
            keep = .5 + .5 * min(r, 1) ** 1.2                      # thicker toward the edge
            if nv < .36 and abs(nu) < .36 - nv * .5:              # the open middle
                keep *= .2
            if rng.random() > keep:
                continue
            cell = (int(x // 11), int(y // 11))
            if any((cell[0] + dx, cell[1] + dy) in taken for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                continue
            taken[cell] = 1
            heading = math.degrees(math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]))
            side = 1 if k % 2 else -1
            ang = heading + side * rng.uniform(30, 58)
            s = 1.3 * max(.75, min(1.25, rng.gauss(1, .12)))
            lit = (-.55 * nu + .65 * nv + rng.uniform(-.45, .45)) > .45
            d = math.hypot(x - TX, y - FORK_Y)
            leaves.append((x, y, ang, s, rng.randrange(len(LEAF_SHAPES)), lit, d))
        if depth == 3:                                             # a leaf at every tip
            e, p = pts[-1], pts[-2]
            if in_dome(e[0], e[1], 1.04):
                heading = math.degrees(math.atan2(e[1] - p[1], e[0] - p[0]))
                nu, nv = (e[0] - cx) / A, (base - e[1]) / B
                leaves.append((e[0], e[1], heading + rng.uniform(-10, 10), 1.35, rng.randrange(len(LEAF_SHAPES)),
                               (-.55 * nu + .65 * nv) > .2, math.hypot(e[0] - TX, e[1] - FORK_Y)))
    return limbs, leaves


# --- roots -------------------------------------------------------------------------
def in_roots(x, y):
    if y < horizon_y(x) + 6:
        return False
    return ((x - TX) / 460) ** 2 + ((y - 596) / 285) ** 2 <= 1


def roots():
    """A wide spread just under the horizon, then tapering tendrils downward,
    a taproot under the T."""
    rng = random.Random(896)
    out = []                                         # (path, depth)

    def grow(p, a, length, w, depth, sink):
        length = min(length, reach(p[0], p[1], a, in_roots) * rng.uniform(.6, .98))
        if length < 14:
            return
        steps = 5 if depth < 2 else 3
        bend = sink if depth else (.09 if math.cos(a) < -.8 else (-.09 if math.cos(a) > .8 else sink))
        pts = wavy(p, a, length, steps, .5, rng, curl=bend)
        pts = [(x, max(y, horizon_y(x) + 8)) for x, y in pts]
        w1 = max(w * .45, .8)
        out.append((ribbon(pts, w, w1), depth))
        if depth >= 3:
            return
        heading = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
        for t in (.35, .65, 1.0):
            if depth >= 2 and t < .6:
                continue
            i = min(int(round(t * steps)), steps)
            na = heading + (math.radians(90) - heading) * (.45 if t < 1 else .12) + rng.uniform(-.25, .25)
            grow(pts[i], na, length * rng.uniform(.5, .7), w1 * (.9 if t == 1 else .65), depth + 1, sink)

    foot = (TX, 604)
    for a, w in ((176, 18), (168, 18), (152, 16), (128, 13), (104, 12),
                 (76, 12), (52, 13), (28, 16), (12, 18), (4, 18)):
        grow(foot, math.radians(a + rng.uniform(-3, 3)), 600, w, 0, (1 if a > 90 else -1) * .03)
    # the taproot, under the T
    tap = wavy((TX - 4, 606), math.radians(91), 236, 7, .3, rng)
    out.append((ribbon(tap, 22, 1.2), 0))
    for t in (.4, .7):
        i = int(t * 7)
        grow(tap[i], math.radians(90 + (-34 if t < .5 else 30)), 110, 6, 2, 0)

    front = []
    for lx, ly, a in ((604, 742, 100), (810, 752, 78), (1020, 750, 101)):
        tp = wavy((lx + (16 if a > 90 else -16), ly - 70), math.radians(a), 104, 5, .4, rng)
        front.append(ribbon(tp, 4, .6))
    return out, front


# --- the drawing ---------------------------------------------------------------------
def svg(title="", ident="tos"):
    limbs, leaves = crown()
    rts, front = roots()

    limb_grad = ('<radialGradient id="%s-limb" gradientUnits="userSpaceOnUse" cx="812" cy="470" r="190">'
                 '<stop offset=".3" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (ident, BARK, LIMB))
    clips = "".join(
        '<clipPath id="%s-c-%s" clipPathUnits="userSpaceOnUse"><circle class="tos-clip tos-clip-%s" '
        'cx="%d" cy="%d" r="%d"/></clipPath>' % (ident, k, k, x, y, r)
        for k, (x, y, r) in CLIPS.items())
    symbols = clips + limb_grad + "".join(
        '<symbol id="%s-leaf%d" overflow="visible"><g class="tos-lf"><path d="%s"/>'
        '<path fill="#FFFFFF" fill-opacity=".22" d="%s"/></g></symbol>' % (ident, i, a, b)
        for i, (a, b) in enumerate(LEAF_SHAPES))

    # the horizon: two halves drawn from the centre outward
    def half(sign):
        xs = [HZ_APEX[0] + sign * k for k in range(0, 2600, 130)]
        pts = [(x, horizon_y(x)) for x in xs]
        return "M%s %s" % (f(pts[0][0]), f(pts[0][1])) + catmull(pts)
    horizon = ('<g id="%s-horizon" class="tos-horizon" clip-path="url(#%s-c-hz)" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round">'
               '<path vector-effect="non-scaling-stroke" d="%s"/><path vector-effect="non-scaling-stroke" d="%s"/></g>'
               % (ident, ident, HORIZON_C, half(-1), half(1)))

    def group(name, fill, paths, clip=None):
        cp = (' clip-path="url(#%s-c-%s)"' % (ident, clip)) if clip else ""
        return '<g id="%s-%s" class="tos-%s"%s fill="%s"><path d="%s"/></g>' % (ident, name, name, cp, fill, "".join(paths))

    roots_svg = (group("roots-primary", BARK, [p for p, d in rts if d == 0], "r1") +
                 group("roots-secondary", BARK, [p for p, d in rts if d == 1], "r2") +
                 group("roots-tendrils", BARK, [p for p, d in rts if d >= 2], "r3"))

    trunk = ('<g id="%s-trunk" class="tos-trunk" clip-path="url(#%s-c-trunk)"><path fill="%s" d="M772 470C776 520 774 560 764 586'
             'C756 597 738 605 716 609L908 609C886 605 868 597 860 586C850 560 848 520 852 470'
             'C850 456 840 440 830 432C824 428 818 427 812 427C806 427 800 428 794 432C784 440 774 456 772 470Z"/>'
             '<path fill="%s" d="M836 404C844 430 848 456 846 486C844 530 846 566 856 588C866 598 884 605 904 609'
             'L870 609C856 598 846 584 840 560C834 520 838 470 836 404Z"/></g>' % (ident, ident, BARK, BARK_SHADE))

    # the top of the trunk is drawn again over the primary limbs' bases, so
    # they grow out of it without a seam; it moves with the crown
    # the primary limbs darken toward the trunk, so they leave it as bark and
    # turn rosy as they go: no seam where they meet it
    branches = (group("branches-primary", "url(#%s-limb)" % ident, [ribbon(p, a, b) for p, a, b, d in limbs if d == 0], "b1") +
                group("branches-secondary", LIMB, [ribbon(p, a, b) for p, a, b, d in limbs if d == 1], "b2") +
                group("twigs", TWIG, [ribbon(p, a, b) for p, a, b, d in limbs if d >= 2], "b3"))

    # ten groups of equal size, by distance from the trunk: they open in turn,
    # from the heart of the crown outward
    order = sorted(leaves, key=lambda l: l[6])
    bins = {i: [] for i in range(10)}
    for k, (x, y, a, s, shape, lit, d) in enumerate(order):
        bins[min(9, k * 10 // len(order))].append(
            '<use href="#%s-leaf%d" fill="%s" transform="translate(%s %s) rotate(%d)%s"/>' % (
                ident, shape, LEAF_LIGHT if lit else LEAF_DEEP, f(x), f(y), round(a),
                (" scale(%s)" % f(s)) if abs(s - 1) > .04 else ""))
    leaf_groups = "".join('<g id="%s-leaves-%d" class="tos-leaves tos-leaves-%d" style="--n:%d">%s</g>' % (
        ident, i, i, i, "".join(bins[i])) for i in range(10))

    crown_g = '<g id="%s-crown" class="tos-crown">%s%s</g>' % (ident, branches, leaf_groups)

    letters = ('<g id="%s-culture-letters" class="tos-culture" aria-label="CULTURE" fill="%s" '
               'font-family="Nunito, Arial Rounded MT Bold, sans-serif" font-weight="800" font-size="%d" '
               'text-anchor="middle">%s</g>' % (ident, ORANGE, LETTER_SIZE, "".join(
                   '<text class="tos-letter" x="%d" y="%d" style="--i:%d">%s</text>' % (x, y, i, ch)
                   for i, (ch, x, y) in enumerate(zip(LETTERS, LETTER_X, LETTER_Y)))))
    front_g = group("roots-front", BARK, front, "r3")

    return ('<svg class="tos" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" overflow="visible" '
            'role="img" aria-labelledby="%s-t"><title id="%s-t">%s</title><defs>%s</defs>%s%s%s%s%s%s</svg>' % (
                W, H, ident, ident, title, symbols, horizon, roots_svg, trunk, crown_g, letters, front_g))


def stats():
    limbs, leaves = crown()
    rts, front = roots()
    return {"limbs": len(limbs), "leaves": len(leaves), "roots": len(rts) + len(front)}


if __name__ == "__main__":
    import sys
    s = svg("The Tree of Sport")
    sys.stdout.write(s)
    sys.stderr.write("%d bytes %s\n" % (len(s.encode()), stats()))
