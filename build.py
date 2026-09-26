#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEWSPORTVISION — static build.

    python3 build.py           build into ./dist   (Netlify / any host)
    python3 build.py --vercel  build into ./dist and write ./vercel.json
    python3 build.py --serve   build, then serve ./dist on :8080

No Node, no package manager, no build dependencies beyond the standard library.
Output is plain static HTML: every word is in the markup, so the site needs no
JavaScript to be read, indexed, or navigated.
"""

import os, shutil, sys, json, base64, hashlib, http.server, socketserver, functools

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))

from content import SITE, LANGS, REDIRECTS          # noqa: E402
from render import url                              # noqa: E402
import pages                                        # noqa: E402
import arms                                         # noqa: E402

DIST = os.path.join(HERE, "dist")
STATIC = os.path.join(HERE, "static")

# route -> builder
ROUTES = [
    ("/",                  pages.home),
    ("/products/",         pages.products),
    ("/services/",         pages.services),
    ("/about/",            pages.about),
    ("/guidelines/",       pages.guidelines),
    ("/books/",            pages.books),
    ("/workshops/",        pages.workshops),
    ("/help-desk/",        pages.helpdesk),
    ("/help-desk/news/",   pages.helpdesk_news),
    ("/work-in-progress/", pages.work_in_progress),
    ("/privacy/",          pages.privacy),
]

# Pages that exist once, in their own language. A.R.M.S. is a Serbian
# association: a translated copy of it under /it/ would be a second URL saying
# the same thing in a language neither of its readers asked for, and the host's
# hreflang pairs would start claiming two pages are the same page.
SINGLE = [
    ("/arms/", arms.arms),
]


def write(rel, text):
    path = os.path.join(DIST, rel.lstrip("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def redirect_stub(target):
    """A portable redirect that works on any static host, including file://."""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<title>Redirecting…</title>'
        '<link rel="canonical" href="%s%s">'
        '<meta http-equiv="refresh" content="0;url=%s">'
        '<meta name="robots" content="noindex">'
        '<script>location.replace("%s"+location.search+location.hash);</script>'
        '</head><body style="font:14px system-ui;padding:2rem">'
        'Redirecting to <a href="%s">%s</a>.</body></html>'
        % (SITE["domain"], target, target, target.split("?")[0], target, target)
    )


def vercel_json(redirects, secure, immutable, revalidate):
    """Everything dist/_redirects and dist/_headers say, in Vercel's dialect.

    Vercel answers a request in a fixed order: redirects, then headers, then
    the filesystem, then rewrites, then the 404. Three consequences shape the
    file below.

      * The legacy Wix URLs are redirects, answered at the edge — the HTML
        stubs a dumber host needs are never built. Measured against the live
        deployment: trailingSlash normalisation runs BEFORE these rules, so a
        bare /shop is answered 308 -> /shop/ and only then 301 -> /products/.
        Both spellings are listed because the slashed one is what the rules
        actually receive; the bare one costs nothing and covers the case where
        that order ever changes.
      * Every rule below is written so that no two rules can set the same
        header on the same request. A header set twice is joined with a comma,
        and "max-age=0, max-age=31536000" would quietly stop the assets from
        being cached at all.
      * There is no rewrite for the Italian tree. One was tried: Vercel serves
        the root 404.html for every unmatched path and the rewrite never fired,
        so an unknown /it/ URL answers 404 with the English page. That is the
        better half of the trade — a rewrite would have returned 200, and a
        wrong status on an error page costs more than a wrong language on a
        page that carries noindex.
    """
    rules = []
    for src, dst in sorted(redirects.items()):
        # Both spellings, so a legacy link lands in one hop whichever way the
        # trailing slash falls, instead of 301 -> 308 -> page.
        for source in (src.rstrip("/"), src.rstrip("/") + "/"):
            # 301, spelled out: Vercel's own "permanent" flag means 308, and
            # these legacy links have been answered with 301 for years.
            rules.append({"source": source, "destination": dst, "statusCode": 301})

    html = ([url(lang, path) for path, _ in ROUTES for lang in LANGS]
            + [path for path, _ in SINGLE])
    cfg = {
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "framework": None,
        "installCommand": "",          # nothing to install: the standard library
        "buildCommand": "python3 build.py --vercel",
        "outputDirectory": "dist",
        "trailingSlash": True,         # the canonical URLs all end in one
        "cleanUrls": False,            # every page is already a directory index
        "redirects": rules,
        "headers": [
            {"source": "/(.*)",
             "headers": [{"key": k, "value": v} for k, v in secure]},
            {"source": "/assets/(.*)",
             "headers": [{"key": "Cache-Control", "value": immutable}]},
            {"source": "/assets/fonts/(.*)",
             "headers": [{"key": "Access-Control-Allow-Origin", "value": "*"}]},
        ] + [{"source": h,
              "headers": [{"key": "Cache-Control", "value": revalidate}]} for h in html],
    }
    with open(os.path.join(HERE, "vercel.json"), "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")

    with open(os.path.join(HERE, ".vercelignore"), "w", encoding="utf-8") as f:
        f.write("# Uploaded to Vercel: the sources the build needs, nothing else.\n"
                "__pycache__/\n*.pyc\n.DS_Store\ntools/\n*.zip\nnetlify.toml\n")


