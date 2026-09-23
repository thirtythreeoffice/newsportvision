# -*- coding: utf-8 -*-
"""
NEWSPORTVISION — layout & shared components.

These are the "components" of the brief's architecture, expressed as functions
that return markup. They are deliberately coarse: a component per compositional
object, never a component per word, so art direction stays controllable at the
page level.
"""

import hashlib, os
from html import escape as _e
from content import SITE, UI, MEDIA, AXIS, AXIS_LABEL
from lqip import LQIP
import linebreak as lb

BASE = SITE["domain"]

# Asset fingerprint: CSS and JS are served with a version query so a deploy is
# never half-old in a returning visitor's cache.
_STATIC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")


def _asset_version():
    h = hashlib.sha1()
    for sub in ("css", "js"):
        d = os.path.join(_STATIC, sub)
        for name in sorted(os.listdir(d)):
            with open(os.path.join(d, name), "rb") as f:
                h.update(name.encode())
                h.update(f.read())
    return h.hexdigest()[:8]


ASSET_V = _asset_version()

# ---------------------------------------------------------------------------
# Information architecture
# ---------------------------------------------------------------------------

NAV = [
    ("home",      "/",           {"en": "Home",       "it": "Home"},      None),
    ("products",  "/products/",  {"en": "Products",   "it": "Prodotti"},  "art"),
    ("services",  "/services/",  {"en": "Services",   "it": "Servizi"},   "sport"),
    ("about",     "/about/",     {"en": "About Us",   "it": "Chi siamo"}, "culture"),
    ("workshops", "/workshops/", {"en": "Workshops",  "it": "Laboratori"}, "culture"),
    ("help-desk", "/help-desk/", {"en": "Help Desk",  "it": "Help Desk"}, "sport"),
]
# A.R.M.S. is not one of these. It is a concept the house offers, reached
# through SERVICES, where it is listed with the rest of what the house does —
# and from the home page's own index of them. This menu stays the house's
# sections; the way in is the content that is about it.


# The three links the live site keeps in its header bar, in its own order.
HEADER_LINKS = ["services", "products", "about"]


# Pages that exist once, in their own language, outside the bilingual tree.
# A link to one of them is the same link from either side of the site.
SINGLE_ROOTS = ("/arms/",)


def url(lang, path):
    """Route for a locale. Italian mirrors English one level down.

    Every route is spelled with its trailing slash, which is the canonical
    form the pages are published under. A link that leaves the slash off is
    not wrong, but it costs the visitor a redirect before the page is even
    asked for — so the slash is put back here, once, for every link on the
    site rather than in each table of links.
    """
    base, hsh, frag = path.partition("#")
    base, qm, query = base.partition("?")
    if base and not base.endswith("/") and "." not in base.rsplit("/", 1)[-1]:
        base += "/"
    path = base + qm + query + hsh + frag
    if lang == "it" and not path.startswith(SINGLE_ROOTS):
        return "/it" + path
    return path


def esc(s):
    return _e(str(s), quote=True)


# ---------------------------------------------------------------------------
# Media
# ---------------------------------------------------------------------------

WIDTHS = (480, 800, 1200, 1600)
FALLBACK_W = 800        # the <img src> for browsers that read no srcset

_MEDIA_DIR = os.path.join(_STATIC, "media")
_media_v = {}


def media_v(stem):
    """
    A content hash for one photograph's files. Media are served as immutable,
    so a changed picture must arrive under a changed URL or a returning visitor
    keeps the old one for a year.
    """
    if stem not in _media_v:
        h = hashlib.sha1()
        for name in sorted(os.listdir(_MEDIA_DIR)):
            if name == stem or name.startswith(stem + "-") or name.startswith(stem + "."):
                with open(os.path.join(_MEDIA_DIR, name), "rb") as f:
                    h.update(name.encode())
                    h.update(f.read())
        _media_v[stem] = h.hexdigest()[:8]
    return _media_v[stem]


