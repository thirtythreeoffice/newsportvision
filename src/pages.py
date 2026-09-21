# -*- coding: utf-8 -*-
"""
NEWSPORTVISION — page compositions.

Seven fields on the homepage, in this order and no other:

    01  hero       YELLOW   the identity, at page scale
    02  event      INK      the institution speaking
    03  products   PAPER    reading
    04  services   PAPER    reading, continued through a photograph
    05  axis       INK      culture / sport / art, the mission set like the logo
    06  history    PAPER    where it came from
    07  close      YELLOW   the invitation

Yellow is spent twice: to open and to close. Between those two moments it does
not appear as a field at all, which is what makes it land when it does.
"""

from content import (AXIS, AXIS_LABEL, CHAPTER_AXIS, SITE, UI, HOME, PRODUCTS_INDEX, SERVICES_INDEX, GUIDELINES,
                     BOOKS, WORKSHOPS, HELPDESK, HELPDESK_NEWS, WORK_IN_PROGRESS,
                     ABOUT, PRIVACY_TITLE, PRIVACY_HEAD, PRIVACY_LEAD, PRIVACY_SECTIONS)
from render import (esc, url, rule, shead, action, index_rows, figure, img, page,
                    footer, NAV)
import linebreak as lb

# ---------------------------------------------------------------------------
# Hero line-breaking.
#
# The logo's three lines fill one measure because they are naturally similar
# widths — NEW is short and takes a rule; SPORT and VISION are near-identical.
# The hero is broken to the same logic, so the same setting rule applies:
#
#   QUICK ▬▬▬▬▬▬▬       short line, finished by the bar
#   STEPS INTO THE      \  near-identical natural widths, so the width axis
#   SPORTS FUTURE       /  closes the gap without tearing the words apart
#
# Not one word is changed or reordered; only where the line turns.
#   (text, carries_rule, narrow_text, only_on)
# ---------------------------------------------------------------------------
HERO_SET = {
    "en": [("QUICK",           True,  None,       None),
           ("STEPS INTO THE",  False, "STEPS",    None),
           ("INTO THE",        False, None,       "narrow"),
           ("SPORTS FUTURE",   False, "SPORTS",   None),
           ("FUTURE",          False, None,       "narrow")],
    # On a phone "PASSI" and "NELLO" cannot each span a "SPORT DEL" line: at the
    # width axis's widest and the tracking limit they still end 42px and 12px
    # short, and the justified block goes ragged. Kept together they fill it.
    "it": [("CELERI",             True,  None,        None),
           ("PASSI NELLO",        False, None,        None),
           ("SPORT DEL FUTURO",   False, "SPORT DEL", None),
           ("FUTURO",             False, None,        "narrow")],
}


def hero_stack(lang):
    out = []
    for text, has_rule, narrow, only in HERO_SET[lang]:
        attrs = ""
        if narrow:
            attrs += ' data-jl-narrow="%s"' % esc(narrow)
        only_attr = ' data-jl-only="%s"' % only if only else ""
        hidden = " hidden" if only == "narrow" else ""
        if has_rule:
            out.append(
                '<span class="hl hl--rule hl--bleed" data-jl-host%s%s>'
                '<span class="jline__t" data-jl data-jl-rule%s>%s</span>'
                '<i class="jline__rule"></i></span>'
                % (only_attr, hidden, attrs, esc(text)))
        else:
            out.append(
                '<span class="hl" data-jl-host%s%s>'
                '<span class="hlw" data-jl%s>%s</span></span>'
                % (only_attr, hidden, attrs, esc(text)))
    return "".join(out)


def jstack(lines, tag="h2", cls="", jmax=None, extra=""):
    """A justified stack of display lines — the logo's setting rule, reusable."""
    jm = ' data-jmax="%s"' % jmax if jmax else ""
    body = "".join(
        '<span class="hl" data-jl-host><span class="hlw" data-jl>%s</span></span>' % esc(l)
        for l in lines)
    return '<%s class="jstack %s" data-justify-stack%s%s>%s</%s>' % (tag, esc(cls), jm, extra, body, tag)


def paras(items, cls="prose"):
    return '<div class="%s">%s</div>' % (cls, "".join("<p>%s</p>" % esc(p) for p in items))


# ===========================================================================
# HOME
# ===========================================================================