def write_help_desk_options():
    """The Help Desk endpoint checks every answer against the lists the buttons
    are drawn from. Those lists live in content.py; this writes them where the
    Vercel Function can import them, so there is one list and not two. The
    English labels are the ones the office reads in the email."""
    from content import HELPDESK
    h = HELPDESK["en"]
    for lang in HELPDESK:
        other = HELPDESK[lang]
        same = ([v for v, _ in other["audiences"]] == [v for v, _ in h["audiences"]] and
                [v for v, _ in other["sports"]] == [v for v, _ in h["sports"]] and
                [v for v, _ in other["topics"]] == [v for v, _ in h["topics"]] and
                [v for v, _ in other["org_topics"]] == [v for v, _ in h["org_topics"]])
        assert same, "Help Desk values differ between languages (%s)" % lang

    def table(pairs):
        return dict((value, label) for value, label in pairs)

    sport = table(h["sports"])
    # the two "which sport suits me / my child?" questions are answers too
    for i, question in enumerate(h["sport_q"], 1):
        sport["advice-%d" % i] = question
    person = h["audiences"][0][0]
    assert person == "person", "the first audience is the individual"

    parts = [
        ("WHO", table(h["audiences"])),
        ("SPORT", sport),
        ("TOPIC_PERSON", table(h["topics"] + [h["topic_other_extra"]])),
        ("TOPIC_ORG", table(h["org_topics"])),
        # the two answers the form's own select offers (pages.helpdesk)
        ("INSURANCE", {"si": "Yes", "no": "No"}),
    ]
    out = ["// Generated by build.py from src/content.py. Edit the content, not this file.\n",
           'export const PERSON = %s;\n' % json.dumps(person)]
    for name, data in parts:
        out.append("export const %s = Object.freeze(%s);\n"
                   % (name, json.dumps(data, ensure_ascii=False, indent=2)))
    path = os.path.join(HERE, "lib", "help-desk-options.mjs")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = "".join(out)
    if not os.path.exists(path) or io_read(path) != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)


