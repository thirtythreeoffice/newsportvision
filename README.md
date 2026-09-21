# NEWSPORTVISION

A rebuild of newsportvision.com. Every word, product, service, chapter of the
history, external link and both languages are carried over from the live site;
nothing is invented and nothing is summarised.

```bash
python3 build.py            # build to ./dist
python3 build.py --serve    # build and serve on http://127.0.0.1:8080
```

No Node, no package manager, no dependencies beyond the Python standard
library. Output is plain static HTML.

---

## The system, and where it comes from

Nothing here is a stylistic preference. Each decision traces to a measurement
taken off the supplied logo, or to an ink NewSportVision already prints with.

### The logo, decoded

The logo PNG was decoded pixel by pixel (`src/` tooling, results in
`static/css/tokens.css`):

| measured | value | becomes |
|---|---|---|
| cap height | 64px | the unit: `u = cap/16` |
| letterspacing | ~11.4px | **3u** |
| inter-line gap | 12px | **3u** |
| white bar thickness | 11px | **3u** |
| line advance | 76px | 19u → display `line-height: 0.867` |
| type measure | 316px | the measure every display line fills |
| "NEW" + its tuck | 210px = **66.4%** | the 2/3 : 1/3 split, and 3:2 type scale |
| bar tucks under the W by | 5px | fields interlock, they never butt |

Three numbers do most of the work: **3u** (one atom governing tracking, leading
and rule weight), **19/16** (the leading), and **2/3** (the split).

### The setting rule

The logo is three lines justified to one measure, and where the words run out a
white bar finishes the line. That is the site's typographic rule, applied by
`static/js/justify.js`:

1. a stack shares one font size, set so the longest line fills the measure;
2. every other line is stretched to that measure using Archivo's variable
   **width axis** (62–125), with letter-spacing only as the residual;
3. lines marked as rule-lines keep their natural width and a flexing bar
   finishes them.

Width axis first, tracking second — the order a typesetter uses, so the colour
of the line stays even instead of the words blowing apart.

`src/linebreak.py` chooses where lines turn, minimising the spread between line
widths measured in ems (not characters — "WWW" and "III" are not the same
width). The words themselves are never changed or reordered.

### Colour

Sampled, not chosen. `#FAC51C` is 84% of the logo's pixels; `#1D1D1B` is 5.5%.

The three supporting inks are the ones NSV already prints with — verified
against their own photographs:

| ink | sampled from their material | distance |
|---|---|---|
| `#F37331` orange | the orange printed Guideline, `#EB7733` | **9/255** — the same ink |
| `#2158A8` blue | the blue Guideline, `#034190` | 45 |
| `#0F6433` green | their court surface, `#219D5F` | 74 |

Each is bound to one term of the axis the company says it exists to create —
*"The mission is to create an axis: culture - sport - art."*

- **CULTURE** blue — what is published, taught, convened
- **SPORT** green — what is played, trained, practised
- **ART** orange — what is made as a designed object

So colour on this site always means something. Every product, service and
chapter of the history is placed on one of the three terms (`AXIS` in
`src/content.py`), and that placement is its colour — the painted tab beside
its name, its go-bar, its plate number, its number in the menu, the ghost year
behind its chapter.

**The terms are never printed as labels.** Writing "Art" next to an item would
be a caption explaining the design instead of design doing the work. The tab
carries it; the word is only ever set at full scale, in the company's own
sentence, in the one place that sentence belongs.

Colour also enters in sequence: the opening screen is ink on yellow and nothing
else — pure identity — and the three inks arrive from the second field onward.

Legibility is not symmetrical, so each term carries three values:
`--axis` (text, clears 4.5:1 on its ground), `--axis-mark` (a painted mark,
stays saturated), `--axis-field` (a filled field, the true ink). Green and blue
carry text on paper; orange carries text on ink; only ink is ever set on yellow.
Every pair passes WCAG AA.

Yellow is spent twice on the homepage — to open and to close. Between those two
moments it does not appear as a field at all, which is what makes it land.

### Paint

A white line on a court is painted. So is a brushstroke. It is the same mark,
made by the same gesture, and it is where sport and art actually touch.

