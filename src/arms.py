# -*- coding: utf-8 -*-
"""
A.R.M.S. — asocijacija roditelja maloletnih sportista.

A microsite inside newsportvision.com. It keeps the host's build, its asset
pipeline, its reveal engine and its page furniture, and almost nothing else:
ARMS has its own ground, its own type, its own grid and its own geometry,
because it is its own institution.

Everything visual here traces to two supplied files — the official mark and
the site architecture — and nothing in it is invented:

    mark          1440 x 1187.72, two columns of 702.99 with a 34.02 gutter,
                  top blocks 827.72 tall, bottom blocks 325.98 (0.3938 of the
                  top), a white bracket 15.59 thick running from the centre of
                  the left block to the centre of the right one and dropping a
                  leg at each end. Measured out of the artwork, not estimated.
    colour        magenta #9F194F, blue #5C9ED6, green #077734, read off the
                  fill operators in the PDFs rather than sampled from pixels.
    proportion    the page's gutter is the mark's gutter: 34.02/1440 of the
                  measure, which is where --a-gut comes from.
    words         every line of Serbian below is transcribed from the supplied
                  material. Where the material says nothing — partners, fees,
                  departments, addresses — this file says nothing either, and
                  the section carries an honest "u pripremi" instead of copy
                  someone would have to retract later.
"""

from render import ASSET_V, INLINE_BOOT, BASE, esc                      # noqa: E402

# ---------------------------------------------------------------------------
# The mark
# ---------------------------------------------------------------------------

# Block copy, exactly as the logo sets it. Bold words are bold in the artwork.
MARK = (
    ("magenta", "tall",  (("asocijacija", 0), ("roditelja", 1),
                          ("maloletnih", 0), ("sportista", 1))),
    ("blue",    "tall",  (("udruženje građana", 0), ("beograd", 1),
                          ("srbija", 0), ("2025", 1))),
    ("blue",    "short", (("što udruženiji", 1), ("to bolji i jači", 0))),
    ("magenta", "short", (("newsportvision", 1), ("koncept", 0))),
)

# The bracket, as a single stroked centreline in the mark's own coordinates.
# The artwork drops its right leg 1.41 units lower than its left — a drafting
# slip at 1/1000 of the width. The path below is symmetrical, which is what the
# drawing means; nothing else about it is changed.
BRACKET = "M359.3 873.8V682.4h721.4v191.4"
BRACKET_LEN = 1104.1

# ---------------------------------------------------------------------------
# Words
# ---------------------------------------------------------------------------

MANIFESTO = (
    "ne postoji dobar roditelj koji nije solidaran sa drugim solidarnim "
    "roditeljima.",

    "solidarnost jača neverovatnom snagom sve solidarne.",

    "ako ne zastupaš sebe sigurno će te zastupati neko drugi, po pravilu "
    "mnogo gori od tebe.... tako bude u društvenom životu.",

    "udruži se sa sebi sličnima......po ciljevima, interesima, osećaju i "
    "naročito KULTURI\u00a0, neudružen si prirodno ‘laka meta’ a često i ‘plen’.",

    "daj svoj roditeljski maksimum dok je dete maloletno, pripremi ga i nauči "
    "da posle brine o sebi i drugima što bolje - samostalno, na bazi "
    "prvenstveno lične odgovornosti.",

    "zdrav sport je za nas aktivnost, sredina, sredstvo i put kojim deca "
    "najbolje mogu da nauče i spreme se za ono šta ih čeka u životu.",
)

CLOSING = "sport bez kulture nema budućnost"

# The five categories of the supplied architecture, in its order. The second
# one is two ideas held together, and is set that way rather than flattened.
SECTIONS = (
    ("ciljevi",    "ciljevi",    None,             "magenta"),
    ("aktivnosti", "aktivnosti", "šta ne radimo",  "blue"),
    ("clanstvo",   "članstvo",   None,             "magenta"),
    ("odeljenja",  "odeljenja",  "po sportovima",  "blue"),
    ("kontakti",   "kontakti",   None,             "magenta"),
)