def img(key, lang, cls="", sizes="100vw", eager=False, counter=False, ratio=None,
        described=False):
    m = MEDIA[key]
    stem = m["src"].rsplit(".", 1)[0]
    alt = "" if described else (m["alt"].get(lang) or m["alt"]["en"])

    v = media_v(stem)

    if m.get("mark"):
        styles = ["--focus:%s" % m.get("focus", "50% 50%")]
        if ratio:
            styles.append("aspect-ratio:%s" % ratio)
        return ('<div class="frame frame--mark %s" style="%s">'
                '<img src="/assets/media/%s?v=%s" width="%d" height="%d" alt="%s" '
                'loading="%s" decoding="async"></div>'
                ) % (esc(cls), ";".join(styles), esc(m["src"]), v, m["w"], m["h"],
                     esc(alt), "eager" if eager else "lazy")

    def srcset(ext):
        return ", ".join("/assets/media/%s-%d.%s?v=%s %dw" % (stem, w, ext, v, w) for w in WIDTHS)

    frame_cls = ("frame " + cls).strip()
    attrs = ' data-counter' if counter else ''
    styles = []
    if ratio:
        styles.append("aspect-ratio:%s" % ratio)
    if m.get("focus"):
        styles.append("--focus:%s" % m["focus"])
    if key in LQIP:
        styles.append("--lqip:url(%s)" % LQIP[key])
    style = ' style="%s"' % ";".join(styles) if styles else ''
    return (
        '<div class="%s"%s%s>'
        '<picture>'
        '<source type="image/avif" srcset="%s" sizes="%s">'
        '<source type="image/webp" srcset="%s" sizes="%s">'
        '<img src="/assets/media/%s-%d.jpg?v=%s" srcset="%s" sizes="%s" '
        'width="%d" height="%d" alt="%s" loading="%s" decoding="async">'
        '</picture></div>'
    ) % (
        esc(frame_cls), style, attrs,
        srcset("avif"), esc(sizes),
        srcset("webp"), esc(sizes),
        stem, FALLBACK_W, v, srcset("jpg"), esc(sizes),
        m["w"], m["h"], esc(alt),
        "eager" if eager else "lazy",
    )


def figure(key, lang, cls="", sizes="100vw", num=None, caption=None, eager=False,
           counter=True, reveal=True, ratio=None, axis=None):
    """
    A plate. The number is the editorial anchor; the term beside it says where
    the picture sits on the axis, so a caption is never a decorative "Fig. 01"
    with nothing after it.
    """
    rev = ' data-reveal="frame"' if reveal else ''
    described = bool(caption)
    cap = ""
    if caption:
        ax = ' data-axis="%s"' % axis if axis else ''
        cap = ('<figcaption class="cap"%s>'
               '<i class="tab tab--cap" aria-hidden="true"></i>'
               '<p>%s</p></figcaption>') % (ax, esc(caption))
    return '<figure%s>%s%s</figure>' % (
        rev, img(key, lang, cls, sizes, eager, counter, ratio, described), cap)


# ---------------------------------------------------------------------------
# Small objects
# ---------------------------------------------------------------------------

def rule(cls="", draw=False):
    c = ("rule " + cls).strip()
    if draw:
        c += " rule--draw"
    return '<span class="%s" aria-hidden="true"></span>' % esc(c)


def shead(label, extra="", axis=None, paint=False):
    """A section head: a painted or ruled line to the edge, and a label."""
    ax = ' data-axis="%s"' % axis if axis else ''
    mark = '<i class="tab"></i>' if axis else ''
    line = ('<span class="paint paint--thin" aria-hidden="true" '
            'style="flex:1 1 auto"></span>') if paint else rule()
    return (
        '<div class="shead" data-reveal="fade"%s>%s%s<span class="meta">%s</span>%s</div>'
    ) % (ax, mark, line, esc(label), extra)


def action(href, label, lang, cursor=None, external=False):
    tgt = ' target="_blank" rel="noopener"' if external else ''
    cur = ' data-cursor="%s"' % esc(cursor) if cursor else ''
    return (
        '<a class="action" href="%s"%s%s>'
        '<span class="action__label">%s</span>'
        '<span class="action__arrow" aria-hidden="true"></span>'
        '</a>'
    ) % (esc(href), tgt, cur, esc(label))