def io_read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def build(host="netlify"):
    """host: "netlify" writes _redirects/_headers/stubs; "vercel" writes
    vercel.json at the project root instead, and leaves dist/ free of the
    files that only another host would read."""
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    write_help_desk_options()

    # --- assets -----------------------------------------------------------
    shutil.copytree(STATIC, os.path.join(DIST, "assets"))

    # --- pages ------------------------------------------------------------
    count = 0
    real_pages = set()
    for path, fn in ROUTES:
        for lang in LANGS:
            out = url(lang, path).lstrip("/")
            rel = os.path.join(out, "index.html") if out else "index.html"
            write(rel, fn(lang))
            real_pages.add(rel)
            count += 1

    # 404 — English at the root, Italian under /it/
    write("404.html", pages.not_found("en"))
    write("it/404.html", pages.not_found("it"))
    count += 2

    for path, fn in SINGLE:
        rel = os.path.join(path.strip("/"), "index.html")
        write(rel, fn())
        real_pages.add(rel)
        count += 1

    # --- redirects --------------------------------------------------------
    # Every legacy Wix URL, in both locales, in three portable forms.
    redirects = {}
    for src, dst in REDIRECTS.items():
        redirects[src] = dst
        redirects["/it" + src] = "/it" + dst
    for src, dst in sorted(redirects.items()):
        rel = src.strip("/")
        if "?" in rel:
            rel = rel.split("?")[0]
        at = os.path.join(rel, "index.html")
        # A redirect must never be written on top of a real page.
        if at in real_pages:
            raise SystemExit("redirect %s would overwrite the page at %s" % (src, at))
        # Vercel answers every one of these from the edge, before it ever looks
        # at the filesystem, so the stub would be 114 files nothing can reach.
        if host != "vercel":
            write(at, redirect_stub(dst))

    if host != "vercel":
        with open(os.path.join(DIST, "_redirects"), "w", encoding="utf-8") as f:
            f.write("# NEWSPORTVISION — legacy Wix routes.\n"
                    "# Every URL the old site answered still answers here.\n")
            for src, dst in sorted(redirects.items()):
                # "301!" forces the rule ahead of the HTML stub that sits at the
                # same path for hosts that have no redirect engine.
                f.write("%-52s %-42s 301!\n" % (src, dst))
            f.write("\n# Italian 404s resolve inside the Italian tree.\n")
            f.write("%-52s %-42s 404\n" % ("/it/*", "/it/404.html"))
            f.write("%-52s %-42s 404\n" % ("/*", "/404.html"))

        with open(os.path.join(DIST, ".htaccess"), "w", encoding="utf-8") as f:
            f.write("Options -MultiViews\nErrorDocument 404 /404.html\n\n"
                    "<IfModule mod_rewrite.c>\nRewriteEngine On\n")
            for src, dst in sorted(redirects.items()):
                f.write('RewriteRule "^%s/?$" "%s" [R=301,L,QSA]\n' % (src.strip("/"), dst))
            f.write("</IfModule>\n")

    # --- headers ----------------------------------------------------------
    # The same set for every host; each one is handed it in its own dialect.
    # Netlify reads dist/_headers, so a drag-and-drop deploy carries them too;
    # Vercel reads vercel.json at the project root.
    #
    # The one inline script on every page is pinned by hash rather than opened
    # up with 'unsafe-inline', so no other inline script can ever run.
    from render import INLINE_BOOT
    digest = base64.b64encode(hashlib.sha256(INLINE_BOOT.encode()).digest()).decode()
    csp = ("default-src 'self'; "
           "img-src 'self' data:; "
           "font-src 'self'; "
           # style attributes carry the grid and the painted fields
           "style-src 'self' 'unsafe-inline'; "
           "script-src 'self' 'sha256-%s'; "
           "form-action 'self' mailto:; "
           "base-uri 'self'; "
           "frame-ancestors 'self'; "
           "object-src 'none'") % digest
    secure = (("X-Content-Type-Options", "nosniff"),
              ("X-Frame-Options", "SAMEORIGIN"),
              ("Referrer-Policy", "strict-origin-when-cross-origin"),
              ("Permissions-Policy",
               "camera=(), microphone=(), geolocation=(), interest-cohort=()"),
              ("Content-Security-Policy", csp))
    IMMUTABLE = "public, max-age=31536000, immutable"
    REVALIDATE = "public, max-age=0, must-revalidate"

    if host != "vercel":
        with open(os.path.join(DIST, "_headers"), "w", encoding="utf-8") as f:
            f.write("/*\n")
            for k, v in secure:
                f.write("  %s: %s\n" % (k, v))
            # Fingerprinted and immutable: cache hard.
            f.write("\n/assets/*\n  Cache-Control: %s\n" % IMMUTABLE)
            f.write("\n/assets/fonts/*\n"
                    "  Cache-Control: %s\n"
                    "  Access-Control-Allow-Origin: *\n" % IMMUTABLE)
            # HTML never: a deploy must be visible to a returning visitor at once.
            f.write("\n/*.html\n  Cache-Control: %s\n" % REVALIDATE)
            f.write("\n/\n  Cache-Control: %s\n" % REVALIDATE)
    else:
        vercel_json(redirects, secure, IMMUTABLE, REVALIDATE)

    # --- sitemap / robots -------------------------------------------------
    urls = []
    for path, _ in ROUTES:
        for lang in LANGS:
            urls.append(SITE["domain"] + url(lang, path))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
          'xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path, _ in ROUTES:
        for lang in LANGS:
            sm.append("<url><loc>%s%s</loc>" % (SITE["domain"], url(lang, path)))
            for alt in LANGS:
                sm.append('<xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>'
                          % (alt, SITE["domain"], url(alt, path)))
            sm.append('<xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>'
                      % (SITE["domain"], url("en", path)))
            sm.append("<changefreq>monthly</changefreq></url>")
    for path, _ in SINGLE:
        sm.append("<url><loc>%s%s</loc><changefreq>monthly</changefreq></url>"
                  % (SITE["domain"], path))
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["domain"])

    print("built %d pages + %d redirects -> dist/  [%s]" % (count, len(redirects), host))
    return count


def relativise():
    """Rewrite dist/ to relative URLs, for hosts that serve a bare folder."""
    sys.path.insert(0, os.path.join(HERE, "src"))
    import relativise
    # redirect stubs are server behaviour; a bare folder has none, and 114 of
    # them would swamp a file-count limit for nothing.
    for src in list(REDIRECTS) + ["/it" + r for r in REDIRECTS]:
        stub = os.path.join(DIST, src.strip("/").split("?")[0], "index.html")
        if os.path.exists(stub) and "Redirecting" in open(stub, encoding="utf-8").read():
            os.remove(stub)
            try:
                os.removedirs(os.path.dirname(stub))
            except OSError:
                pass
    h, c = relativise.run(DIST, [r for r, _ in ROUTES] + [r for r, _ in SINGLE])
    print("relativised %d pages and %d stylesheets" % (h, c))


def serve(port=8080):
    http.server.SimpleHTTPRequestHandler.extensions_map.update(
        {".avif": "image/avif", ".webp": "image/webp", ".woff2": "font/woff2"})
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIST)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print("serving dist/ on http://127.0.0.1:%d" % port)
        httpd.serve_forever()


if __name__ == "__main__":
    build("vercel" if "--vercel" in sys.argv else "netlify")
    if "--relative" in sys.argv:
        relativise()
    if "--serve" in sys.argv:
        serve(int(sys.argv[sys.argv.index("--serve") + 1]) if len(sys.argv) > sys.argv.index("--serve") + 1 and sys.argv[sys.argv.index("--serve") + 1].isdigit() else 8080)