`src/gen_brush.py` generates the marks. A brush is not an outline with wavy
edges, it is a bundle of bristles each laying its own track — so every mark is
built as a union of bristle bands that overlap into a solid core, thin at the
edges, run dry at different points and fray apart at the tail. Deterministic:
same seed, same strokes, every build. ~61KB raw, ~25KB gzipped.

Paint appears as: the axis strokes under CULTURE / SPORT / ART, the index tabs,
the bar that opens a typographic wall item, pull-quote rules, the torn edges
where a colour field ends, the painted colour bar in the footer, and one large
**overprinted sweep** per major field — `mix-blend-mode: multiply`, which is
what a second ink actually does on press, so where it crosses the type nothing
lightens and nothing is obscured.

Crisp rules are the institution stating itself; painted ones are the same
statement made by hand. The two are never mixed inside one object.

### Plates

Every image is paired to the words standing next to it, and where nothing in
the library genuinely belongs to a subject the item is set typographically
rather than given a picture that means nothing:

| where | plate | why |
|---|---|---|
| home / event | runner mid-leap | *"is there an evolution? should be"* |
| home / products | the three printed guides | the products themselves |
| home / services | a figure training alone at dawn | *"who is **looking** at the right way to approach sport"* |
| home / history | young gymnasts training | a youth basketball school |
| Guidelines | the three guides | the product |
| Books | a desk, magazines, hand lettering | writing and publishing |
| FutureSportFuture | moon over cloud | the summit, the future |
| Back to School | young athletes | school-age players |
| Help Desk | a guide open in the hand | a guide being consulted |
| Parents of Young Athletes | young gymnasts | young athletes |
| Workshops | a skateboarder on concert-hall steel | *"an artistic exhibition is installed… sport is the art of motion"* |
| About 1989 / BAM / 1999 / 2014 | youth / court / competition / desk | school, movement, championships, concept |

My 12 Seconds, 3 Balls 1 Champion, Master Course: CAMST and NSV Pass carry no
photograph — nothing in the library is about them. Two stock images from the old
site (a vinyl stylus, a factory conveyor) belonged to no subject here at all and
were dropped rather than placed decoratively.

---

## Content

`src/content.py` is the single source of truth — every string transcribed from
the live site (crawled 2026-09-14), English from the default locale and Italian
from `?lang=it`.

Source-side defects are **preserved deliberately**, with notes, rather than
silently corrected:

1. the English footer reads "Newsportvsion", the Italian "Newsportvision";
2. the Italian Help Desk news heading reads "HEL DESK";
3. the Italian homepage leaves the Products and Services blurbs in English;
4. the Italian About page links a transposed, dead BAM URL — the working
   spelling is used so the link resolves, the visible text is unchanged;
5. the two "work in progress" pages carry different dates and messages.

