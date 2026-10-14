# FSF2026 — design notes

Working notes for `/fsf2026/` (branch `feat/fsf2026-page`). Not deployed.
Screenshots of every critique round are in `design-review/`.

## 1. What the house already is (measured from the code, not guessed)

| | value | where |
|---|---|---|
| Ink / paper / yellow | `#1D1D1B` / `#F2EFE7` / `#FAC51C` | `tokens.css` |
| Quiet text | `#63635D` (5.2:1 on paper) | `--fg-quiet` |
| Display face | Archivo variable, `wdth` 62–125, weights 600–800 | `--font-display` |
| Text face | the site's serif, italic used for "handwriting" | `--font-text` |
| Headline setting | `jstack()` — lines justified to one measure by the width axis, tracking only as residual | `justify.js` |
| Grid | 12 columns, gutter = content / 75, page margin `clamp(18px, 4.2vw, 76px)` | `--col`, `--gutter`, `--page-x` |
| Spacing | 12 px atom on a Fibonacci ladder: 12, 24, 36, 60, 96, 156, 252 | `--space-1…7` |
| Between sections | `clamp(96px, 13vh, 190px)` | `--act` |
| Rules | 1 px hair, 2 px thin, the logo bar | `--rule-*` |
| Corners / shadows | none — `--radius: 0` | |
| Motion | 170 ms micro, 340 ms UI, editorial/enter easings; reveals via `data-reveal` | `--t-*`, `--ease-*` |
| A chapter's identity | its own fields, the house's shell; the header names the chapter | `arms.css` |

Every size, gap and rule on the FSF page is one of these tokens. The page adds
colour and one accent face, nothing else.

## 2. What the PDF is

`SPORT MANIFEST ITA-ENG-SRP.pdf`, 3 pages, 595 × 842.

- Fonts: **Apertura** (Regular, Bold) for everything set large; Minion Pro for text. Apertura is commercial and cannot be served on the web.
- Flat fills: blue `#448AC9`, green `#17A249` / `#40AD48`.
- The tree is a **JPEG, 1642 × 896**, with its caption, the logo and the seven letters of CULTURE baked into the pixels. Orange of the letters, sampled: `#ED7835`.
- The staircase of five words: first word bold, the rest regular.

## 3. Decisions

**The opening is one illustrated scene.** The sky is the section's own,
full-bleed, from under the header to the green: a vertical gradient set once
as tokens, with a ~3% grain so it never bands, and a very large, very soft
white-cyan glow behind the crown (a layer of the section, not of the drawing,
so it has no edge at any width). The tree has no background and no frame; the
horizon runs off both edges of the screen. SPORT stands on the line where the
sky meets the green.

| token | value | hue |
|---|---|---|
| `--fsf-sky-top` | `#8FCDF1` | 202° |
| `--fsf-sky-mid` | `#5BB0E8` | 204° |
| `--fsf-sky-horizon` | `#3696DA` | 205° |
| `--fsf-sky-deep` | `#2A86CB` | 206° — behind the roots, down to SPORT |
| `--fsf-glow` | `rgb(232 248 255)` at ≤ 58% | — |

The PDF's own blue (`#448AC9`, 208°) read violet on screen next to the leaves;
the scale above keeps the whole sky in true sky-blue (202–206°).

**The tree** (`src/tree_of_sport.py` → `src/gen_tree.py` → `src/tree_of_sport.svg`,
inlined; 121 KB after SVGO, 24 paths, 6 leaf symbols, ~450 leaf uses). Hand
constructed, no raster, no trace, built in the PDF raster's coordinates so it
can be laid over the original (`design-review/tree-v4/overlay-*`). Groups in
drawing order: `horizon` · `roots-primary` · `roots-secondary` ·
`roots-tendrils` · `trunk` · `crown` (`branches-primary` · `branches-secondary`
· `twigs` · `leaves-0…9`) · `culture-letters` · `roots-front`.
Branches and roots are tapered filled shapes; the primary limbs carry a radial
fill from bark to rosy brown, so they leave the trunk without a seam. Leaves
are six drawn shapes with a midrib, set along the twigs — denser toward the
crown's edge, sparse inside so the limbs show — in the PDF's two greens.
`--fsf-glow`, the sky and the label "The tree of sport" belong to the page;
the yellow seal is no longer drawn into the tree.

**Growth (storyboard).** From culture to sport: the roots feed the tree.
Plays once, when the opening arrives; 3.6 s on a desktop, ×0.65 on a phone.

| time | what happens |
|---|---|
| 0.0–0.9 s | the glow behind the crown brightens |
| 0.0–0.8 s | the horizon opens from the centre to both edges |
| 0.3–1.5 s | roots grow out of the foot: primary, then secondary, then the tendrils (and the three in front of L, T, U) |
| 0.7–1.9 s | the letters rise 12 px and fade in, C to E, as the roots reach them |
| 0.95–1.75 s | the trunk rises from the horizon |
| 1.33–2.54 s | limbs grow out of the trunk: primary, secondary, twigs |
| 1.95–3.5 s | leaves open in ten waves from the heart of the crown outward: each scales from its stalk, settling a few degrees as it opens |
| 3.1–3.75 s | SPORT settles onto the line |
| after | desktop only: the crown sways ±0.4° round the top of the trunk on a 7.6 s breath; three leaf groups flutter out of phase. Paused off screen and in a hidden tab. |

How: each part is revealed by a circle in the drawing's own coordinates (an
SVG `<clipPath>`) scaled up from the point it grows from; the leaves grow
through one inherited, registered number (`--grow`) that each leaf — a `<use>`
of a `<symbol>` — scales by from its stalk. Only transforms and opacity, on
about thirty groups. No library. The complete tree is the markup's default:
without script, or with reduced motion, nothing moves and nothing is hidden.

**Type.** Archivo carries the page. **Nunito** (self-hosted, 39 KB) stands in
for the PDF's Apertura — a commercial face — where the PDF uses it: CULTURE,
SPORT (regular, white), and the staircase words.

**SPORT** stands on the boundary: with line-height 1 Nunito's baseline is
0.1714em above the foot of its box in Chromium, WebKit and Firefox, so the box
is pulled down by exactly that and the baseline is the edge of the green.

**The staircase** is one straight diagonal under the five words, as in the PDF:
five columns by six rows, each word's foot on the line where its column
begins. It is drawn on arrival.

**The declaration is an object**: a sheet of the house's paper on the dark
ground, with a header line, a seal, a justified title, the sentence with two
lines to sign on, and a ruled foot. Signed, the same sheet keeps the name,
takes the date, and the seal is stamped on it. Nothing is cleared.

**What is not here yet is named, not faked.** No grey boxes. Two ruled rows —
Photographs, Films — marked "in preparation"; each leaves when its material is
added to `src/fsf2026_media.py`. The programme timeline is not rendered at all
until the brochure supplies facts.

## 4. Accessibility floor

- Text contrast ≥ 4.5:1 everywhere (values above); the breadcrumb inherits the header ink.
- One `h1`; sections labelled; CULTURE is one word to a screen reader, seven spans to the eye.
- Form: real labels (visually hidden), `required`, status in an `aria-live` region, errors never clear input, honeypot off-screen and out of the tab order.
- `prefers-reduced-motion` handled by the house reveal system; the stair is simply present without script.

## 5. Open

- Client approval of the redrawn Tree of Sport (an interpretation of their artwork) and of the growth animation.
- Photographs, films, the FSF2026 brochure.
- Native-speaker pass on the Italian.
- Approval of the one-word correction in the EN manifesto (currently published verbatim).
