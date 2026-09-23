# -*- coding: utf-8 -*-
"""
A.R.M.S. — a chapter of newsportvision.com, not a site beside it.

The first build of this page gave ARMS its own ground, its own typeface and its
own furniture, and it read as a second website wearing the host's link. This one
takes the opposite position, and it is the right one: ARMS is a concept of the
house, so it is set in the house's types, on the house's paper, with the house's
header, menu, reveals, justification engine and closing canvas. What it brings
of its own is what an identity actually is — a colour relationship, a geometry,
a vocabulary, a voice.

    from the host   the measure, the grid, the acts and their tongues, the
                    justified stacks, the index rows, the chapter blocks, the
                    shead rules, the reveal timing, the intro, the cursor, the
                    grain, the footer canvas. Nothing is reimplemented.
    from A.R.M.S.   magenta #9F194F and blue #5C9ED6 as whole surfaces rather
                    than small cards, green #077734 kept for resources, the
                    four-block geometry used twice and never as wallpaper, and
                    every word of Serbian exactly as the material sets it.

Measured out of the artwork: blocks of 702.99 with a 34.02 gutter, lower blocks
0.3938 of the upper, a bracket 15.59 thick running from the centre of one
column to the centre of the other.
"""

from render import (ASSET_V, INLINE_BOOT, BASE, esc, site_header,
                    menu_panel, url)                                # noqa: E402

# ---------------------------------------------------------------------------
# Words — transcribed, never written
# ---------------------------------------------------------------------------

# The hero sets the name as a statement, not as a transcript of the mark: two
# lines fill the measure at a size the screen can hold, and the mark itself
# still carries the four-line setting a few centimetres away.
NAME = ("ASOCIJACIJA RODITELJA", "MALOLETNIH SPORTISTA")

MANIFESTO = (
    "ne postoji dobar roditelj koji nije solidaran sa drugim solidarnim "
    "roditeljima.",

    "solidarnost jača neverovatnom snagom sve solidarne.",

    "ako ne zastupaš sebe sigurno će te zastupati neko drugi, po pravilu "
    "mnogo gori od tebe.... tako bude u društvenom životu.",

    "udruži se sa sebi sličnima......po ciljevima, interesima, osećaju i "
    "naročito KULTURI , neudružen si prirodno ‘laka meta’ a često i "
    "‘plen’.",

    "daj svoj roditeljski maksimum dok je dete maloletno, pripremi ga i nauči "
    "da posle brine o sebi i drugima što bolje - samostalno, na bazi "
    "prvenstveno lične odgovornosti.",

    "zdrav sport je za nas aktivnost, sredina, sredstvo i put kojim deca "
    "najbolje mogu da nauče i spreme se za ono šta ih čeka u životu.",
)

CLOSING = ("SPORT BEZ", "KULTURE NEMA", "BUDUĆNOST")

SECTIONS = (
    ("ciljevi",    "ciljevi",    None,            "01"),
    ("aktivnosti", "aktivnosti", "šta ne radimo", "02"),
    ("clanstvo",   "članstvo",   None,            "03"),
    ("odeljenja",  "odeljenja",  "po sportovima", "04"),
    ("kontakti",   "kontakti",   None,            "05"),
)

RESOURCES = (
    ("help desk",          "pitanje roditelja, odgovor na jednom mestu"),
    ("predlozi roditelja", "šta roditelji predlažu jedni drugima"),
    ("istorija",           "odakle asocijacija dolazi"),
    ("partneri",           "sa kim se radi"),
)

PUB_TITLE = ("30 PREDLOGA", "ZA RODITELJA", "MALOLETNOG", "SPORTISTE")
PUB_PARTS = ("šta znati (10)", "šta raditi (10)", "šta ne raditi (10)")

