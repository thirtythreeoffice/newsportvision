# -*- coding: utf-8 -*-
"""
Rewrite the built site to relative URLs.

Some hosts (a preview/artifact host among them) serve a folder of files with
no server in front of it: root-relative paths like /assets/app.css are never
resolved. This pass converts every internal reference to a path relative to
the file that makes it, so the same build works with or without a server.
Absolute URLs, mailto:, anchors and metadata are left alone.
"""
import os, re

PAGE_ROUTES = set()


def depth_prefix(rel_path):
    d = rel_path.count(os.sep)
    return "../" * d if d else ""


def to_rel(url, prefix):
    """/assets/x → ../assets/x ; /products/ → ../products/index.html"""
    if not url.startswith("/") or url.startswith("//"):
        return url
    path, _, tail = url.partition("#")
    path, _, query = path.partition("?")
    if query:
        query = "?" + query
    if tail:
        tail = "#" + tail

    if path.startswith("/assets/"):
        return prefix + path[1:] + query + tail
    if path == "/":
        return prefix + "index.html" + query + tail
    clean = path.strip("/")
    if path.endswith("/") or clean in PAGE_ROUTES:
        return prefix + clean + "/index.html" + query + tail
    return prefix + clean + query + tail


def rewrite_html(text, prefix):
    def attr(m):
        name, quote, url = m.group(1), m.group(2), m.group(3)
        return '%s=%s%s%s' % (name, quote, to_rel(url, prefix), quote)
    text = re.sub(r'\b(href|src)=(["\'])(/[^"\']*)\2', attr, text)

    def srcset(m):
        quote, value = m.group(1), m.group(2)
        parts = []
        for item in value.split(","):
            item = item.strip()
            if not item:
                continue
            bits = item.split()
            bits[0] = to_rel(bits[0], prefix)
            parts.append(" ".join(bits))
        return 'srcset=%s%s%s' % (quote, ", ".join(parts), quote)
    text = re.sub(r'srcset=(["\'])([^"\']*)\1', srcset, text)

    # url(/assets/…) inside inline styles
    text = re.sub(r'url\((/assets/[^)]*)\)',
                  lambda m: "url(%s)" % to_rel(m.group(1), prefix), text)
    # the redirect stubs navigate with script
    text = re.sub(r'location\.replace\("(/[^"]*)"',
                  lambda m: 'location.replace("%s"' % to_rel(m.group(1), prefix), text)
    return text


def run(dist, routes):
    PAGE_ROUTES.update(r.strip("/") for r in routes if r != "/")
    n_html = n_css = 0
    for root, _dirs, files in os.walk(dist):
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, dist)
            if name.endswith(".html"):
                prefix = depth_prefix(rel)
                with open(full, encoding="utf-8") as f:
                    text = f.read()
                with open(full, "w", encoding="utf-8") as f:
                    f.write(rewrite_html(text, prefix))
                n_html += 1
            elif name.endswith(".css"):
                # a stylesheet in assets/css reaches assets/img as ../img
                with open(full, encoding="utf-8") as f:
                    text = f.read()
                text = text.replace('url("/assets/', 'url("../')
                text = text.replace("url('/assets/", "url('../")
                text = text.replace("url(/assets/", "url(../")
                with open(full, "w", encoding="utf-8") as f:
                    f.write(text)
                n_css += 1
    return n_html, n_css