# The second layer: resources and participation. Green, as in the architecture.
RESOURCES = (
    ("help-desk",  "help desk",
     "pitanje roditelja, odgovor na jednom mestu"),
    ("predlozi",   "predlozi roditelja",
     "šta roditelji predlažu jedni drugima"),
    ("istorija",   "istorija (about)",
     "odakle asocijacija dolazi"),
    ("partneri",   "partneri",
     "sa kim se radi"),
)

PUBLICATION = {
    "title": ("30 PREDLOGA", "ZA RODITELJA", "MALOLETNOG", "SPORTISTE"),
    "parts": ("šta znati (10)", "šta raditi (10)", "šta ne raditi (10)"),
    "format": "PDF",
}

INTRO = "asocijacija roditelja maloletnih sportista"


# ---------------------------------------------------------------------------
# Small pieces
# ---------------------------------------------------------------------------

def asterisk(i=0):
    """The divider the architecture uses between statements."""
    return ('<span class="a-ast" aria-hidden="true" data-reveal="fade" '
            'data-delay="%d">*</span>' % (i * 40))


def prep(what):
    """What a section says while its content is still being written.

    An empty room with a sign is honest. Invented copy about an association
    that has to stand behind every word it publishes is not.
    """
    return ('<p class="a-prep"><span class="a-prep__dot" aria-hidden="true"></span>'
            '%s</p>' % esc(what))


def mark(size="lg", decorative=False):
    """The official mark, rebuilt at its measured proportions.

    Text, colour, ratio and bracket are the artwork's own. It is built in the
    page rather than placed as an image so that it can hold real text, keep its
    edges crisp at any size, and recompose on a narrow screen instead of
    shrinking until its words disappear.
    """
    blocks = []
    for i, (colour, height, lines) in enumerate(MARK):
        rows = ""
        for t, bold in lines:
            # the mark carries a © after the concept's name; it is part of the
            # artwork, set small and light against the bold word it follows.
            body = esc(t) + ('<sup class="a-blk__c">©</sup>'
                             if t == "newsportvision" else "")
            rows += ('<span class="a-blk__l%s">%s</span>'
                     % (" is-b" if bold else "", body))
        blocks.append(
            '<div class="a-blk a-blk--%s a-blk--%s" style="--i:%d">%s</div>'
            % (colour, height, i, rows))

    svg = (
        '<svg class="a-mark__brace" viewBox="0 0 1440 1187.72" aria-hidden="true" '
        'preserveAspectRatio="none" focusable="false">'
        '<path d="%s" fill="none" stroke="#fff" stroke-width="15.59" '
        'stroke-linecap="butt" pathLength="%s"/></svg>' % (BRACKET, BRACKET_LEN))

    label = ("A.R.M.S. — asocijacija roditelja maloletnih sportista, "
             "udruženje građana, Beograd, Srbija, 2025. NewSportVision koncept.")
    return ('<div class="a-mark a-mark--%s"%s%s>%s%s</div>'
            % (size,
               ' aria-hidden="true"' if decorative else
               ' role="img" aria-label="%s"' % esc(label),
               "",
               "".join(blocks), svg))


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def hero():
    return """
<section class="a-hero" aria-labelledby="a-h1">
  <div class="a-wrap a-hero__in">
    <p class="a-kicker" data-reveal="fade">newsportvision koncept
      <span class="a-kicker__sep" aria-hidden="true"></span>beograd / srbija / 2025</p>
    <div class="a-hero__mark" data-a-draw>%(mark)s</div>
    <div class="a-hero__say">
      <h1 class="a-wordmark" id="a-h1"><span class="a-sr">A.R.M.S.</span>%(letters)s</h1>
      <p class="a-tag">° tok pozitivne energije °</p>
      <p class="a-hero__full">%(intro)s</p>
    </div>
  </div>
</section>""" % {
        "mark": mark("lg"),
        "letters": "".join(
            '<span aria-hidden="true" style="--n:%d">%s</span>' % (i, c)
            for i, c in enumerate("A.R.M.S.")),
        "intro": esc(INTRO),
    }