def home(lang):
    c = HOME[lang]
    ui = UI[lang]
    p = PRODUCTS_INDEX[lang]
    s = SERVICES_INDEX[lang]
    a = ABOUT[lang]

    # ---- 01 hero -----------------------------------------------------------
    hero = """
<section class="act-hero on-yellow tongue tongue--right tongue--paint tongue--paint-2" data-field="yellow" data-intro aria-labelledby="hero-h">
  <i class="sweep" aria-hidden="true"
     style="top:29%%;height:clamp(64px,10vh,132px);--sweep-w:78%%;--sweep-ink:var(--nsv-art);--sweep-o:.15;--sweep-tilt:-1.2deg"></i>
  <div class="wrap hero-top">
    <span class="meta">%(kicker)s</span>
  </div>
  <div class="wrap">
    <h1 class="hero-stack" id="hero-h" data-justify-stack data-jmax="240">%(lines)s</h1>
  </div>
  <div class="wrap hero-bottom grid">
    <div class="c8 hero-foot-l">
      <span class="meta">%(sub)s</span>
    </div>
    <a class="hero-next c4 s9" href="#fsf" data-cursor="%(view)s">
      <span class="rule rule--thin"></span>
      <span class="meta meta--quiet">%(eyebrow)s</span>
      <span class="fsf">FSF <span aria-hidden="true">26</span></span>
      <span class="meta">%(scroll)s — %(place)s</span>
    </a>
  </div>
</section>""" % {
        "kicker": esc(c["hero_kicker"]),
        "lines": hero_stack(lang),
        "sub": esc(c["hero_sub"]),
        "view": esc(ui["view"]),
        "eyebrow": esc(c["event_eyebrow"]),
        "scroll": esc("03.10.2026"),
        "place": esc(c["event_place"]),
    }

    # ---- 02 event ----------------------------------------------------------
    event = """
<section class="act-event on-ink tongue tongue--left" id="fsf" data-field="ink" aria-labelledby="fsf-h">
  <div class="wrap">
    %(shead)s
    <div class="grid" style="margin-top:var(--space-4)">
      <div class="c3 event-slit">%(fig)s</div>
      <div class="c8 s5">
        <p class="meta meta--quiet">%(about)s</p>
        %(title)s
        <dl class="datarow datarow--2">
          <div><dt class="meta meta--quiet">%(l_date)s</dt><dd>%(date)s</dd></div>
          <div><dt class="meta meta--quiet">%(l_place)s</dt><dd>%(place)s</dd></div>
        </dl>
        <div class="prose measure" style="margin-top:var(--space-3)" data-reveal="up"><p>%(body)s</p></div>
        <p class="event-close" style="margin-top:var(--space-4)" data-reveal="up">%(close)s</p>
      </div>
    </div>
  </div>
  <div class="wrap"><i class="paint paint--3 act-close" aria-hidden="true"></i></div>
</section>""" % {
        "shead": shead(c["event_eyebrow"]),
        "fig": figure("gathering", lang,
                      sizes="(max-width:767px) 100vw, (max-width:1279px) 42vw, (max-width:1800px) 30vw, 22vw",
                      axis="culture"),
        "about": esc(c["event_about"]),
        "title": jstack(lb.auto(c["event_name"]), tag="h2", cls="event-title", jmax="150",
                        extra=' id="fsf-h"'),
        "l_date": esc("Date" if lang == "en" else "Data"),
        "l_place": esc("Place" if lang == "en" else "Luogo"),
        "date": esc(c["event_date"]),
        "place": esc(c["event_place"]),
        "body": esc(c["event_body"]),
        "close": "<br>".join(esc(l) for l in c["event_close"]),
    }

    # ---- 03 products -------------------------------------------------------
    products = """
<section class="act-po on-paper" data-field="paper" aria-labelledby="prod-h">
  <div class="wrap">
    %(shead)s
    <div class="grid" style="margin-top:var(--space-3)">
      <div class="c7">
        <h2 class="h2 po-head" id="prod-h" data-reveal="up">%(head)s</h2>
        <div class="prose measure" style="margin-top:var(--space-3)" data-reveal="up" data-delay="80">
          <p>%(body)s</p>
        </div>
      </div>
      <div class="c4 s9 po-fig">%(fig)s</div>
    </div>
    %(index)s
    <div style="margin-top:var(--space-4)">%(action)s</div>
  </div>
</section>""" % {
        "shead": shead(ui["nav_products"], paint=True),
        "head": esc(c["products_head"]),
        "body": esc(c["products_body"]),
        "fig": figure("guides", lang, cls="frame--port",
                      sizes="(max-width:767px) 100vw, 32vw",
                      caption=("Guidelines — Parents, Young Athletes, Fans."
                               if lang == "en" else
                               "Guide — Genitori, Giovani Atleti, Tifosi.")),
        "index": index_rows(p["items"], lang),
        "action": action(url(lang, "/products/"), p["statement"], lang, cursor=ui["view"]),
    }

    # ---- the hinge: a photograph becomes the next ground --------------------
    hinge = """
<div class="hinge on-paper" data-field="paper" aria-hidden="true">%s</div>""" % img(
        "court", lang, cls="frame--pano", sizes="100vw", counter=True)

    # ---- 04 services -------------------------------------------------------
    services = """
<section class="act-po on-paper" data-field="paper" aria-labelledby="srv-h">
  <div class="wrap">
    %(shead)s
    <div class="grid" style="margin-top:var(--space-3)">
      <div class="c4">%(fig)s</div>
      <div class="c8 s5">
        <h2 class="h2 po-head" id="srv-h" data-reveal="up">%(head)s</h2>
        <div class="prose measure" style="margin-top:var(--space-3)" data-reveal="up" data-delay="80">
          <p>%(body)s</p>
        </div>
      </div>
    </div>
    %(index)s
    <div class="grid">
      <div class="c5 s8 close-statement" data-reveal="up" data-axis="sport" role="group">
        <i class="paint paint--2 close-statement__bar" aria-hidden="true"></i>
        <p class="h3 close-statement__t">%(statement)s</p>
        <a class="meta tlink close-statement__go" href="%(href)s" data-cursor="%(view)s">%(all)s</a>
      </div>
    </div>
  </div>
</section>""" % {
        "shead": shead(ui["nav_services"]),
        "statement": esc(s["statement"]),
        "href": esc(url(lang, "/services/")),
        "view": esc(ui["view"]),
        "all": esc(ui["nav_services"]),
        "fig": figure("coach_youth", lang, cls="frame--port", sizes="(max-width:767px) 100vw, 32vw", axis="sport"),
        "head": esc(c["services_head"]),
        "body": esc(c["services_body"]),
        "index": index_rows(s["items"], lang),
    }

    # ---- 05 the axis -------------------------------------------------------
    # Their mission sentence names three words. Set as a three-line justified
    # stack, it is the same object as the logo — and the middle line is the
    # word the two stacks share.
    # Their mission names three words. Set as a three-line justified stack it
    # is the same object as the logo — and each line is underwritten by its own
    # ink, painted rather than ruled. This is the one place on the site where
    # all three appear together at full scale.
    axis_terms = ["culture", "sport", "art"]
    axis_words = [AXIS_LABEL[lang][t] for t in axis_terms]
    axis_lines = "".join(
        '<span class="hl axis__w" data-jl-host data-axis="%s">'
        '<span class="hlw%s" data-jl%s>%s</span>'
        '<i class="paint axis__paint paint--%d" aria-hidden="true"></i>'
        '</span>'
        % (t,
           " echo" if t == "art" else "",
           ' data-echo="%s"' % esc(w) if t == "art" else "",
           esc(w), (i % 3) + 1)
        for i, (t, w) in enumerate(zip(axis_terms, axis_words)))

    concept = "".join('<p class="concept-line" data-reveal="up" data-delay="%d">%s</p>'
                      % (i * 70, esc(l)) for i, l in enumerate(c["concept"]))

    axis = """
<section class="act-axis on-ink tongue tongue--right tongue--paint" data-field="ink" aria-labelledby="axis-h">
  <i class="sweep sweep--3" aria-hidden="true"
     style="top:9%%;height:clamp(58px,9vh,120px);--sweep-w:64%%;--sweep-ink:var(--nsv-culture);--sweep-o:.20;--sweep-tilt:1.1deg"></i>
  <div class="wrap">
    %(shead)s
    <div class="grid" style="margin-top:var(--space-3)">
      <div class="c8 s5">%(concept)s</div>
    </div>
    <div class="axis" data-justify-stack data-jmax="320" role="group" aria-labelledby="axis-h">
      <h2 class="visually-hidden" id="axis-h">%(axis_label)s</h2>
      %(axis_lines)s
    </div>
    <div class="grid" style="margin-top:var(--space-5)">
      <div class="c5 s8">
        <div class="prose" data-reveal="up"><p>%(articulation)s</p></div>
        <div style="margin-top:var(--space-3)">
          <a class="meta tlink" href="%(about_href)s">%(learn)s</a>
        </div>
      </div>
    </div>
  </div>
</section>""" % {
        "shead": shead(c["concept"][2].rstrip("."), paint=True),
        "concept": concept,
        "axis_label": esc(c["concept"][2]),
        "axis_lines": axis_lines,
        "articulation": esc(c["articulation"]),
        "about_href": esc(url(lang, "/about/")),
        "learn": esc(c["learn_more"]),
    }

    # ---- 06 history --------------------------------------------------------
    history = """
<section class="act-po on-paper" data-field="paper" aria-labelledby="hist-h">
  <div class="wrap">
    %(shead)s
    <div class="chapter" style="border-top:0;padding-top:var(--space-3)">
      <span class="chapter__year" aria-hidden="true">1989</span>
      <div class="chapter__body grid">
        <div class="c6">
          <h2 class="chapter__label" id="hist-h" data-reveal="up">%(label)s</h2>
          <div class="prose measure" style="margin-top:var(--space-3)" data-reveal="up" data-delay="80">
            <p>%(intro)s</p>
          </div>
          <div style="margin-top:var(--space-4)">%(action)s</div>
        </div>
        <div class="c5 s8">%(fig)s</div>
      </div>
    </div>
  </div>
</section>""" % {
        "shead": shead(ui["nav_about"], axis="sport"),
        "label": esc(a["chapters"][0]["label"]),
        "intro": esc(a["chapters"][0]["body"][0]),
        "action": action(url(lang, "/about/"),
                         "1989 — 2026" if lang == "en" else "1989 — 2026",
                         lang, cursor=ui["read"]),
        "fig": figure("basket_youth", lang, cls="frame--land",
                      sizes="(max-width:767px) 100vw, 40vw", axis="sport"),
    }

    body = hero + event + products + hinge + services + axis + history

    return page(lang, "/", c["title"], c["description"], body, active="home",
                footer_html=footer(lang, "/", c["contact_invite"], c["got_idea"]),
                og_image="basket-hoop-1600.jpg")


