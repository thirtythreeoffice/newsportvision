# -*- coding: utf-8 -*-
"""
Balanced line-breaking for justified display stacks.

The logo's three lines fill one measure because they happen to be close to the
same natural width. A stack whose lines differ wildly cannot be justified
without one line tracking out into separate letters, so the break points have
to be chosen for width, not for word count.

This picks the partition of a sentence into N lines that minimises the spread
between the widest and narrowest line, measured in ems using Archivo's
uppercase advances rather than character counts — "WWW" and "III" are not the
same width, and a character-count heuristic sets them as if they were.

The words themselves are never changed, reordered, or dropped. Only where the
line turns is decided here.
"""

from itertools import combinations

# Approximate advance widths (em) for Archivo uppercase at display weight.
W = {
    "A": .66, "B": .65, "C": .67, "D": .69, "E": .58, "F": .56, "G": .71,
    "H": .71, "I": .28, "J": .53, "K": .65, "L": .55, "M": .87, "N": .71,
    "O": .74, "P": .63, "Q": .74, "R": .65, "S": .62, "T": .60, "U": .69,
    "V": .64, "W": .95, "X": .63, "Y": .61, "Z": .60,
    "0": .64, "1": .40, "2": .62, "3": .62, "4": .66, "5": .62,
    "6": .64, "7": .58, "8": .64, "9": .64,
    " ": .26, ".": .30, ",": .30, ":": .30, ";": .30, "?": .55, "!": .32,
    "-": .38, "—": .80, "–": .55, "(": .38, ")": .38, "'": .25, "’": .25,
    "&": .72, "/": .45, "È": .58, "É": .58, "À": .66,
}
DEFAULT = .62


def width(text):
    """Natural width of a line, in ems."""
    return sum(W.get(ch, DEFAULT) for ch in text.upper())


def balance(text, n):
    """Split `text` into exactly n lines with the most even widths."""
    words = text.split()
    if n <= 1 or len(words) <= n:
        return [text] if n <= 1 else _pad(words, n)
    best = None
    for cuts in combinations(range(1, len(words)), n - 1):
        idx = (0,) + cuts + (len(words),)
        lines = [" ".join(words[idx[i]:idx[i + 1]]) for i in range(n)]
        w = [width(l) for l in lines]
        spread = max(w) - min(w)
        if best is None or spread < best[0]:
            best = (spread, lines)
    return best[1]


def _pad(words, n):
    lines = [w for w in words]
    while len(lines) < n:
        lines.append("")
    return lines[:n]


def auto(text, target=8.2, max_lines=4):
    """
    Break a sentence into the number of lines that puts each one near `target`
    ems wide — wide enough to read as a display line, short enough that the
    width axis can close the gap without tracking taking over.
    """
    total = width(text)
    if total <= target * 1.35:
        return [text]
    n = max(2, min(max_lines, int(round(total / target))))
    words = text.split()
    n = min(n, len(words))
    if n <= 1:
        return [text]

    # Prefer the line count whose balanced solution is most even, with a slight
    # bias toward fewer lines so a stack never becomes a ladder of fragments.
    best = None
    for k in (n - 1, n, n + 1):
        if k < 2 or k > max_lines or k > len(words):
            continue
        lines = balance(text, k)
        w = [width(l) for l in lines]
        if min(w) <= 0:
            continue
        ratio = min(w) / max(w)
        # A line less than ~58% of the longest cannot be justified without the
        # tracking taking over; "FUTURESPORTFUTURE / 2026" is better as one
        # line than as a word and an orphan.
        if ratio < 0.58:
            continue
        score = (max(w) / min(w)) + (k - 2) * 0.06
        if best is None or score < best[0]:
            best = (score, lines)
    return best[1] if best else [text]
