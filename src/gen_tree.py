"""Write src/tree_of_sport.svg — the Tree of Sport as the page inlines it.

    python3 src/gen_tree.py

Draws the tree (src/tree_of_sport.py) and, when svgo is on the PATH, passes it
through svgo with ids, roles, aria and the title kept. The title is left as a
token; the page puts the alt text of its own language there. Run it after
changing the drawing; the build only reads the file.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tree_of_sport  # noqa: E402

CONFIG = """export default { multipass: true, floatPrecision: 1, plugins: [{ name: 'preset-default',
  params: { overrides: { cleanupIds: false, removeTitle: false, removeDesc: false, removeViewBox: false,
    collapseGroups: false, moveGroupAttrsToElems: false, inlineStyles: false, minifyStyles: false,
    mergePaths: false, removeUnknownsAndDefaults: { keepRoleAttr: true, keepAriaAttrs: true } } } }] };
"""

raw = tree_of_sport.svg("%%TITLE%%")
out = os.path.join(HERE, "tree_of_sport.svg")
svgo = shutil.which("svgo")
if svgo:
    with tempfile.TemporaryDirectory() as d:
        src, cfg = os.path.join(d, "t.svg"), os.path.join(d, "svgo.config.mjs")
        open(src, "w").write(raw)
        open(cfg, "w").write(CONFIG)
        subprocess.run([svgo, "--config", cfg, src, "-o", out], check=True, capture_output=True)
else:
    open(out, "w").write(raw)
print("tree_of_sport.svg: %d bytes%s" % (os.path.getsize(out), "" if svgo else " (svgo not found: unoptimised)"))