# ===========================================================================
# PRODUCTS / SERVICES — the wall
# ===========================================================================

# A poster wall: each item gets its own proportion. The variation is a fixed
# map, not a random one, so the page composes the same way every build.
PRODUCT_WALL = [
    # slug,               span, start, image key,      frame class,   offset
    ("guidelines",        7, 1,  "guides",      "frame--land", 0),  # the printed guides
    ("my-12-seconds",     4, 9,  "leap",        "frame--port", 1),  # one burst of effort
    ("books",             5, 1,  "desk",        "frame--sq",   0),  # writing, publishing
    ("futuresportfuture", 6, 7,  "summit_room", "frame--wide", 1),  # the summit itself
    ("3-balls",           4, 1,  "finish_line", "frame--port", 0),  # one champion
    ("camst",             5, 6,  "course_room", "frame--wide", 1),  # a master course
    ("back-to-school",    6, 7,  "school_bus",  "frame--pano", 0),  # back to school
]

SERVICE_WALL = [
    ("help-desk", 8, 1, "guide_open", "frame--wide", 0),  # a guide being consulted
    ("parents",   5, 1, "basket_youth","frame--land", 0), # the young athletes themselves
    ("nsv-pass",  4, 9, "nsvpass",    "frame--sq",   1),  # the Pass mark itself
]


