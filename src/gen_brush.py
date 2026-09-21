# -*- coding: utf-8 -*-
"""
Generate the painted marks.

A white line on a court is painted. So is a brushstroke. It is the same mark,
made by the same gesture, and it is where sport and art actually touch — the
axis NewSportVision says it exists to create. The logo's bar is the site's core
object; these are that bar made by hand instead of by rule.

A brush is not an outline with wavy edges — it is a bundle of bristles, each
laying its own track. So each mark here is built as a union of bristle bands:
they overlap into a solid core, thin out at the edges, run dry at different
points, and fray apart at the tail. That is what gives real dry-brush streaks
rather than a faceted lozenge.

Deterministic: same seed, same strokes, every build.
"""
import math, os, random

OUT = os.path.join(os.path.dirname(__file__), "..", "static", "img")
os.makedirs(OUT, exist_ok=True)


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def noise_fn(rnd, amp, octaves=4, base=1.3):
    """A small deterministic 1-D noise, as a sum of sines."""
    terms = []
    for o in range(octaves):
        terms.append((amp / (1.9 ** o), base * (2.1 ** o) * rnd.uniform(0.7, 1.4),
                      rnd.uniform(0, math.tau)))
    def f(t):
        return sum(a * math.sin(t * math.tau * f_ + p) for a, f_, p in terms)
    return f


def band(rnd, w, cy, thick, x0, x1, wob, steps=16):
    """One bristle track: a thin wavy quad from x0 to x1."""
    n_top = noise_fn(rnd, thick * wob, 3)
    n_bot = noise_fn(rnd, thick * wob, 3)
    drift = noise_fn(rnd, thick * 0.9, 2)
    top, bot = [], []
    for i in range(steps + 1):
        t = i / steps
        x = x0 + (x1 - x0) * t
        # the track thins at both of its own ends
        k = smooth(t / 0.10) * smooth((1 - t) / 0.16)
        k = 0.25 + 0.75 * k
        c = cy + drift(t * 0.7)
        half = thick * 0.5 * k
        top.append((round(x), round(c - half + n_top(t * 2.1))))
        bot.append((round(x), round(c + half + n_bot(t * 2.3))))
    d = "M%d %d" % top[0]
    d += "".join("L%d %d" % p for p in top[1:])
    d += "".join("L%d %d" % p for p in reversed(bot))
    return d + "Z"


def stroke(seed, w=1200, h=80, bristles=34, dryness=0.55, fray=0.30,
           load=0.06, core=0.62):
    """
    A brush bar.
      dryness  how often a bristle lifts off the surface mid-stroke
      fray     how far the tail splits into separate tracks
      load     how blunt the loaded (leading) end is
      core     share of the height that stays solid
    """
    rnd = random.Random(seed)
    parts = []
    cyc = h / 2.0

    for i in range(bristles):
        u = (i + 0.5) / bristles            # 0..1 across the height
        off = (u - 0.5) * h                  # distance from the centreline
        edge = abs(u - 0.5) * 2              # 0 at centre, 1 at the outside

        # bands away from the centre are thinner, shorter and start later
        thick = (h / bristles) * (2.4 - 1.35 * edge) * rnd.uniform(0.85, 1.2)
        x0 = w * (rnd.uniform(0.0, load) + edge * rnd.uniform(0.0, 0.05))
        x1 = w * (1.0 - fray * (edge ** 1.6) * rnd.uniform(0.25, 1.0)
                  - rnd.uniform(0.0, 0.04))
        cy = cyc + off * rnd.uniform(0.93, 1.07)

        # where this bristle runs dry
        cuts = []
        n_cuts = rnd.choices([0, 1, 2, 3], weights=[42, 30, 18, 10])[0]
        if edge > core:
            n_cuts += 1
        for _ in range(n_cuts):
            c = rnd.uniform(0.18, 0.99)
            wd = rnd.uniform(0.015, 0.075) * (0.6 + dryness)
            cuts.append((c - wd, c + wd))
        cuts.sort()

        # walk the track, skipping the dry stretches
        segs, cur = [], 0.0
        for a, b in cuts:
            a = max(cur, a)
            if a - cur > 0.035:
                segs.append((cur, a))
            cur = max(cur, b)
        if 1.0 - cur > 0.035:
            segs.append((cur, 1.0))

        for a, b in segs:
            sx0 = x0 + (x1 - x0) * a
            sx1 = x0 + (x1 - x0) * b
            if sx1 - sx0 < w * 0.012:
                continue
            parts.append(band(rnd, w, cy, thick, sx0, sx1, wob=0.30))

    # flecks thrown off the tail
    for _ in range(rnd.randint(4, 8)):
        fx = w * rnd.uniform(0.9, 1.01)
        fy = cyc + rnd.uniform(-h * 0.46, h * 0.46)
        fw = w * rnd.uniform(0.004, 0.022)
        fh = rnd.uniform(1.0, h * 0.06)
        parts.append("M%.1f,%.1f h%.1f v%.1f h%.1f Z" % (fx, fy, fw, fh, -fw))

    return "".join(parts)