def index_rows(items, lang, start=1):
    """
    The editorial index. Each row carries its term of the axis as a painted
    tab, and floods with that term's ink when you reach it — so moving down
    the list is moving across culture, sport and art.
    """
    out = ['<div class="index">']
    for i, (slug, name, href) in enumerate(items, start):
        ax = AXIS.get(slug)
        out.append(
            '<a class="index__row" href="%s"%s data-cursor="%s" data-reveal="up" data-delay="%d">'
            '<i class="tab" aria-hidden="true"></i>'
            '<span class="index__name">%s</span>'
            '<span class="index__go" aria-hidden="true"></span>'
            '</a>' % (esc(url(lang, href)),
                      ' data-axis="%s"' % ax if ax else '',
                      esc(UI[lang]["view"]), (i - start) * 55,
                      esc(name))
        )
    out.append("</div>")
    return "".join(out)


# ---------------------------------------------------------------------------
# Chrome
# ---------------------------------------------------------------------------

def masthead(lang, tag="a"):
    """
    The identity, rebuilt rather than reproduced as an image: three justified
    lines, the first finished by a rule. Same object the whole site is made of.
    """
    href = ' href="%s"' % url(lang, "/") if tag == "a" else ''
    return (
        '<%s class="mast"%s aria-label="NewSportVision — home">'
        '<span class="mast__l"><span>New</span><i class="mast__bar"></i></span>'
        '<span class="mast__l"><span>Sport</span></span>'
        '<span class="mast__l"><span>Vision</span></span>'
        '</%s>'
    ) % (tag, href, tag)


def lang_switch(lang, path, cls=""):
    other = "it" if lang == "en" else "en"
    return (
        '<div class="lang %s">'
        '<a class="meta" href="%s" hreflang="en" lang="en" aria-current="%s">EN</a>'
        '<span class="lang__sep" aria-hidden="true"></span>'
        '<a class="meta" href="%s" hreflang="it" lang="it" aria-current="%s">IT</a>'
        '</div>'
    ) % (esc(cls),
         esc(url("en", path)), "true" if lang == "en" else "false",
         esc(url("it", path)), "true" if lang == "it" else "false")


def site_header(lang, path, active, chapter=None):
    """chapter: when the page belongs to a concept rather than to the site's
    own spine, the masthead says which one and the section links stand down."""
    ui = UI[lang]
    links = []
    for key in ([] if chapter else HEADER_LINKS):
        item = next(n for n in NAV if n[0] == key)
        label = {"services": ui["nav_services"], "products": ui["nav_products"],
                 "about": ui["nav_about"]}[key]
        cur = ' aria-current="page"' if active == key else ''
        links.append('<a class="meta" href="%s"%s>%s</a>' % (esc(url(lang, item[1])), cur, esc(label)))

    return (
        '<header class="site-header">'
        '<div class="wrap header-inner">'
        '%s'
        '<nav class="header-nav" aria-label="%s">'
        '<span class="header-links">%s</span>'
        '%s'
        '<button class="menu-btn meta" type="button" aria-expanded="false" aria-controls="menu">'
        '<span>%s</span>'
        '<span class="menu-btn__bars" aria-hidden="true"><i></i><i></i></span>'
        '</button>'
        '</nav></div></header>'
    ) % (masthead(lang) + (
             '<span class="chapter-of"><span aria-hidden="true">/</span>'
             '<span class="chapter-of__here">%s</span></span>' % esc(chapter)
             if chapter else ""),
         esc(ui["menu"]), "".join(links),
         "" if chapter else lang_switch(lang, path), esc(ui["menu"]))


