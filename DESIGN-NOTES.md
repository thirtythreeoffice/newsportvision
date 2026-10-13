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

**Palette — the picture's own, calibrated.**
The PDF blue pasted flat was half of why v1 looked cheap. v2 samples the
illustration's edge instead and continues it into the page:

| token | value | use |
|---|---|---|
| `--fsf-sky-0` | `#4D93DD` | where the page opens — ink on it is 4.9:1 |
| `--fsf-sky-1/2/3` | `#5E9EE5` / `#7BBAF0` / `#217BEB` | the illustration's top corners, top centre, foot |
| `--fsf-green` | `#11863C` | the hill. One step deeper than the PDF's `#17A249`: white on the PDF green is 3.3:1, on this 4.7:1 |
| `--fsf-leaf` | `#17A249` | the PDF's own green, kept for the stair line, where nothing is read against it |
| `--fsf-root` | `#ED7835` | CULTURE — 6.3:1 on ink |

Yellow stays the house's and stays rare: the label mark, the seal, the one
button, the closing field.

**Type.** Archivo carries everything, as on the rest of the site. **Nunito**
(variable, self-hosted, 39 KB, latin) stands in for Apertura in exactly two
places that are born in the PDF: the staircase words and CULTURE. Same rounded,
open geometry; free licence.

**The tree is not framed.** Its caption and logo were painted out of the raster
(row-wise interpolation of the sky behind them — the tree itself is untouched),
and the image thins to nothing on all four sides over a band that repeats its
edge colours stop for stop. Result: no rectangle, a tree standing in the page's
sky. On screens ≥ 1360 px it rises beside the opening statement.

**SPORT** is live text, set across the line where sky becomes hill.
**CULTURE** is live text at the head of the root section, in the picture's arc
and colour. It could not be set over the roots themselves: the letters are part
of the JPEG. With layered source artwork this becomes one composition.

**The staircase** is one SVG path — tread, riser, tread — on a 5 × 5 grid, so a
word and its tread meet by construction. It is drawn on arrival. On a phone the
treads shorten and the stair turns steep; the words keep their size.

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

- Layered/vector source of the Tree of Sport (would let CULTURE sit among the roots as live text, and stay sharp on retina above 1642 px).
- Photographs, films, the FSF2026 brochure.
- Native-speaker pass on the Italian.
- Approval of the one-word correction in the EN manifesto (currently published verbatim).