# The first row belongs to the house, not to the association: same list, same
# type, one level up — smaller, with the arrow the microsite already uses for
# its way back, and set apart by space rather than by a rule or a box.
MENU_ROWS = [(None,   "/",            "newsportvision",       False, True),
             ("arms", "#ciljevi",    "ciljevi",              False),
             ("arms", "#aktivnosti", "aktivnosti",           False),
             ("arms", "#clanstvo",   "članstvo",             False),
             ("arms", "#odeljenja",  "odeljenja po sportovima", False),
             ("arms", "#kontakti",   "kontakti",             False),
             (None,   "#resursi",    "resursi",              False)]


# ---------------------------------------------------------------------------
# The host's own pieces, filled with ARMS
# ---------------------------------------------------------------------------

def jstack(lines, jmax=240, first_rule=None, cls="jstack"):
    """A justified stack: the site's signature, and the reason this page reads
    as the same hand. Every line is stretched to one measure on Archivo's width
    axis by justify.js; a short first line hands the rest of its measure to a
    rule, exactly as the home page gives it to QUICK."""
    out = []
    if first_rule:
        out.append('<span class="hl hl--rule hl--bleed" data-jl-host>'
                   '<span class="jline__t" data-jl data-jl-rule>%s</span>'
                   '<i class="jline__rule"></i></span>' % esc(first_rule))
    for t in lines:
        out.append('<span class="hl" data-jl-host>'
                   '<span class="hlw" data-jl>%s</span></span>' % esc(t))
    return ('<div class="%s" data-justify-stack data-jmax="%d">%s</div>'
            % (cls, jmax, "".join(out)))


def shead(label, thin=False):
    return ('<div class="shead" data-reveal="fade">'
            '<span class="rule%s" aria-hidden="true"></span>'
            '<span class="meta">%s</span></div>'
            % (" rule--thin" if thin else "", esc(label)))


def prep(_what=None):
    """A category whose content is still being written says so in two words.

    It used to say a whole sentence about founding acts and assemblies, which
    read as a note between colleagues rather than as anything a visitor came
    for. Two words, in the site's quietest type, is the whole statement.
    """
    return ('<p class="arms-prep"><i class="tab" aria-hidden="true"></i>'
            '<span>u pripremi</span></p>')


def mark(cls=""):
    """The official artwork, placed.

    Not rebuilt: the supplied PDF was converted to SVG with every glyph turned
    into an outline, so the construction, proportions, spacing and colour
    relationships are the artwork's own, down to the coordinate. It is one
    asset, one element, and it is never recomposed — only its size changes.
    """
    alt = ("A.R.M.S. — asocijacija roditelja maloletnih sportista. "
           "Udruženje građana, Beograd, Srbija, 2025. NewSportVision koncept. "
           "Tok pozitivne energije.")
    return ('<img class="ark %s" src="/assets/media/arms-mark.svg" alt="%s" '
            'width="1701" height="1701" decoding="async">' % (cls, esc(alt)))


# ---------------------------------------------------------------------------
# Acts
# ---------------------------------------------------------------------------

def hero():
    """No logo in the middle of a slide. The association's name is the page's
    opening statement, set as a justified block the way this site opens every
    chapter, with A.R.M.S. taking the rule line. The mark arrives cropped
    against the right edge, the way the host crops its photographs."""
    return """
<section class="act-hero arms-hero on-paper tongue tongue--right" data-field="paper"
         data-intro aria-labelledby="arms-h">
  <div class="wrap hero-top">
    <span class="meta">newsportvision koncept</span>
    <span class="meta meta--quiet">udruženje građana &middot; beograd / srbija / 2025</span>
  </div>
  <div class="wrap arms-hero__in">
    <h1 class="hero-stack arms-hero__stack" id="arms-h" data-justify-stack data-jmax="230">
      <span class="hl hl--rule hl--bleed" data-jl-host><span class="jline__t" data-jl data-jl-rule>A.R.M.S.</span><i class="jline__rule"></i></span>%(lines)s</h1>
  </div>
  <div class="wrap hero-bottom">
    <span class="rule rule--thin" aria-hidden="true"></span>
    <span class="meta">&deg; tok pozitivne energije &deg;</span>
  </div>
</section>""" % {
        # Wide, the name is two lines that fill the measure. Narrow, it
        # recomposes into the four-line setting the mark itself uses — the
        # host's own mechanism for exactly this, and here it lands the page
        # back on the logo's composition on a phone.
        "lines": (
            '<span class="hl" data-jl-host><span class="hlw" data-jl '
            'data-jl-narrow="ASOCIJACIJA">ASOCIJACIJA RODITELJA</span></span>'
            '<span class="hl" data-jl-host data-jl-only="narrow" hidden>'
            '<span class="hlw" data-jl>RODITELJA</span></span>'
            '<span class="hl" data-jl-host><span class="hlw" data-jl '
            'data-jl-narrow="MALOLETNIH">MALOLETNIH SPORTISTA</span></span>'
            '<span class="hl" data-jl-host data-jl-only="narrow" hidden>'
            '<span class="hlw" data-jl>SPORTISTA</span></span>'),
    }