def torn_edge(seed, w=1600, h=160, dryness=0.5):
    """
    A field edge: solid above, painted and broken below. Used where a colour
    field ends against paper instead of being cut with a straight rule.
    """
    rnd = random.Random(seed)
    n = 320
    line = noise_fn(rnd, h * 0.17, 5)
    fine = noise_fn(rnd, h * 0.05, 7)
    pts = []
    for i in range(n + 1):
        t = i / n
        x = t * w
        y = h * 0.58 + line(t * 1.4) + fine(t * 5.0)
        pts.append((x, y))
    d = "M0 0 L%d 0" % w
    d += "".join("L%d %d" % (round(x), round(y)) for x, y in reversed(pts))
    d += "Z"

    # Bristle tails below the edge. Paint pulls to a point as it runs out, so
    # each one narrows down its length instead of ending square.
    parts = [d]
    for _ in range(rnd.randint(30, 46)):
        t = rnd.random()
        x = t * w
        base = h * 0.58 + line(t * 1.4) + fine(t * 5.0) - 2
        bw = w * rnd.uniform(0.003, 0.026)
        bh = h * rnd.uniform(0.05, 0.38) * (0.5 + dryness)
        lean = rnd.uniform(-0.25, 0.25) * bw
        tipw = bw * rnd.uniform(0.0, 0.22)
        mid = bh * rnd.uniform(0.35, 0.7)
        parts.append(
            "M%d %d L%d %d L%d %d L%d %d L%d %d Z" % (
                round(x), round(base),
                round(x + bw), round(base),
                round(x + bw * 0.78 + lean * 0.5), round(base + mid),
                round(x + bw * 0.5 + lean + tipw), round(base + bh),
                round(x + bw * 0.5 + lean), round(base + bh)))
    # a little spatter, well separated from the edge
    for _ in range(rnd.randint(7, 13)):
        x = rnd.random() * w
        y = h * rnd.uniform(0.82, 0.99)
        r = rnd.uniform(1.2, 3.4)
        parts.append("M%d %d l%d %d l%d %d Z" % (
            round(x), round(y), round(r * 2), round(r), round(-r * 2), round(r * 0.8)))
    return "".join(parts)


def write(name, d, w, h):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
           'preserveAspectRatio="none"><path d="%s" fill="#000"/></svg>' % (w, h, d))
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return len(svg)


if __name__ == "__main__":
    total = 0
    specs = [
        ("brush-1.svg", stroke(11, bristles=26, dryness=0.45, fray=0.26)),
        ("brush-2.svg", stroke(27, bristles=24, dryness=0.75, fray=0.38)),
        ("brush-3.svg", stroke(43, bristles=28, dryness=0.35, fray=0.20)),
    ]
    for name, d in specs:
        n = write(name, d, 1200, 80)
        total += n
        print("%-14s %6d bytes" % (name, n))
    # Short marks. A 1200-wide stroke squashed into a 45px tab loses all its
    # bristle texture horizontally, so the small marks are drawn short.
    for name, seed, br, dry in (("tab-1.svg", 5, 13, 0.55), ("tab-2.svg", 19, 11, 0.40),
                                ("tab-3.svg", 37, 15, 0.70)):
        n = write(name, stroke(seed, w=240, h=80, bristles=br, dryness=dry,
                               fray=0.34, load=0.10), 240, 80)
        total += n
        print("%-14s %6d bytes" % (name, n))
    for name, seed, dry in (("edge-1.svg", 71, 0.45), ("edge-2.svg", 93, 0.70)):
        n = write(name, torn_edge(seed, dryness=dry), 1600, 160)
        total += n
        print("%-14s %6d bytes" % (name, n))
    print("total %.1f kB" % (total / 1024))
