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

**The opening is page 1 of the manifesto, redrawn.** A flat blue band, the
Tree of Sport as a framed panel on it, SPORT on the line where the band meets
the green — the PDF's own composition, at the site's scale.

| token / colour | value | where it comes from |
|---|---|---|
| `--fsf-band` | `#458BCA` | the PDF's band (`#448AC9` in the file, as it renders) — ink on it 4.7:1 |
| panel sky | `#74ADDD` → `#79B2E1` → `#4186C7` + glow `#B4DCF0` | sampled down the panel of the PDF render |
| leaves | `#4B943C`, `#5CA443` | the PDF's two greens, as rendered |
| limbs | `#8C5A3E` | the PDF's rosy brown |
| trunk, roots | `#643214` | the PDF's chocolate |
| horizon | `#1E5028` | the PDF's dark green line |
| CULTURE | `#F08C46` | the PDF's peach-orange |
| `--fsf-green` | `#11863C` | the hill. A step deeper than the PDF's `#17A249`: white text on the PDF green is 3.1:1, on this 4.7:1 |

Colours were sampled from the PDF **render** (what a reader sees), not from the
raw JPEG inside it, whose values read darker and duller.

**The tree** (`src/tree_of_sport.py` → `src/gen_tree.py` → `src/tree_of_sport.svg`,
inlined) is a redrawing, not a tracing: it is built in the PDF raster's own
coordinates (1642 × 896) so it can be laid over the original and compared
(`design-review/tree/overlay-*`). Measured from the raster and matched: a
924 × ~440 crown (a 1.7:1 dome), the fork at y≈455, a trunk ~70 wide flaring to
~108, the horizon arc (584 under the trunk), roots from x 171 to 1460, the
letters' positions and cap height. Every shape is placed by rule from a fixed
seed: limbs curve out of the upper trunk and divide into twigs; ~580 almond
leaves are scattered evenly through the dome (never closer than 17 units) in
the two greens, so the crown is lacy with sky between the leaves; the roots
run out under the horizon and send tendrils down, with three passing in front
of L, T and U. Each tone of leaves is one path, so the drawing is ~150 KB
(60 KB gzipped) and about 600 elements.
Layers: `sky`, `label`, `seal`, `roots`, `horizon`, `trunk`, `crown`,
`culture-letters`, `roots-over`.

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

- Client approval of the redrawn Tree of Sport (an interpretation of their artwork).
- Photographs, films, the FSF2026 brochure.
- Native-speaker pass on the Italian.
- Approval of the one-word correction in the EN manifesto (currently published verbatim).