def manifesto():
    """Six statements, paced by surface rather than by box. Three stand on the
    ink this site already uses for its dramatic acts, one takes a whole magenta
    field to itself, two return to paper. The bracket from the mark travels
    down the ink act and nowhere else."""
    def say(i, text, size="lg"):
        return ('<p class="arms-say arms-say--%s" data-reveal="up" data-delay="%d">%s</p>'
                % (size, (i % 2) * 70, esc(text)))

    return """
<section class="act-arms-ink on-ink tongue tongue--left" data-field="ink"
         aria-labelledby="arms-man">
  <div class="wrap">
    %(head)s
    <h2 class="visually-hidden" id="arms-man">Zašto se roditelji udružuju</h2>
    <div class="arms-says">
      <span class="arms-brace" aria-hidden="true"></span>
      %(a)s
      %(b)s
      %(c)s
    </div>
  </div>
</section>

<section class="act-arms-field on-arms" data-field="ink">
  <div class="wrap">
    %(d)s
  </div>
</section>

<section class="act-arms-paper on-paper" data-field="paper">
  <div class="wrap arms-says arms-says--close">
    %(e)s
    %(f)s
  </div>
</section>""" % {
        "head": shead("zašto se roditelji udružuju"),
        "a": say(0, MANIFESTO[0]),
        "b": say(1, MANIFESTO[1], "sm"),
        "c": say(2, MANIFESTO[2]),
        "d": say(0, MANIFESTO[3], "xl"),
        "e": say(0, MANIFESTO[4]),
        "f": say(1, MANIFESTO[5], "sm"),
    }


def register():
    """The five categories, once.

    The first build listed them in an index and then repeated them as five
    chapter blocks — the same five words twice, with a ghosted number behind
    each heading that carried no information the list above had not already
    given. This is one object instead of two: the site's index row, opened up
    to hold the category's thesis and its state, and still the anchor the menu
    points at.
    """
    items = (
        ("ciljevi", "ciljevi", None,
         "što udruženiji — to bolji i jači.",
         "Ciljevi se upisuju iz osnivačkog akta."),
        ("aktivnosti", "aktivnosti", "šta ne radimo",
         "Ono što asocijacija radi i ono što svesno ne radi stoje jedno uz "
         "drugo, jer se jedno bez drugog ne razume.",
         "Spisak aktivnosti i granice rada se pripremaju."),
        ("clanstvo", "članstvo", None,
         "Ko može da se učlani, kako se učlanjuje i šta članstvo znači.",
         "Uslovi članstva se objavljuju kada ih usvoji skupština."),
        ("odeljenja", "odeljenja", "po sportovima",
         "Odeljenja se otvaraju po sportu, kako se roditelji udružuju.",
         "Spisak odeljenja se otvara sa prvim upisanim sportom."),
        ("kontakti", "kontakti", None,
         "udruženje građana, beograd, srbija.",
         "Adresa i kontakt se objavljuju po registraciji."),
    )
    rows = []
    for i, (slug, name, sub, thesis, state) in enumerate(items):
        label = esc(name) + ('<span class="arms-reg__sub">%s</span>' % esc(sub)
                             if sub else "")
        rows.append(
            '<section class="arms-reg" id="%s" data-axis="arms" '
            'aria-labelledby="h-%s" data-reveal="up" data-delay="%d">'
            '<i class="tab" aria-hidden="true"></i>'
            '<h2 class="arms-reg__n" id="h-%s">%s</h2>'
            '<div class="arms-reg__say"><p class="arms-reg__t">%s</p>%s</div>'
            '</section>'
            % (slug, slug, i * 60, slug, label, esc(thesis), prep(state)))
    return """
<section class="act-arms-reg on-paper" data-field="paper" aria-labelledby="arms-idx">
  <div class="wrap">
    %(head)s
    <h2 class="visually-hidden" id="arms-idx">Sadržaj</h2>
    <div class="arms-register">%(rows)s</div>
  </div>
</section>""" % {"head": shead("sadržaj"), "rows": "".join(rows)}


