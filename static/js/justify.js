/* ===========================================================================
   NEWSPORTVISION — the justification engine
   ---------------------------------------------------------------------------
   The logo is a three-line typographic block justified to one measure. Its
   three lines are all the same size; what changes per line is the letterfit,
   and on the first line, where the words run out, a white rule finishes the
   measure.

   This module applies that setting rule to the page:

     1. a stack shares ONE font size, chosen so the longest line exactly fills
        the measure;
     2. every other line is stretched to that same measure using Archivo's
        variable width axis (62–125), with letter-spacing only as the residual;
     3. lines marked as rule-lines keep their natural width, and a flexing rule
        fills whatever measure is left over.

   Width axis first, tracking second, is the order a typesetter would use: it
   keeps the colour of the line even instead of blowing the words apart.

   Without JS the same markup still renders: lines simply wrap at the CSS
   clamp size, flush left. Nothing is hidden and nothing overflows.
   =========================================================================== */
(function () {
  "use strict";

  /* The stacks are claimed by the one-line script in the document head, before
     first paint — a deferred script can run after the browser has already
     shown an unset heading once. The matching CSS holds an unjustified stack
     back, so a heading is composed before it is ever seen rather than resized
     in front of the reader; if this file never runs, a CSS failsafe releases
     every stack after three seconds, so nothing can stay hidden. */
  document.documentElement.classList.add("js-justify");

  var AXIS_MIN = 62, AXIS_MID = 100, AXIS_MAX = 125;
  var TRACK_MIN = -0.05, TRACK_MAX = 0.34;   // em — the residual allowance
  /* A line that cannot reach the measure even at the widest cut and the full
     allowance ("ART" under "CULTURE") is not torn into loose letters on the
     way to falling short anyway. It is set as a word, wide and lightly
     tracked, and the mark beneath it carries the measure — the logo's own
     answer: where the words run out, the bar finishes the line. */
  var TRACK_SHORT = 0.06;
  var REF = 200;                              // reference size for measuring

  /* How the engine stays cheap.
     Archivo's advances interpolate linearly between its width masters at 62,
     100 and 125 (measured: under 0.01px of error at nine points along the
     axis). So a line's width is fully described by three measurements, and
     the axis value that lands it on the measure is solved, not searched.

     Every stack on the page is measured together: all lines are set to one
     axis value, then all are read, so the whole page costs five layouts per
     pass however many lines it has — instead of eleven forced layouts per
     line, which on a mid-range phone held the first screen back for a good
     fraction of a second. */

  function visible(el) { return !!(el.offsetParent || el.getClientRects().length); }

  function hostOf(el) { return el.closest("[data-jl-host]") || el; }

  function release(stack) { stack.classList.add("is-justified"); }

  function widthOf(el) { return el.getBoundingClientRect().width; }

  /* Width at axis value v, from the three master measurements. */
  function widthAt(m, v) {
    return v <= AXIS_MID
      ? m[0] + (m[1] - m[0]) * (v - AXIS_MIN) / (AXIS_MID - AXIS_MIN)
      : m[1] + (m[2] - m[1]) * (v - AXIS_MID) / (AXIS_MAX - AXIS_MID);
  }

  /* The axis value whose width is `target`, clamped to the axis. */
  function solveAxis(m, target) {
    if (target <= m[0]) return AXIS_MIN;
    if (target >= m[2]) return AXIS_MAX;
    if (target <= m[1]) {
      return m[1] === m[0] ? AXIS_MID
        : AXIS_MIN + (target - m[0]) * (AXIS_MID - AXIS_MIN) / (m[1] - m[0]);
    }
    return m[2] === m[1] ? AXIS_MID
      : AXIS_MID + (target - m[1]) * (AXIS_MAX - AXIS_MID) / (m[2] - m[1]);
  }

  var boxWidth = typeof WeakMap === "function" ? new WeakMap() : null;

  function justifyAll(list) {
    /* Read: which stacks can be set, and at what measure. */
    var jobs = [];
    list.forEach(function (stack) {
      var shown = visible(stack);
      var box = shown ? widthOf(stack) : 0;
      /* Remember the measure this pass used, so the resize watcher can tell a
         real change of measure from the notification this pass itself causes. */
      if (boxWidth) boxWidth.set(stack, box);
      if (!shown || box < 40) { release(stack); return; }
      var lines = Array.prototype.filter.call(stack.querySelectorAll("[data-jl]"), function (l) {
        return !l.hidden && !hostOf(l).hidden;
      });
      if (!lines.length) { release(stack); return; }
      jobs.push({ stack: stack, box: box, lines: lines.map(function (l) {
        return { el: l, host: hostOf(l), rule: l.hasAttribute("data-jl-rule"), m: [] };
      }) });
    });
    if (!jobs.length) return;

    var all = [];
    jobs.forEach(function (j) { all.push.apply(all, j.lines); });

    /* Measure every line at the reference size, at each width master. */
    all.forEach(function (L) {
      L.host.style.fontSize = REF + "px";
      L.el.style.letterSpacing = "0em";
      L.el.style.marginRight = "0px";
      L.el.style.width = "max-content";
    });
    [AXIS_MIN, AXIS_MID, AXIS_MAX].forEach(function (v, k) {
      all.forEach(function (L) { L.el.style.setProperty("--wdth", v); });
      all.forEach(function (L) { L.m[k] = widthOf(L.el) / REF; });
    });

    /* Solve and write. The longest line at the normal width sets the size for
       the whole stack; every other line is solved onto the same measure. */
    jobs.forEach(function (j) {
      var widest = 0;
      j.lines.forEach(function (L) { if (L.m[1] > widest) widest = L.m[1]; });
      var size = widest > 0 ? j.box / widest : 0;
      var max = parseFloat(j.stack.dataset.jmax || "0");
      var min = parseFloat(j.stack.dataset.jmin || "0");
      if (max && size > max) size = max;
      if (min && size < min) size = min;
      j.size = size;
      /* A stack held at its maximum size no longer fills the column; its
         measure is its own widest line, and the others are set to that. */
      j.measure = Math.min(j.box, widest * size);
      j.lines.forEach(function (L) {
        L.el.style.width = "";
        if (!size || !isFinite(size)) { L.host.style.fontSize = ""; L.el.style.removeProperty("--wdth"); return; }
        L.host.style.fontSize = size + "px";
        if (L.rule) {
          /* Rule-lines stay at their designed width; the bar absorbs the rest. */
          L.el.style.setProperty("--wdth", AXIS_MID);
          L.el.style.letterSpacing = "";
          L.el.style.marginRight = "";
          return;
        }
        var target = j.measure / size;
        L.axis = Math.abs(L.m[1] - target) * size > 0.5 ? solveAxis(L.m, target) : AXIS_MID;
        L.el.style.setProperty("--wdth", L.axis.toFixed(3));
      });
    });

    /* Verify against the real line and hand whatever is left to tracking —
       the axis ends where the font ends, and sub-pixel rounding is real. */
    all.forEach(function (L) { L.w = L.rule || L.axis == null ? 0 : widthOf(L.el); });
    jobs.forEach(function (j) {
      j.lines.forEach(function (L) {
        if (L.rule || L.axis == null || !j.size) return;
        var residual = j.measure - L.w;
        var text = (L.el.textContent || "").trim();
        var gaps = Math.max(text.length - 1, 1);
        var em = Math.abs(residual) < 0.25 ? 0 : (residual / gaps) / j.size;
        if (em > TRACK_MAX) em = TRACK_SHORT;
        if (em < TRACK_MIN) em = TRACK_MIN;
        L.el.style.letterSpacing = em ? em.toFixed(5) + "em" : "0em";
        /* letter-spacing adds a trailing gap after the final glyph; pull it
           back so the line still sits flush on the right edge. */
        L.el.style.marginRight = em ? (-em).toFixed(5) + "em" : "0px";
      });
      release(j.stack);
    });
  }

  /* --- Narrow-screen recomposition -----------------------------------------
     A fifteen-character line on a 375px screen would have to be set at 36px to
     fill the measure, which is not a hero. Where the author supplied an
     alternative break for narrow screens, use it. */
  var mqNarrow = window.matchMedia("(max-width: 767px)");

  function recompose(stack) {
    var narrow = mqNarrow.matches;
    Array.prototype.forEach.call(stack.querySelectorAll("[data-jl]"), function (l) {
      var alt = l.dataset.jlNarrow;
      if (!alt) return;
      if (!l.dataset.jlWide) l.dataset.jlWide = l.textContent.trim();
      var want = narrow ? alt : l.dataset.jlWide;
      if (l.textContent !== want) l.textContent = want;
    });
    Array.prototype.forEach.call(stack.querySelectorAll("[data-jl-only]"), function (l) {
      var only = l.dataset.jlOnly;
      var show = (only === "narrow") ? narrow : !narrow;
      var host = hostOf(l);
      host.hidden = !show;
      if (host !== l) l.hidden = !show;
    });
  }

  var stacks = [], started = false, schedulePublic = function () {};

  function runAll() {
    for (var i = 0; i < stacks.length; i++) recompose(stacks[i]);
    try { justifyAll(stacks); }
    finally { stacks.forEach(release); }
  }

  function init() {
    if (started) return;
    started = true;
    stacks = Array.prototype.slice.call(document.querySelectorAll("[data-justify-stack]"));
    if (stacks.length) runAll();

    /* Tell the page its display type is set: the opening sequence waits for
       this, so it never animates lines that are still being composed. */
    document.documentElement.setAttribute("data-composed", "");
    try { document.dispatchEvent(new CustomEvent("nsv:composed")); } catch (e) { /* old engines */ }
    if (!stacks.length) return;

    var raf = 0;
    function schedule() { cancelAnimationFrame(raf); raf = requestAnimationFrame(runAll); }
    schedulePublic = schedule;

    if ("ResizeObserver" in window && boxWidth) {
      /* Only a change of measure recomposes a stack. Its height changes every
         time it is set, and reacting to that would set it twice. A phone's
         address bar sliding away changes neither. */
      var ro = new ResizeObserver(function (entries) {
        var changed = false;
        entries.forEach(function (e) {
          var w = e.target.getBoundingClientRect().width;
          var prev = boxWidth.get(e.target);
          if (prev == null || Math.abs(prev - w) > 0.5) changed = true;
        });
        if (changed) schedule();
      });
      stacks.forEach(function (s) { ro.observe(s); });
    } else {
      var lastW = window.innerWidth;
      window.addEventListener("resize", function () {
        if (window.innerWidth !== lastW) { lastW = window.innerWidth; schedule(); }
      });
    }
    if (mqNarrow.addEventListener) mqNarrow.addEventListener("change", schedule);
    else if (mqNarrow.addListener) mqNarrow.addListener(schedule);

    /* A face that arrives after the first pass (a Latin-extended subset for an
       accented Italian heading, say) changes every width. Set again. */
    if (document.fonts && document.fonts.addEventListener) {
      document.fonts.addEventListener("loadingdone", schedule);
    }
  }

  /* Wait for the display face — setting against a fallback and then reflowing
     is the one place a font swap would show up as a layout jump. Only that one
     face is waited for: document.fonts.ready waits for every face on the page,
     which held the headline (and with it the largest paint) behind a body
     serif it does not use. Never wait longer than 2.2s. */
  if (document.fonts && document.fonts.load) {
    var faces = Promise.all([
      document.fonts.load('800 100px "Archivo"'),
      document.fonts.load('600 100px "Archivo"')
    ]).catch(function () { /* set with what is there */ });
    faces.then(init);
    setTimeout(init, 2200);
    /* and once the rest have settled, confirm the measure */
    if (document.fonts.ready) document.fonts.ready.then(function () { if (started) schedulePublic(); });
  } else if (document.readyState === "complete") {
    init();
  } else {
    window.addEventListener("load", init);
  }
})();