def menu_panel(lang, path, active, rows=None, foot=None):
    """rows: (axis, href, label, current) when a concept brings its own
    destinations. The panel, its wipe, its focus trap and its type are the
    site's; only the list inside it changes."""
    ui = UI[lang]
    items = []
    rows = rows if rows is not None else [
        (ax, url(lang, href), labels[lang], active == key)
        for key, href, labels, ax in NAV]
    # What the list costs in rows, counted from the list itself so that adding
    # or removing a name re-sizes the type without anyone editing a number. A
    # row set one level up is smaller and costs less than a whole one; .6 is
    # what it measures, its own line plus the space that sets it apart.
    cost = 0.0
    for row in rows:
        cost += .6 if (len(row) > 4 and row[4]) else 1
    for row in rows:
        ax, href, label, cur = row[:4]
        # a fifth value marks a row that belongs one level up from the list
        up = len(row) > 4 and row[4]
        items.append(
            '<li%s%s><a href="%s"%s>%s'
            '<span class="mword">%s</span></a></li>'
            % (' class="menu-up"' if up else '',
               ' data-axis="%s"' % ax if ax else '',
               esc(href), ' aria-current="page"' if cur else '',
               '<i class="menu-up__arrow" aria-hidden="true"></i>' if up
               else '<i class="tab menu-tab" aria-hidden="true"></i>',
               esc(label))
        )
    return (
        '<div class="menu-panel" id="menu" aria-hidden="true" style="--menu-rows:%s">'
        '<div class="wrap header-inner">'
        '%s'
        '<nav class="header-nav">'
        '%s'
        '<button class="menu-btn meta" type="button" data-menu-close>'
        '<span>%s</span>'
        '<span class="menu-btn__bars" aria-hidden="true"><i></i><i></i></span>'
        '</button></nav></div>'
        '<nav class="wrap" aria-label="%s"><ul class="menu-list">%s</ul></nav>'
        '<div class="wrap menu-foot">%s</div></div>'
    ) % (("%.2f" % cost).rstrip("0").rstrip("."),
         masthead(lang, tag="span"),
         "" if rows is not None else lang_switch(lang, path),
         esc(ui["close"]),
         esc(ui["menu"]), "".join(items),
         foot if foot is not None else (
             '<a class="meta tlink tlink--invert" href="mailto:%s">%s</a>'
             '<a class="meta tlink tlink--invert" href="%s">%s</a>'
             % (esc(SITE["email"]), esc(SITE["email"]),
                esc(url(lang, "/privacy/")), esc(ui["privacy"]))))


def footer(lang, path, invite, got_idea):
    ui = UI[lang]
    socials = "".join(
        '<a class="meta tlink tlink--invert" href="%s" target="_blank" rel="noopener">%s</a>'
        % (esc(u), esc(n)) for n, u in SITE["social"]
    )
    invite_html = "".join('<p>%s</p>' % esc(l) for l in invite)
    return (
        '<footer class="footer-canvas on-yellow" data-field="yellow">'
        '<div class="wrap">'
        '<div class="grid">'
        '<div class="c7" data-reveal="up">'
        # The invitation is three paragraphs of its own; a <p> cannot hold them,
        # and the parser would close it empty and leave them unstyled.
        '<div class="lead measure-sm">%s</div>'
        '</div>'
        '<div class="c5 s8" data-reveal="up" data-delay="90">'
        '<span class="meta meta--quiet">%s</span>'
        '</div>'
        '</div>'

        '<div data-justify-stack data-jmax="280" style="margin-top:var(--space-5)">%s</div>'

        '<a class="mailto-big tlink" href="mailto:%s" data-cursor="%s" '
        'style="margin-top:var(--space-3)">%s</a>'

        '%s'

        '<div class="footer-grid" style="margin-top:var(--space-4)">'
        '<div class="social">%s</div>'
        '<a class="meta tlink" href="%s">%s</a>'
        '<span class="meta meta--quiet">%s</span>'
        '<a class="meta to-top" href="#top"><span class="to-top__bar" aria-hidden="true"></span>%s</a>'
        '</div>'
        '<div class="colophon">'
        '<div class="colourbar" aria-hidden="true">'
        '<i></i><i></i><i></i><i></i><i></i><i></i></div>'
        '</div>'
        '<span class="crop crop--bl" aria-hidden="true"></span>'
        '<span class="crop crop--br" aria-hidden="true"></span>'
        '</div></footer>'
    ) % (invite_html,
         esc(ui["contact_line"]),
         "".join('<span class="hl got" data-jl-host><span class="hlw" data-jl>%s</span></span>' % esc(l)
                 for l in lb.auto(got_idea)),
         esc(SITE["email"]), esc(ui["open"]), esc(SITE["email"]),
         '<div style="margin-top:var(--space-4)">%s</div>' % rule("rule--thin"),
         socials,
         esc(url(lang, "/privacy/")), esc(ui["privacy"]),
         esc(ui["copyright"]),
         esc(ui["to_top"]))