def manifesto():
    out = ['<section class="a-manifesto" aria-labelledby="a-man">',
           '  <h2 class="a-sr" id="a-man">Zašto asocijacija</h2>',
           '  <div class="a-wrap">']
    for i, line in enumerate(MANIFESTO):
        side = "l" if i % 2 == 0 else "r"
        out.append(
            '    <div class="a-say a-say--%s" data-reveal="up" data-delay="%d">'
            '<p class="a-say__t">%s</p></div>' % (side, (i % 2) * 60, esc(line)))
        if i < len(MANIFESTO) - 1:
            out.append('    <div class="a-say__div">%s</div>' % asterisk(i))
    out.append("  </div>")
    out.append("</section>")
    return "\n".join(out)


def index():
    """The five categories. The architecture draws them as blocks; here they
    keep that shape and become the way into the page."""
    items = []
    for i, (slug, a, b, colour) in enumerate(SECTIONS):
        second = '<span class="a-idx__b">%s</span>' % esc(b) if b else ""
        plus = '<span class="a-idx__p" aria-hidden="true">+</span>' if b else ""
        items.append(
            '<li><a class="a-idx a-idx--%s" href="#%s" data-reveal="up" data-delay="%d">'
            '<span class="a-idx__n" aria-hidden="true">%02d</span>'
            '<span class="a-idx__t"><span class="a-idx__a">%s</span>%s%s</span>'
            '<span class="a-idx__go" aria-hidden="true"></span></a></li>'
            % (colour, slug, i * 55, i + 1, esc(a), plus, second))
    return ('<nav class="a-index" aria-label="Sadržaj">\n'
            '  <div class="a-wrap"><ol class="a-index__list">%s</ol></div>\n'
            '</nav>' % "".join(items))


def section(slug, a, b, colour, body, n=None):
    head = esc(a) + (' <span class="a-h__b">%s</span>' % esc(b) if b else "")
    num = ('<span class="a-sec__n" aria-hidden="true">%02d</span>' % n) if n else ""
    return """
<section class="a-sec a-sec--%(c)s" id="%(slug)s" aria-labelledby="h-%(slug)s" data-a-sec>
  <div class="a-wrap">
    <div class="a-sec__head">
      <span class="a-sec__rule" aria-hidden="true"></span>
      <h2 class="a-h" id="h-%(slug)s" data-reveal="up">%(num)s%(head)s</h2>
    </div>
    <div class="a-sec__body">%(body)s</div>
  </div>
</section>""" % {"c": colour, "slug": slug, "head": head, "body": body, "num": num}


def ciljevi():
    # The thesis here is the line the mark itself carries, not one of the six
    # statements: those belong to the manifesto, and a sentence that appears
    # twice on one page is a sentence nobody reads twice.
    return section(
        "ciljevi", "ciljevi", None, "magenta",
        '<div class="a-cols">'
        '  <div class="a-col a-col--wide" data-reveal="up">'
        '    <p class="a-lead">što udruženiji — to bolji i jači.</p>'
        '  </div>'
        '  <div class="a-col a-col--side" data-reveal="up" data-delay="80">'
        + prep("Ciljevi se upisuju iz osnivačkog akta.") +
        '  </div>'
        '</div>', n=1)


def aktivnosti():
    body = (
        '<div class="a-two">'
        '  <div class="a-two__a" data-reveal="up">'
        '    <h3 class="a-h3">aktivnosti</h3>'
        + prep("Spisak aktivnosti se priprema.") +
        '  </div>'
        '  <span class="a-two__link" aria-hidden="true"></span>'
        '  <div class="a-two__b" data-reveal="up" data-delay="90">'
        '    <h3 class="a-h3 a-h3--neg">šta ne radimo</h3>'
        + prep("Granice rada se upisuju uz aktivnosti.") +
        '  </div>'
        '</div>')
    return section("aktivnosti", "aktivnosti", "šta ne radimo", "blue", body, n=2)