def wall(items, layout, lang):
    """
    The wall. Each item takes a different share of the grid and a different
    vertical position, but every label in a row sits on the same line above a
    shared rule — the way an exhibition labels what is hanging on it.
    """
    by_slug = {slug: (name, href) for slug, name, href in items}
    out = ['<div class="wall grid">']
    for i, (slug, span, start, media, fcls, off) in enumerate(layout, 1):
        if slug not in by_slug:
            continue
        name, href = by_slug[slug]
        fig = ""
        if media:
            fig = img(media, lang, cls=fcls or "", counter=True, eager=(i == 1),
                      sizes="(max-width:767px) 100vw, %dvw" % round(span * 7.8))
        ax = AXIS.get(slug)
        out.append(
            '<a class="wall__item c%d s%d%s%s" href="%s"%s data-cursor="%s" '
            'data-reveal="up" data-delay="%d">'
            '%s'
            '<span class="wall__foot">'
            '<span class="wall__meta">'
            '<i class="tab" aria-hidden="true"></i>'
            '<span class="wall__go" aria-hidden="true"></span></span>'
            '<span class="wall__name">%s</span>'
            '</span></a>'
            % (span, start,
               " wall__item--drop" if off else "",
               " wall__item--type" if not media else "",
               esc(url(lang, href)),
               ' data-axis="%s"' % ax if ax else '',
               esc(UI[lang]["view"]), (i - 1) * 60,
               fig, esc(name))
        )
    out.append("</div>")
    return "".join(out)


def statement_page(lang, data, layout, kicker, active, path, og, sweep="art"):
    ui = UI[lang]
    lines = lb.auto(data["statement"])

    body = """
<section class="page-head on-paper" data-field="paper" style="position:relative;overflow:clip">
  <i class="sweep sweep--2" aria-hidden="true"
     style="top:47%%;height:clamp(64px,10vh,132px);--sweep-w:86%%;--sweep-ink:var(--sweep-page,var(--nsv-art));--sweep-o:.15"></i>
  <div class="wrap">
    <div class="kicker">
      <span class="paint paint--thin" aria-hidden="true" style="flex:1 1 auto"></span>
      <span class="meta">%(kicker)s</span></div>
    %(statement)s
  </div>
</section>
<section class="on-paper" data-field="paper" style="padding-bottom:var(--act);position:relative">
  <span class="crop crop--tr" aria-hidden="true"></span>
  <div class="wrap">%(wall)s</div>
  <span class="crop crop--bl" aria-hidden="true"></span>
</section>""" % {
        "rule": rule(),
        "kicker": esc(kicker),
        "statement": jstack(lines, tag="h1", cls="statement-stack", jmax="190"),
        "wall": wall(data["items"], layout, lang),
    }
    return page(lang, path, data["title"],
                data["statement"], body, active=active,
                body_class="sweep-" + sweep,
                footer_html=footer(lang, path, HOME[lang]["contact_invite"], HOME[lang]["got_idea"]),
                og_image=og)


def products(lang):
    return statement_page(lang, PRODUCTS_INDEX[lang], PRODUCT_WALL,
                          UI[lang]["nav_products"], "products", "/products/",
                          "guides-three-1600.jpg", sweep="art")


def services(lang):
    return statement_page(lang, SERVICES_INDEX[lang], SERVICE_WALL,
                          UI[lang]["nav_services"], "services", "/services/",
                          "court-lines-1600.jpg", sweep="sport")


# ===========================================================================
# ABOUT — the history, as an exhibition
# ===========================================================================

CHAPTER_MEDIA = [
    ("basket_youth", "frame--land"),  # the first private basketball school
    ("coach_youth",  "frame--wide"),  # youth development, players aged 12–15
    ("basket_hoop",  "frame--land"),  # FIBA, and the European Championships
    ("summit_room",  "frame--sq"),    # the International Summit, Milano 2014
]
# Each chapter sits in a different part of the grid, and the field flips at the
# point the story leaves Yugoslavia. Nothing alternates on a fixed beat.
CHAPTER_GRID = [
    ("c5 s1", "c6 s7",  "on-paper", "paper"),
    ("c5 s4", "c5 s1",  "on-paper", "paper"),
    ("c6 s6", "c5 s1",  "on-ink",   "ink"),
    ("c6 s1", "c5 s8",  "on-ink",   "ink"),
]