def plate():
    """The mark, on its own ground.

    The artwork was drawn for white, and this is the only white surface on the
    page — which is the whole point: it is shown, once, with room around it,
    the way a gallery hangs a thing rather than filling a gap with it.
    """
    return """
<section class="act-arms-plate" aria-label="A.R.M.S.">
  <div class="wrap">
    <div class="arms-plate__in" data-reveal="fade">%s</div>
  </div>
</section>""" % mark("ark--plate")


def publication():
    """A publication on a green field, its title set the way this site sets a
    title: justified to the measure. The link is a link — this site does not
    use pill buttons, and a download that does not exist yet is not dressed up
    as one that does."""
    return """
<section class="act-arms-pub on-arms-green" data-field="ink" aria-labelledby="arms-pub">
  <div class="wrap">
    %(head)s
    <h2 class="visually-hidden" id="arms-pub">30 predloga za roditelja maloletnog sportiste</h2>
    %(stack)s
    <div class="grid arms-pub__foot">
      <div class="c6" data-reveal="up">
        <ul class="arms-pub__parts">%(parts)s</ul>
      </div>
      <div class="c4 s8" data-reveal="up" data-delay="80">
        <span class="meta meta--quiet">PDF</span>
        %(prep)s
      </div>
    </div>
  </div>
</section>""" % {
        "head": shead("publikacija", thin=True),
        # Held well under the hero: this is a resource inside the chapter, not
        # the chapter's headline. Capped, the engine justifies the four lines
        # to their own widest line instead of the page, which is what makes
        # the title read as an object standing on the field.
        "stack": jstack(PUB_TITLE, jmax=92, cls="jstack arms-pub__t"),
        "parts": "".join('<li><span class="meta">%s</span></li>' % esc(p)
                         for p in PUB_PARTS),
        "prep": prep("Publikacija se priprema za preuzimanje."),
    }


def resources():
    rows = []
    for i, (name, note) in enumerate(RESOURCES):
        rows.append(
            '<div class="index__row index__row--static" data-reveal="up" data-delay="%d">'
            '<i class="tab" aria-hidden="true"></i>'
            '<span class="index__name">%s</span>'
            '<span class="index__note">%s</span></div>'
            % (i * 55, esc(name), esc(note)))
    return """
<section class="act-arms-res on-paper" id="resursi" data-field="paper" aria-labelledby="arms-res">
  <div class="wrap">
    %(head)s
    <h2 class="visually-hidden" id="arms-res">Resursi</h2>
    <div class="index arms-res">%(rows)s</div>
    %(prep)s
  </div>
</section>""" % {"head": shead("resursi"), "rows": "".join(rows),
                 "prep": prep("Svaki modul se otvara kada njegov sadržaj bude spreman.")}