Removed at the client's direction: the rolling `NSV•MOVING FORWARD / FSF /
PRODUCTS•SERVICES` strip (it read as filler), and the `Milano — 2014` note in
the opening screen. The About page's `N EW S PORT V ISION` device — the live
Italian site's spaced initials — broke across two lines and read as a mistake;
that masthead is now the logo itself, three justified lines at seven columns
with the bar finishing the first.

### Routes

11 routes × 2 languages, plus 404s. **114 legacy Wix URLs redirect**, verified
end to end. Shipped three ways: `_redirects` (Netlify), `.htaccess` (Apache),
and an HTML stub at every legacy path so it works on any static host.

The 43 duplicated `copia-di-*` Help Desk pages — whose slugs and titles no
longer matched each other — are rebuilt as **one instrument** at `/help-desk/`.
Every audience, sport, topic and form field survives. Each state is addressable
(`?who=person&sport=basketball&topic=injuries`), so the old deep links land
where they meant to and the back button walks the tree.

`/shop` and its three product pages held unconfigured Wix demo data ("Sono un
prodotto", €20) — no real store. Those URLs redirect to `/products/`.

---

## Engineering

**Motion architecture: one.** A deterministic sweep decides *when*, CSS decides
*how*, and the only per-frame work left in script is the header's colour. No
animation library: nothing here needs a timeline engine.

An IntersectionObserver was tried and removed — it does not reliably fire for an
element that goes from below the viewport to above it in one frame, which is
exactly what an anchor jump or a restored scroll position does, and it left
content permanently invisible.

**Three motions, three properties.** A photograph is touched by three motions,
and each owns its own property on its own element, so none can overwrite
another:

| element | motion | property |
|---|---|---|
| the frame | clips | `overflow: clip` (not `hidden`: that would make it a scroll container and stall the scroll timeline) |
| `<picture>` | the entrance wipe, the hover lift | `clip-path`, `scale` |
| `<img>` | the counter-drift, the arrival fade | `translate`, `opacity` |

**Counter-motion runs on the scroll timeline** (`animation-timeline: view()`),
so it moves on the compositor, exactly with the finger. The image is cut 8%
taller than its window and centred, and drifts 3.5% of its own height each way,
so an edge can never show. Where the browser has no scroll timeline, a script
fallback runs for mouse users only — a main-thread effect on a touch screen
always trails the finger, and a photograph swimming in its window reads as a
glitch.

**Reveals are animations, not transitions.** A start state applies until the
element is in; the entrance fills backwards, so afterwards the element is left
entirely to its own styles. Stagger is a custom property, not a timer: a fast
flick reveals everything it passed in one frame, each piece on its own beat.

**Compose before paint.** The head script claims the display stacks before
first paint; a CSS failsafe releases them after three seconds if the engine
never arrives. The engine solves each line's width-axis value from three
measurements (Archivo interpolates linearly between its masters at 62/100/125 —
measured error under 0.01px), measures every stack on the page together, and
reruns only when a stack's *width* changes. 3.4–5.2× faster per pass than the
binary search it replaced, and one pass at load instead of two.

Two setting rules keep a stack honest:
- a stack held at its maximum size is measured to its own widest line, not to
  the column, so a capped title is never torn into loose letters;
- a line that cannot reach the measure even at the widest cut and the full
  tracking allowance ("ART" under "CULTURE") is set as a word, and the mark
  beneath it carries the measure.

**Built for fast, careless use.**
- The menu survives any number of taps; focus always returns to the button
  (Safari does not focus a tapped button), never stays in a closed panel. The
  page behind is inert and holds still; the panel scrolls on a phone held
  sideways. Following a link, the panel stays drawn until the next page
  arrives.
- Help Desk: a second tap within 350ms of a step change is ignored, so it can
  never answer a question that has not been read. Each choice is a history
  entry, so the back button walks back up the tree.
- Hover states exist only on devices that hover; a finger gets a press state,
  delayed a beat so a scroll that starts on a row never floods it.
- Returning through the back button puts the menu and footer back to rest.
- A phone's address bar sliding in and out costs nothing: only a change of
  width recomposes anything.
- Between pages, a short cross-fade where the browser supports it
  (`@view-transition`), with the header carried across. Off under reduced
  motion.

**Degrades completely.** With JS off every word is present and legible, no
reveal start-state applies, and nothing overflows. Under
`prefers-reduced-motion` nothing stays hidden because its animation was
cancelled.

**Images.** AVIF / WebP / JPEG at 480 / 800 / 1200 / 1600, quality 75. The
ladder is set by the phone column: ~390 CSS px is 780 device px at 2x and 1170
at 3x, so a phone takes the 800 or 1200 file and never the 1600 one (the Home
page's photographs went from 1019 KB to 503 KB on a 3x phone). Every `sizes`
hint is checked against the width the picture actually renders at, from 390 to
1920, so no picture is fetched too small to be sharp. Per-image focal points
keep an aggressive crop on its subject, and a 20px base64 placeholder sits
under every frame.

Loading: the first photograph on each page is fetched at once, at high
priority. Once the page has settled, the rest are fetched quietly in the
background, nearest first and two at a time, so a quick flick never arrives at
a placeholder — except on a data-saver or 2G connection. Each picture fades in
over its placeholder in 240ms. Image URLs carry a content hash, because media
are cached as immutable.

**The event plate.** Its depth is the text's depth. Sized by ratio alone it
grew with its column *and* with the side margin the canvas gains on a wide
screen: 603px tall at 1440, 837 at 1920, 1349 at 2560 — one and a half
screens, and by then it was setting the row height rather than following it.
It is now taken out of flow at 1024px and up, so the text sets the row and the
picture fills exactly that; the two columns end on one line at every width.
Below 1024px the column is too narrow to be a slit (200px at 768), so the
plate takes the full width above the text instead, bounded by the screen.

**Fonts.** Three faces are ever used — Archivo, Newsreader and Newsreader
italic — and the display italic that was being shipped is gone. The stacks
carry metric-matched fallbacks (measured against the real faces: Archivo
97.1% of Arial, Newsreader 102.8% of Georgia) so the swap does not reflow the
page. The setting engine waits for the display face alone: `fonts.ready` waits
for every face on the page, which held the headline — and with it the largest
paint — behind a body serif it does not use.

**Paint.** The grain is two black plates whose grain lives in their alpha
channel. Compositing black at alpha a is arithmetically identical to
multiplying by (1 - a), so they darken exactly as the multiply layer they
replace did — measured: mean 0.9887 against 0.98876, the same integer RGB on
every field — but a blend mode reads the page behind it, so a fixed
full-screen blended layer has to be resolved against fresh content on every
scrolled frame. Nothing blends across the whole viewport any more.

**The scroll frame.** A frame now measures one or two elements, not
thirty-five: the reveal list is ordered down the page once, so the first
element still below the trigger line ends the search. Everything else on the
frame is a cached lookup — the header's field bands are measured per layout
change, not hit-tested per frame.

**Page width.** Full-bleed elements are sized from `--vw`, the page's measured
width (the root's client width), written by the head script before first
paint. `100vw` cannot be trusted for this: whether it includes the scrollbar's
lane depends on the browser once `scrollbar-gutter` is set.

**Dark mode.** `color-scheme: only light`, in CSS and in the head: Chrome for
Android's Auto Dark Theme, WebView's algorithmic darkening and Samsung
Internet's dark mode would otherwise invert the palette.

**Assets are fingerprinted** (`?v=<content hash>`) so a deploy is never half-old
in a returning visitor's cache. The one inline script is pinned by hash in the
Content-Security-Policy, from the same constant the page is built with.

## Verified

- 23 pages: one `h1` each, no heading jumps, every image with `alt`, every
  control with an accessible name, correct `lang`, canonical + hreflang
- 114 legacy URLs → live destinations
- no JS errors or warnings on any page; no missing assets
- no horizontal overflow, and no page can be scrolled sideways, at
  375 / 390 / 430 / 768 / 834 / 1024 / 1280 / 1440 / 1600 / 1920
- every text and fill colour pair passes WCAG AA; focus rings switch to yellow
  on dark grounds, where blue would only reach 2.4:1
- keyboard: skip link first, logical tab order, closed menu out of the tab
  order, menu traps focus and wraps both ways, Escape closes and returns focus
- no text clips its container and no two text elements overlap, across every
  page at 375 / 430 / 834 / 1024 / 1440 / 1920
- phones (320 / 360 / 390 / 412 / 430): no photograph overlaps text, another
  photograph, a colour tongue or a brush sweep; every stacked column has air
  between it and the next; no text runs past the screen
- every justified stack reaches its measure at 360 / 768 / 1440, except lines
  set short by rule
- visible words, alt text, labels and descriptions identical to the previous
  build on all 24 pages
- 24 pages × 320 / 390 / 430 / 768 / 1024 / 1440 / 1920 / 2560: no horizontal
  overflow, no media off-screen, no clipped text, no plate taller than the
  screen
- 179 referenced assets resolve; no console errors on any page
- a jump to the foot of a page, and repeated direction changes, leave nothing
  unrevealed

## Known gaps

- **The Help Desk form has no back end.** It composes the enquiry and hands it
  to the visitor's mail client, addressed to the address the site already
  publishes. Swap one function in `static/js/helpdesk.js` for a POST when an
  endpoint exists; nothing else changes.
- **Imagery is what the live site had.** Several are generic stock. The genuine
  NSV product photography (the printed Guidelines) carries the most weight and
  is used where it counts. Real event and archive photography would lift the
  event and history pages considerably.
- Untranslated Italian strings are the source's, not omissions.