def about(lang):
    a = ABOUT[lang]
    ui = UI[lang]

    head = """
<section class="page-head on-paper" data-field="paper">
  <div class="wrap">
    <div class="kicker">%(rule)s<span class="meta">%(kicker)s</span></div>
    <div class="grid about-head">
      <div class="c7">%(title)s</div>
      <div class="c4 s9 about-head__intro">%(intro)s</div>
    </div>
  </div>
</section>""" % {
        "rule": rule(),
        "kicker": esc(ui["nav_about"]),
        # The identity at page scale: the same three-line justified block the
        # logo is — set to seven columns, which is the measure that lets the
        # three lines fill without the tracking having to do the work.
        "title": ('<h1 class="jstack about-mast" data-justify-stack>'
                  '<span class="hl hl--rule" data-jl-host>'
                  '<span class="jline__t" data-jl data-jl-rule>New</span>'
                  '<i class="jline__rule"></i></span>'
                  '<span class="hl" data-jl-host><span class="hlw" data-jl>Sport</span></span>'
                  '<span class="hl" data-jl-host><span class="hlw" data-jl>Vision</span></span>'
                  '</h1>'),
        "intro": paras(a["intro"], cls="prose"),
    }

    chapters = []
    for i, ch in enumerate(a["chapters"]):
        tcls, icls, field_cls, field = CHAPTER_GRID[i]
        mkey, fcls = CHAPTER_MEDIA[i]
        cax = CHAPTER_AXIS[i]
        # The ghost year belongs behind its own paragraph, not across the
        # neighbouring column — so it starts where the text column starts.
        col_start = int(tcls.split("s")[-1]) - 1
        body_html = paras(ch["body"])
        if i == 2:
            body_html = body_html.replace(
                "www.bambasketballmovementhistory.com",
                '<a class="tlink" href="%s" target="_blank" rel="noopener">'
                'www.bambasketballmovementhistory.com</a>' % esc(SITE["bam_url"]))
            body_html = body_html.replace(
                "www.bambasketballmovementishtory.com",
                '<a class="tlink" href="%s" target="_blank" rel="noopener">'
                'www.bambasketballmovementishtory.com</a>' % esc(SITE["bam_url"]))
        chapters.append("""
<section class="%(field_cls)s" data-field="%(field)s" data-axis="%(cax)s">
  <div class="wrap">
    <article class="chapter">
      <span class="chapter__year" aria-hidden="true"
            style="left:calc((var(--col) + var(--gutter)) * %(colstart)d)">%(year)s</span>
      <div class="chapter__body grid">
        <div class="%(tcls)s">
          <p class="chapter__tag"><i class="tab" aria-hidden="true"></i></p>
          <h2 class="chapter__label" data-reveal="up">%(label)s</h2>
          <div style="margin-top:var(--space-3)" data-reveal="up" data-delay="80">%(body)s</div>
        </div>
        <div class="%(icls)s" style="align-self:end">%(fig)s</div>
      </div>
    </article>
  </div>
</section>""" % {
            "field_cls": field_cls, "field": field, "cax": cax,
            "colstart": col_start,
            "year": esc(ch["year"]), "tcls": tcls, "icls": icls,
            "label": esc(ch["label"]),
            "body": body_html,
            "fig": figure(mkey, lang, cls=fcls, sizes="(max-width:767px) 100vw, 47vw",
                          axis=cax),
        })

    body = head + "".join(chapters)
    return page(lang, "/about/", a["title"],
                a["intro"][0], body, active="about",
                footer_html=footer(lang, "/about/", HOME[lang]["contact_invite"],
                                   HOME[lang]["got_idea"]),
                og_image="basket-youth-1600.jpg")


# ===========================================================================
# Editorial pages — Guidelines, Books, Workshops
# ===========================================================================