def clanstvo():
    rows = (("ko može da se učlani", None),
            ("kako se učlanjuje", None),
            ("šta članstvo znači", None))
    items = "".join(
        '<li class="a-q" data-reveal="up" data-delay="%d">'
        '<span class="a-q__n" aria-hidden="true">%02d</span>'
        '<span class="a-q__t">%s</span></li>' % (i * 60, i + 1, esc(q))
        for i, (q, _) in enumerate(rows))
    body = ('<ol class="a-qs">%s</ol>%s' % (items,
            prep("Uslovi članstva se objavljuju kada ih usvoji skupština.")))
    return section("clanstvo", "članstvo", None, "magenta", body, n=3)


def odeljenja():
    """Built as a directory so it holds three sports or thirty without being
    redrawn: the type carries the system, not a grid of icons."""
    body = ('<div class="a-dir" data-reveal="up">'
            '<p class="a-dir__note">Odeljenja se otvaraju po sportu, kako se '
            'roditelji udružuju.</p>'
            + prep("Spisak odeljenja se otvara sa prvim upisanim sportom.") +
            '</div>')
    return section("odeljenja", "odeljenja", "po sportovima", "blue", body, n=4)


def kontakti():
    body = ('<div class="a-cols">'
            '  <div class="a-col a-col--wide" data-reveal="up">'
            '    <p class="a-lead">udruženje građana, beograd, srbija.</p>'
            '  </div>'
            '  <div class="a-col a-col--side" data-reveal="up" data-delay="80">'
            + prep("Adresa i kontakt se objavljuju po registraciji.") +
            '  </div>'
            '</div>')
    return section("kontakti", "kontakti", None, "magenta", body, n=5)


def publication():
    p = PUBLICATION
    # each line is its own block, so they need a space between them or a
    # screen reader runs them into one word
    title = " ".join('<span>%s</span>' % esc(t) for t in p["title"])
    parts = "".join('<li>%s</li>' % esc(t) for t in p["parts"])
    return """
<section class="a-pub" aria-labelledby="a-pub-h">
  <div class="a-wrap a-pub__in">
    <div class="a-pub__obj" data-reveal="up">
      <div class="a-pub__cover">
        <h2 class="a-pub__t" id="a-pub-h">%(title)s</h2>
        <span class="a-ast a-ast--pub" aria-hidden="true">*</span>
        <ul class="a-pub__parts">%(parts)s</ul>
        <span class="a-ast a-ast--pub" aria-hidden="true">*</span>
        <p class="a-pub__fmt">%(fmt)s</p>
      </div>
      <span class="a-pub__edge" aria-hidden="true"></span>
    </div>
    <div class="a-pub__say" data-reveal="up" data-delay="90">
      <p class="a-lead">Trideset predloga, u tri desetine: šta znati, šta raditi,
        šta ne raditi dok je dete maloletno.</p>
      %(state)s
    </div>
  </div>
</section>""" % {
        "title": title,
        "parts": parts,
        "fmt": esc(p["format"]),
        "state": prep("Publikacija se priprema za preuzimanje."),
    }


def resources():
    items = []
    for i, (slug, name, note) in enumerate(RESOURCES):
        items.append(
            '<li class="a-res" data-reveal="up" data-delay="%d">'
            '<span class="a-res__mark" aria-hidden="true"></span>'
            '<h3 class="a-res__t">%s</h3>'
            '<p class="a-res__n">%s</p></li>' % (i * 55, esc(name), esc(note)))
    return ('<section class="a-resources" aria-labelledby="a-res-h">'
            '<div class="a-wrap">'
            '<div class="a-sec__head"><span class="a-sec__rule a-sec__rule--g" aria-hidden="true"></span>'
            '<h2 class="a-h a-h--g" id="a-res-h" data-reveal="up">resursi</h2></div>'
            '<ul class="a-res__list">%s</ul>'
            '%s</div></section>' % ("".join(items),
                                    prep("Svaki od ova četiri modula se otvara "
                                         "kada njegov sadržaj bude spreman.")))


