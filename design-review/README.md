# FSF2026 v2 — design review rounds

Not deployed (`.vercelignore`). Full-page captures at 1440 and 390 px, WebKit.
"Before" of a round is the "after" of the previous one, so it is stored once.

| file | what it is |
|---|---|
| `v1-*.jpg` | the rejected first version (Step Zero) |
| `round1-before-*` | v2 as first written, before any critique |
| `round1-after-*` | = round 2 before |
| `round2-after-*` | = round 3 before |
| `round3-after-*` | after round 3 |
| `final-*`, `final-it-*`, `final-signed-*` | the branch as pushed: EN, IT, and the signed declaration |

## Round 1 — five weakest, and what was done
1. **The tree was a pasted rectangle** — box edges visible, and the artwork's baked caption and logo made it read as a slide. → caption and logo painted out of the raster; image masked to nothing on three sides; band behind it made transparent at the top.
2. **A dead blue gap between the statement and the tree.** → on wide screens the tree is pulled up to stand beside "Held in Belgrade", under the headline.
3. **The staircase was not a staircase** — one diagonal chopped into fragments. → redrawn as tread/riser/tread, five by five, each word standing on its tread.
4. **The declaration read as a form letter** — line-height 1.8, native 13px checkbox, an empty column beside a tall sheet. → 1.62, drawn checkbox, side statement set at heading scale and made sticky.
5. **A ghost rectangle on the closing yellow** (an inherited "tongue" in a second yellow). → removed.

## Round 2
1. **The stair line rendered dashed in Safari** (stretched SVG + `pathLength`). → script redraws the path in real pixels; length is measured, not declared.
2. **"Held in Belgrade" was painted under the image.** → hero raised above the plate.
3. **The declaration's first line broke as "from / Belgrade / , without"** and the comma was orphaned on mobile. → line lengths retuned; the comma is bound to its line.
4. **Mobile eyebrow wrapped into three ragged lines.** → two clean lines, rule dropped.
5. **Manifesto: an empty left column and the download buried under the text.** → download stands in the left column, at the foot of the text.

## Round 3
1. **"Archive in preparation" was the weakest block** — a leaf garland that read as clip-art. → replaced by two ruled index rows in the house style (Photographs / Films — in preparation); a row leaves when its material arrives.
2. **The sheet had no foot.** → a ruled footer: what the paper is, and the declaration's own three words (symbolic · declarative · voluntary).
3. **A hard line where the picture met the flat blue under it.** → picture fades at its foot too.
4. **Breadcrumb "FSF 26" was grey on blue (≈1.2:1).** → inherits the header's ink.
5. **Ghost name clipped on its line; IT statement touched the crown.** → line widened; statement given a measure.