# ---------------------------------------------------------------------------
# Document
# ---------------------------------------------------------------------------

# The one inline script. It runs in the head, before first paint:
#   - `js` switches on the reveal start-states;
#   - `js-justify` holds display stacks back until they are set (a deferred
#     script can run after the browser has already painted an unset heading);
#   - `--vw` is the page's real width, so full-bleed pictures and fields meet
#     the screen edge exactly from the first frame (see tokens.css);
#   - photographs are marked as they load, so they fade in rather than pop.
#     Load events do not bubble, but they can be captured at the document.
# build.py pins this exact string by hash in the Content-Security-Policy.
INLINE_BOOT = ("(function(d){var r=d.documentElement;r.className+=' js js-justify';"
               "r.style.setProperty('--vw',r.clientWidth+'px');"
               "d.addEventListener('load',function(e){var t=e.target;"
               "if(t&&t.tagName==='IMG')t.classList.add('is-loaded')},true)})(document);")

# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------

def first_photo_now(body):
    """
    The first photograph on a page is the first one anybody reaches, often
    within a second of arriving, so it is fetched immediately rather than
    waiting for the reader to scroll near it.

    It is not given a raised priority: no page opens on a photograph — every
    one opens on type — so the largest paint waits on the display face, and a
    picture below the fold must not be fetched ahead of it.
    """
    i = body.find('loading="lazy"')
    if i < 0 or 'loading="eager"' in body[:i]:
        return body      # this page already fetches its first picture at once
    return body[:i] + 'loading="eager"' + body[i + len('loading="lazy"'):]


def page(lang, path, title, description, body, active=None, footer_html=None,
         body_class="", og_image="skate-architecture-1600.jpg", noindex=False):
    ui = UI[lang]
    body = first_photo_now(body)
    canonical = BASE + url(lang, path)
    alt_en = BASE + url("en", path)
    alt_it = BASE + url("it", path)

    return """<!doctype html>
<html lang="%(lang)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="only light">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(indexing)s
<meta name="theme-color" content="#FAC51C">
<meta property="og:type" content="website">
<meta property="og:site_name" content="newsportvision">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(base)s/assets/media/%(og)s">
<meta property="og:locale" content="%(locale)s">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">
<meta name="twitter:image" content="%(base)s/assets/media/%(og)s">
<link rel="icon" href="/assets/media/nsv-logo.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/media/nsv-logo.png">
<link rel="preload" href="/assets/fonts/archivo-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/newsreader-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/tokens.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/base.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/components.css?v=%(v)s">
<link rel="stylesheet" href="/assets/css/pages.css?v=%(v)s">
<script>%(boot)s</script>
</head>
<body class="%(bodycls)s" id="top">
<a class="skip-link" href="#main">%(skip)s</a>
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
%(extra)s
</body>
</html>
""" % {
        "v": ASSET_V,
        "boot": INLINE_BOOT,
        "lang": lang,
        "indexing": ('<meta name="robots" content="noindex,follow">' if noindex else
                     ('<link rel="canonical" href="%s">'
                      '<link rel="alternate" hreflang="en" href="%s">'
                      '<link rel="alternate" hreflang="it" href="%s">'
                      '<link rel="alternate" hreflang="x-default" href="%s">'
                      % (esc(canonical), esc(alt_en), esc(alt_it), esc(alt_en)))),
        "title": esc(title),
        "desc": esc(description),
        "canonical": esc(canonical),
        "alt_en": esc(alt_en),
        "alt_it": esc(alt_it),
        "base": BASE,
        "og": og_image,
        "locale": "en_GB" if lang == "en" else "it_IT",
        "bodycls": esc(body_class),
        "skip": esc(ui["skip"]),
        "header": site_header(lang, path, active),
        "menu": menu_panel(lang, path, active),
        "body": body,
        "footer": footer_html or "",
        "extra": '<script src="/assets/js/helpdesk.js?v=%s" defer></script>' % ASSET_V if active == "help-desk" else "",
    }