def editorial(lang, data, path, kicker, media, pull_index, og, active=None,
              eyebrow=None, axis=None):
    ui = UI[lang]
    b = data["body"]
    standfirst = b[0]
    rest = b[1:]

    # One sentence from their own copy is given a wall to itself.
    pull = rest[pull_index] if 0 <= pull_index < len(rest) else None
    if pull:
        rest = rest[:pull_index] + rest[pull_index + 1:]

    mid = max(1, len(rest) // 2)
    col_a, col_b = rest[:mid], rest[mid:]

    eyebrow_html = ('<p class="annot" style="margin-bottom:var(--space-1)">%s</p>' % esc(eyebrow)) if eyebrow else ""

    body = """
<section class="page-head on-paper" data-field="paper">
  <div class="wrap">
    <div class="kicker">%(rule)s<span class="meta">%(kicker)s</span></div>
    %(eyebrow)s
    %(title)s
    <div class="grid" style="margin-top:var(--space-4)">
      <div class="c7 s6"><p class="lead">%(standfirst)s</p></div>
    </div>
  </div>
</section>
<section class="editorial on-paper" data-field="paper">
  <div class="wrap">
    <div style="margin-top:var(--space-4)">%(fig)s</div>
    %(pull)s
    <div class="grid">
      <div class="c5 s2">%(col_a)s</div>
      <div class="c4 s8">%(col_b)s</div>
    </div>
    <div class="editorial-end">
      <span class="meta meta--quiet">%(contact_label)s</span>
      <a class="mailto-big tlink" href="mailto:%(email)s" data-cursor="%(open)s">%(email)s</a>
    </div>
  </div>
</section>""" % {
        "rule": rule(),
        "kicker": esc(kicker),
        "eyebrow": eyebrow_html,
        "contact_label": esc(UI[lang]["contact_line"]),
        "email": esc(SITE["email"]),
        "open": esc(UI[lang]["open"]),
        "title": jstack(lb.auto(data["head"]), tag="h1", cls="statement-stack", jmax="200"),
        "standfirst": esc(standfirst),
        "fig": figure(media[0], lang, cls=media[1], sizes="100vw", axis=axis),
        "pull": ('<p class="pull" data-reveal="up"%s>%s</p>'
                 % (' data-axis="%s"' % axis if axis else '', esc(pull))) if pull else "",
        "col_a": paras(col_a),
        "col_b": paras(col_b),
    }
    return page(lang, path, data["title"], standfirst, body,
                active=active, body_class=("axis-" + axis) if axis else "",
                footer_html=footer(lang, path, HOME[lang]["contact_invite"], HOME[lang]["got_idea"]),
                og_image=og)


def guidelines(lang):
    return editorial(lang, GUIDELINES[lang], "/guidelines/", UI[lang]["nav_products"],
                     ("guides", "frame--pano"), 2,
                     "guides-three-1600.jpg", active="products", axis="art")


def books(lang):
    return editorial(lang, BOOKS[lang], "/books/", UI[lang]["nav_products"],
                     ("desk", "frame--wide"), 1,
                     "desk-editorial-1600.jpg", active="products",
                     eyebrow=BOOKS[lang].get("eyebrow"), axis="culture")


def workshops(lang):
    return editorial(lang, WORKSHOPS[lang], "/workshops/", UI[lang]["nav_more"],
                     ("skate", "frame--wide"), 5,
                     "skate-architecture-1600.jpg", active="workshops", axis="culture")


# ===========================================================================
# WORK IN PROGRESS
# ===========================================================================

def work_in_progress(lang):
    w = WORK_IN_PROGRESS[lang]
    lines = "".join('<span class="hl wip__l" data-jl-host><span class="hlw" data-jl>%s</span></span>'
                    % esc(seg) for l in w["lines"] for seg in lb.auto(l))
    body = """
<section class="wip on-yellow" data-field="yellow">
  <div class="wrap">
    <div class="kicker" style="display:flex;align-items:baseline;gap:var(--space-2)">
      <span class="idx">%(date)s</span>%(rule)s
    </div>
    <h1 class="wip__lines" data-justify-stack data-jmax="150" style="margin-top:var(--space-3)">%(lines)s</h1>
    <div style="margin-top:var(--space-5)">%(action)s</div>
  </div>
</section>""" % {
        "date": esc(w["date"]), "rule": rule(),
        "lines": lines,
        "action": action(url(lang, "/"), UI[lang]["nav_home"], lang, cursor=UI[lang]["view"]),
    }
    return page(lang, "/work-in-progress/", w["title"], w["lines"][0], body,
                footer_html=footer(lang, "/work-in-progress/", HOME[lang]["contact_invite"],
                                   HOME[lang]["got_idea"]))


# ===========================================================================
# HELP DESK — news, and the instrument itself
# ===========================================================================

def helpdesk_news(lang):
    d = HELPDESK_NEWS[lang]
    body = """
<section class="page-head on-paper" data-field="paper">
  <div class="wrap">
    <div class="kicker">%(rule)s<span class="meta">%(kicker)s</span></div>
    %(title)s
    <div class="grid" style="margin-top:var(--space-4)">
      <div class="c7 s6"><p class="lead">%(a)s</p>
      <p class="h3" style="margin-top:var(--space-3)">%(b)s</p></div>
    </div>
    <div style="margin-top:var(--space-5)">%(fig)s</div>
    <div style="margin-top:var(--space-5)">%(action)s</div>
  </div>
</section>""" % {
        "rule": rule(), "kicker": esc(UI[lang]["nav_services"]),
        "title": jstack(lb.auto(d["head"]), tag="h1", cls="statement-stack", jmax="200"),
        "a": esc(d["body"][0]), "b": esc(d["body"][1]),
        "fig": figure("guides", lang, cls="frame--pano", sizes="100vw", axis="art"),
        "action": action(url(lang, "/help-desk/"), UI[lang]["nav_more"] if False else "Help Desk",
                         lang, cursor=UI[lang]["open"]),
    }
    return page(lang, "/help-desk/news/", d["title"], d["body"][0], body, active="services",
                footer_html=footer(lang, "/help-desk/news/", HOME[lang]["contact_invite"],
                                   HOME[lang]["got_idea"]),
                og_image="guides-three-1600.jpg")


def helpdesk(lang):
    h = HELPDESK[lang]
    ui = UI[lang]

    def opts(items, group):
        out = ['<div class="opts" role="group">']
        for i, (val, label) in enumerate(items, 1):
            out.append(
                '<button type="button" class="opt" data-group="%s" data-value="%s" aria-pressed="false">'
                '<span class="idx">%02d</span>'
                '<span class="opt__name">%s</span>'
                '<span class="opt__go" aria-hidden="true"></span></button>'
                % (esc(group), esc(val), i, esc(label)))
        out.append("</div>")
        return "".join(out)

    sport_qs = "".join(
        '<button type="button" class="opt" data-group="sport" data-value="advice-%d" aria-pressed="false">'
        '<span class="idx">%s</span><span class="opt__name">%s</span>'
        '<span class="opt__go" aria-hidden="true"></span></button>'
        % (i, "?", esc(q)) for i, q in enumerate(h["sport_q"], 1))

    topics = h["topics"] + [h["topic_other_extra"]]

    body = """
<section class="page-head on-paper" data-field="paper">
  <div class="wrap">
    <div class="kicker" data-axis="sport">
      <i class="tab" aria-hidden="true"></i>%(rule)s<span class="meta">%(kicker)s</span></div>
    <p class="annot" style="margin-bottom:var(--space-1)">%(eyebrow)s</p>
    %(title)s
  </div>
</section>

<section class="hd on-paper" data-field="paper">
  <div class="wrap">
    <nav class="hd-steps" aria-label="%(steps_label)s">
      <span class="hd-step meta" data-step="1" data-state="active">
        <span class="hd-step__n">01</span><span class="hd-step__v" data-slot="who">%(step1)s</span></span>
      <span class="hd-step meta" data-step="2">
        <span class="hd-step__n">02</span><span class="hd-step__v" data-slot="sport">%(step2)s</span></span>
      <span class="hd-step meta" data-step="3">
        <span class="hd-step__n">03</span><span class="hd-step__v" data-slot="topic">%(step3)s</span></span>
    </nav>

    <div class="grid">
      <div class="c7">
        <div class="hd-panel" data-panel="1">
          <h2 class="h3 hd-q"><span class="hd-q__lead">%(intro_a)s</span> %(intro_b)s</h2>
          %(who)s
        </div>

        <div class="hd-panel" data-panel="2" hidden>
          <h2 class="h3 hd-q">%(step2)s</h2>
          %(sports)s
          <div class="opts" style="margin-top:var(--space-3);border-top:0">%(sport_qs)s</div>
          <button type="button" class="hd-back meta" data-back="1"><i aria-hidden="true"></i>%(back)s</button>
        </div>

        <div class="hd-panel" data-panel="3" hidden>
          <h2 class="h3 hd-q">%(step3)s</h2>
          %(topics)s
          <div data-org-topics hidden>%(org)s</div>
          <button type="button" class="hd-back meta" data-back="2"><i aria-hidden="true"></i>%(back)s</button>
        </div>

        <div class="hd-panel" data-panel="4" hidden>
          <h2 class="h3 hd-q">%(form_head)s</h2>
          <p class="hd-summary meta" data-summary></p>
          <form class="hd-form" method="post" action="mailto:%(email)s" enctype="text/plain"
                data-hd-form data-sent="%(f_sent)s" novalidate>
            <div class="field-row">
              <p class="field"><label class="meta" for="hd-name">%(f_name)s</label>
                 <input id="hd-name" name="name" type="text" autocomplete="given-name" required></p>
              <p class="field"><label class="meta" for="hd-surname">%(f_surname)s</label>
                 <input id="hd-surname" name="surname" type="text" autocomplete="family-name"></p>
            </div>
            <div class="field-row">
              <p class="field"><label class="meta" for="hd-email">%(f_email)s</label>
                 <input id="hd-email" name="email" type="email" autocomplete="email" required></p>
              <p class="field"><label class="meta" for="hd-phone">%(f_phone)s</label>
                 <input id="hd-phone" name="phone" type="tel" autocomplete="tel"></p>
            </div>
            <p class="field"><label class="meta" for="hd-ins">%(f_insurance)s</label>
              <select id="hd-ins" name="insurance">
                <option value="">%(f_choose)s</option>
                <option value="si">Sì</option>
                <option value="no">No</option>
              </select></p>
            <p class="field"><label class="meta" for="hd-msg">%(f_message)s</label>
               <textarea id="hd-msg" name="message"></textarea></p>
            <p class="check"><input id="hd-terms" name="terms" type="checkbox" required>
               <label for="hd-terms">%(f_terms)s —
                 <a class="tlink" href="%(privacy)s">%(privacy_label)s</a></label></p>
            <p class="field"><button type="submit" class="action" style="border:0;padding:0">
              <span class="action__label">%(f_send)s</span>
              <span class="action__arrow" aria-hidden="true"></span></button></p>
            <p class="annot" data-hd-status role="status" aria-live="polite"></p>
          </form>
          <button type="button" class="hd-back meta" data-back="3"><i aria-hidden="true"></i>%(back)s</button>
        </div>
      </div>

      <aside class="c4 s9">
        <div>%(fig)s</div>
        <p style="margin-top:var(--space-3)">
          <a class="meta tlink" href="%(news)s">%(news_label)s</a></p>
      </aside>
    </div>
  </div>
</section>""" % {
        "rule": rule(), "kicker": esc(ui["nav_services"]),
        "eyebrow": esc(h["eyebrow"]),
        "title": jstack(lb.auto(h["head"]), tag="h1", cls="statement-stack", jmax="180"),
        "intro_a": esc(h["intro_a"]), "intro_b": esc(h["intro_b"]),
        "steps_label": esc(h["head"]),
        "step1": esc(h["step1"]), "step2": esc(h["step2"]), "step3": esc(h["step3"]),
        "who": opts(h["audiences"], "who"),
        "sports": opts(h["sports"], "sport"),
        "sport_qs": sport_qs,
        "topics": opts(topics, "topic"),
        "org": opts(h["org_topics"], "topic"),
        "back": esc(ui["back"]),
        "form_head": esc(h["form_head"]),
        "email": esc(SITE["email"]),
        "f_name": esc(h["f_name"]), "f_surname": esc(h["f_surname"]),
        "f_email": esc(h["f_email"]), "f_phone": esc(h["f_phone"]),
        "f_insurance": esc(h["f_insurance"]), "f_choose": esc(h["f_choose"]),
        "f_message": esc(h["f_message"]), "f_terms": esc(h["f_terms"]),
        "f_send": esc(h["f_send"]),
        "f_sent": esc(h["f_sent"]),
        "privacy": esc(url(lang, "/privacy/")), "privacy_label": esc(ui["privacy"]),
        "fig": figure("guide_open", lang, cls="frame--port", sizes="(max-width:767px) 100vw, 30vw",
                      num="Fig. 01", caption=None),
        "news": esc(url(lang, "/help-desk/news/")),
        "news_label": esc(HELPDESK_NEWS[lang]["body"][1]),
    }

    return page(lang, "/help-desk/", h["title"], h["intro_a"], body, active="help-desk",
                footer_html=footer(lang, "/help-desk/", HOME[lang]["contact_invite"],
                                   HOME[lang]["got_idea"]),
                og_image="court-lines-1600.jpg")


# ===========================================================================
# PRIVACY
# ===========================================================================

def privacy(lang):
    ui = UI[lang]
    toc = "".join('<li><a class="meta" href="#%s">%s</a></li>' % (esc(sid), esc(title))
                  for sid, title, _ in PRIVACY_SECTIONS)
    secs = []
    for sid, title, paras_ in PRIVACY_SECTIONS:
        block = []
        for p in paras_:
            if p.lstrip().startswith("<ul>"):
                block.append(p)
            else:
                block.append("<p>%s</p>" % p if ("<em>" in p or "<a " in p) else "<p>%s</p>" % esc(p))
        secs.append('<h2 id="%s">%s</h2>%s' % (esc(sid), esc(title), "".join(block)))

    body = """
<section class="page-head on-paper" data-field="paper">
  <div class="wrap">
    <div class="kicker">%(rule)s<span class="meta">%(kicker)s</span></div>
    <h1 class="h1" style="max-width:20ch">%(head)s</h1>
  </div>
</section>
<section class="legal on-paper" data-field="paper">
  <div class="wrap grid">
    <nav class="legal-toc c3" aria-label="%(toc_label)s">
      <p class="meta meta--quiet" style="margin-bottom:var(--space-1)">%(toc_label)s</p>
      <ol>%(toc)s</ol>
    </nav>
    <div class="legal-body c7 s5">
      %(lead)s
      %(secs)s
      <p class="meta meta--quiet" style="margin-top:var(--space-5)">%(entity)s · %(addr)s · %(vat)s</p>
    </div>
  </div>
</section>""" % {
        "rule": rule(), "kicker": esc(ui["privacy"]),
        "head": esc(PRIVACY_HEAD),
        "toc_label": esc(ui["in_this_page"]),
        "toc": toc,
        "lead": "".join('<p class="lead" style="margin-bottom:1em">%s</p>' % esc(p) for p in PRIVACY_LEAD),
        "secs": "".join(secs),
        "entity": esc(SITE["entity"]), "addr": esc(SITE["entity_address"]),
        "vat": esc(SITE["entity_vat"]),
    }
    return page(lang, "/privacy/", PRIVACY_TITLE, PRIVACY_LEAD[0][:180], body,
                footer_html=footer(lang, "/privacy/", HOME[lang]["contact_invite"],
                                   HOME[lang]["got_idea"]))


# ===========================================================================
# 404
# ===========================================================================

def not_found(lang):
    ui = UI[lang]
    # Two lines, not three: a three-letter "NOT" cannot be set to the width of
    # "FOUND" without tearing it apart.
    txt = {"en": ["PAGE NOT", "FOUND"], "it": ["PAGINA NON", "TROVATA"]}[lang]
    lines = "".join('<span class="hl wip__l" data-jl-host><span class="hlw" data-jl>%s</span></span>'
                    % esc(l) for l in txt)
    body = """
<section class="nf on-ink" data-field="ink">
  <div class="wrap">
    <div class="kicker" style="display:flex;align-items:baseline;gap:var(--space-2)">
      <span class="idx">404</span>%(rule)s
    </div>
    <h1 class="wip__lines" data-justify-stack data-jmax="150" style="margin-top:var(--space-3)">%(lines)s</h1>
    <div style="margin-top:var(--space-5)">%(action)s</div>
  </div>
</section>""" % {"rule": rule(), "lines": lines,
                 "action": action(url(lang, "/"), ui["nav_home"], lang, cursor=ui["view"])}
    # An error page is served at whatever URL was missed, so it carries no
    # canonical of its own and its language switch goes to the other home.
    return page(lang, "/", "404 | newsportvision", "Page not found", body, noindex=True,
                footer_html=footer(lang, "/", HOME[lang]["contact_invite"], HOME[lang]["got_idea"]))