def closing():
    """The host's own thesis, in Serbian: its services page opens with SPORT
    WITHOUT CULTURE IS A DISSERVICE. This chapter closes with the same idea in
    the association's words, set the same way, on the house's yellow."""
    return """
<section class="act-arms-close on-yellow tongue tongue--right" data-field="yellow"
         aria-label="%(alt)s">
  <div class="wrap">%(stack)s</div>
</section>""" % {"alt": esc(" ".join(CLOSING).lower()),
                 "stack": jstack(CLOSING, jmax=190,
                                 cls="jstack statement-stack arms-close__t")}


def foot(lang):
    """The site's closing canvas, in ARMS ink: the same justified line, the
    same oversized mailto, the same rule — and the way back, named."""
    return """
<footer class="footer-canvas on-arms arms-foot" data-field="ink">
  <div class="wrap">
    %(stack)s
    <a class="mailto-big tlink" href="mailto:office@newsportvision.com"
       data-cursor="Piši" style="margin-top:var(--space-3)">office@newsportvision.com</a>
    <div style="margin-top:var(--space-4)"><span class="rule rule--thin" aria-hidden="true"></span></div>
    <div class="arms-foot__grid" style="margin-top:var(--space-3)">
      <span class="meta meta--quiet">a.r.m.s. &middot; newsportvision koncept</span>
      <a class="meta tlink tlink--invert arms-foot__back" href="%(home)s" data-cursor="Nazad">
        <span class="arms-foot__arrow" aria-hidden="true"></span>newsportvision
      </a>
    </div>
  </div>
</footer>""" % {
        "stack": ('<div class="arms-foot__say" data-justify-stack data-jmax="250">'
                  '<span class="hl got" data-jl-host>'
                  '<span class="hlw" data-jl>Udruži se</span></span></div>'),
        "home": esc(url(lang, "/")),
    }


# ---------------------------------------------------------------------------
# The page
# ---------------------------------------------------------------------------

def shell(lang, title, description, body):
    """The host's head, exactly: same boot script, same four stylesheets, same
    justification engine and behaviour script, same versioning. arms.css is a
    fifth sheet that adds ARMS's surfaces and takes nothing away."""
    # The way back is now a destination in the list itself, so the legal row
    # keeps only what it is for.
    menu_foot = (
        '<a class="meta tlink tlink--invert" '
        'href="mailto:office@newsportvision.com">office@newsportvision.com</a>')
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
<link rel="preload" href="/assets/fonts/archivo-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/newsreader-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/tokens.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/base.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/components.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/pages.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/arms.css?v=%(v)s">
<script>%(boot)s</script>
</head>
<body class="arms" id="top">
<a class="skip-link" href="#main">Preskoči na sadržaj</a>
<div class="grain" aria-hidden="true"></div>
%(header)s
%(menu)s
<main id="main">
%(body)s
</main>
%(footer)s
<div class="cursor" aria-hidden="true"><i class="cursor__bar"></i><span class="cursor__label"></span></div>
<script src="/assets/js/justify.js?v=%(v)s" defer></script>
<script src="/assets/js/app.js?v=%(v)s" defer></script>
</body>
</html>
""" % {
        "v": ASSET_V,
        "boot": INLINE_BOOT,
        "title": esc(title),
        "desc": esc(description),
        "canonical": BASE + "/arms/",
        "base": BASE,
        "header": site_header(lang, "/arms/", "arms", chapter="A.R.M.S."),
        "menu": menu_panel(lang, "/arms/", "arms", rows=MENU_ROWS, foot=menu_foot),
        "body": body,
        "footer": foot(lang),
    }


def arms(lang="en"):
    body = "\n".join((hero(), manifesto(), register(),
                      publication(), resources(), plate(), closing()))
    return shell(
        lang,
        "A.R.M.S. | asocijacija roditelja maloletnih sportista",
        "A.R.M.S. — asocijacija roditelja maloletnih sportista. Udruženje "
        "građana, Beograd, Srbija, 2025. NewSportVision koncept.",
        body)