def closing():
    words = CLOSING.split()
    spans = "".join('<span data-reveal="up" data-delay="%d">%s</span> '
                    % (i * 70, esc(w)) for i, w in enumerate(words))
    return ('<section class="a-closing" aria-label="%s">'
            '<div class="a-wrap"><p class="a-closing__t">%s</p></div>'
            '</section>' % (esc(CLOSING), spans))


# ---------------------------------------------------------------------------
# The frame: where the host ends and the microsite begins
# ---------------------------------------------------------------------------

def threshold(back):
    """A strip in the host's own typeface, on the host's own paper, above the
    microsite's white. Crossing it is the whole point: one line says who owns
    this room, and gives the way out of it."""
    return """
<div class="a-threshold">
  <div class="a-wrap a-threshold__in">
    <a class="a-back" href="%s">
      <span class="a-back__arrow" aria-hidden="true"></span>
      <span class="a-back__t">newsportvision</span>
    </a>
    <span class="a-threshold__slash" aria-hidden="true">/</span>
    <span class="a-threshold__here">arms</span>
  </div>
</div>""" % esc(back)


def arms_footer(back):
    return """
<footer class="a-foot">
  <div class="a-wrap a-foot__in">
    <div class="a-foot__mark">%(mark)s</div>
    <div class="a-foot__say">
      <p class="a-foot__name">A.R.M.S.</p>
      <p class="a-foot__sub">asocijacija roditelja maloletnih sportista<br>
        udruženje građana · beograd · srbija · 2025</p>
      <p class="a-foot__nsv"><a href="%(back)s">a newsportvision concept</a></p>
    </div>
  </div>
</footer>""" % {"mark": mark("sm", decorative=True), "back": esc(back)}


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------

def shell(title, description, body, back="/"):
    """The host's shell, minus the host's furniture.

    Same boot script, same reveal engine, same asset versioning — so the
    microsite inherits every performance and security decision the site has
    already made. What it does not inherit is the header, the menu and the
    footer, because a microsite that keeps the parent's navigation on screen
    is a page, not a place.
    """
    return """<!doctype html>
<html lang="sr-Latn">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="only light">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(canonical)s">
<meta name="theme-color" content="#9F194F">
<meta property="og:type" content="website">
<meta property="og:site_name" content="newsportvision">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(base)s/assets/media/arms-mark.png">
<meta property="og:locale" content="sr_RS">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(base)s/assets/media/arms-mark.png">
<link rel="icon" href="/assets/media/nsv-logo.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/media/nsv-logo.png">
<link rel="preload" href="/assets/fonts/jost-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/jost-normal-latin-ext.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/tokens.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/base.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/arms.css?v=%(v)s">
<script>%(boot)s</script>
</head>
<body class="a-body" id="top">
<a class="skip-link" href="#main">Preskoči na sadržaj</a>
%(threshold)s
<main id="main">
%(body)s
</main>
%(footer)s
<script src="/assets/js/app.js?v=%(v)s" defer></script>
<script src="/assets/js/arms.js?v=%(v)s" defer></script>
</body>
</html>
""" % {
        "v": ASSET_V,
        "boot": INLINE_BOOT,
        "title": esc(title),
        "desc": esc(description),
        "canonical": BASE + "/arms/",
        "base": BASE,
        "threshold": threshold(back),
        "body": body,
        "footer": arms_footer(back),
    }


def arms(lang="en"):
    """The microsite. One page: the supplied architecture is a structure, not
    yet a library, and five routes standing empty would say less than five
    sections that say plainly what is still being written. Every section is
    already addressable — /arms/#ciljevi — so splitting them into routes later
    costs a line in the route table and breaks no link that exists today."""
    body = "\n".join((
        hero(),
        manifesto(),
        index(),
        ciljevi(),
        aktivnosti(),
        clanstvo(),
        odeljenja(),
        publication(),
        resources(),
        kontakti(),
        closing(),
    ))
    return shell(
        "A.R.M.S. | asocijacija roditelja maloletnih sportista",
        "A.R.M.S. — asocijacija roditelja maloletnih sportista. Udruženje "
        "građana, Beograd, Srbija, 2025. NewSportVision koncept.",
        body,
        back="/it/" if lang == "it" else "/",
    )
