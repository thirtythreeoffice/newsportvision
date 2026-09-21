/* ===========================================================================
   NEWSPORTVISION — behaviour
   ---------------------------------------------------------------------------
   Motion architecture: one. A deterministic sweep decides *when*, CSS decides
   *how*, and the only thing that still needs a per-frame value in script is
   the header. Image counter-motion runs on the scroll timeline itself where
   the browser has one, so it moves on the compositor, in step with the
   finger. No animation library is loaded: nothing here needs a timeline
   engine, and 70KB of one would buy the page nothing it does not already have.

   Everything degrades: with JS off, all content is present and legible, and
   every reveal is already in its final state.
   =========================================================================== */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)");
  var each = function (list, fn) { Array.prototype.forEach.call(list, fn); };

  root.classList.add("js");

  /* The page's real width, so full-bleed elements meet the screen edge exactly.
     The root's client width never includes a scrollbar or the lane reserved
     for one, which 100vw may or may not, depending on the browser. The head
     script writes it before first paint; this keeps it current. Written only
     when it changes: a custom property on the root restyles the document. */
  var pageW = -1;
  function pageWidth() {
    var w = root.clientWidth;
    if (w && w !== pageW) { pageW = w; root.style.setProperty("--vw", w + "px"); }
  }

  /* =========================================================================
     0. Where a page begins.

        Every link here is an ordinary link to another document, so the
        browser opens that document at its top on its own, and back and
        forward restore what the reader left — which is what a reader
        expects, and none of it is taken away below.

        Two cases still need correcting, and only these two:

          * The page is being read inside someone else's frame — a preview,
            an embed. The scroll that the reader sees belongs to the host's
            container, not to this document, and a new page loaded into the
            frame leaves it exactly where the previous page had pushed it:
            the reader lands half way down a page they have never seen.
          * A browser hands a fresh navigation a restored offset anyway.

        The correction is made before the first frame is painted, and again
        once after load for a browser that restores late. It is never made
        on a timer, and it stands down for good the moment the reader
        touches the page, so it cannot pull them back up from under a
        scroll they have already begun.
     ========================================================================= */
  function jump() {
    try { window.scrollTo({ top: 0, left: 0, behavior: "instant" }); }
    catch (e) { window.scrollTo(0, 0); }
  }

  function arrival() {
    var entry = window.performance && performance.getEntriesByType &&
                performance.getEntriesByType("navigation")[0];
    /* back, forward, reload: the browser's to restore, and it restores it
       well. An anchor is the page's own business. Neither is touched. */
    if ((entry ? entry.type : "navigate") !== "navigate" || location.hash) return;

    /* Only a page this site itself opened may move a host's scroll. Arriving
       from anywhere else, the host put us on screen where it meant to. */
    var framed = window.top !== window.self;
    var ours = document.referrer.lastIndexOf(location.origin + "/", 0) === 0;
    var stood = false;

    each(["wheel", "touchstart", "keydown", "pointerdown"], function (t) {
      window.addEventListener(t, function () { stood = true; },
                              { passive: true, once: true, capture: true });
    });

    function top() {
      if (stood) return;
      if (window.scrollY || window.pageYOffset) jump();
      if (framed && ours) {
        try {
          root.scrollIntoView({ block: "start", inline: "nearest", behavior: "instant" });
        } catch (e) { /* a frame that will not be scrolled is not an error */ }
      }
    }

    top();
    document.addEventListener("DOMContentLoaded", top);
    window.addEventListener("load", function () { requestAnimationFrame(top); });
  }

  arrival();

  /* =========================================================================
     1. Reveals
     A deterministic sweep rather than an IntersectionObserver. IO does not
     reliably fire for an element that goes from below the viewport to above it
     in a single frame — which is exactly what happens on an anchor jump, a
     restored scroll position, or a find-in-page. That left content permanently
     invisible. The sweep runs inside the scroll loop that already exists, over
     a list that only ever shrinks.

     The entrance itself is a CSS animation, not a transition, so it never
     replaces an element's own transitions, and its stagger is a custom
     property rather than a timer: a fast flick reveals everything it passed
     in one frame, each piece still on its own beat.
     ========================================================================= */
  var pending = [];

  function collectReveals() {
    pending = Array.prototype.slice.call(document.querySelectorAll("[data-reveal]:not(.is-in)"));
    pending.forEach(function (el) {
      if (el.dataset.delay) el.style.setProperty("--rd", parseInt(el.dataset.delay, 10) + "ms");
    });
    if (reduce.matches) {
      pending.forEach(function (el) { el.classList.add("is-in"); });
      pending = [];
      return;
    }
    orderReveals();
  }

  /* Ordered down the page once, so a frame only has to look at the next one
     or two. Measuring all thirty-five of them on every scrolled frame is what
     a fast flick could not afford. */
  function orderReveals() {
    if (pending.length < 2) return;
    var y = window.scrollY || window.pageYOffset;
    var tops = new Map();
    pending.forEach(function (el) { tops.set(el, el.getBoundingClientRect().top + y); });
    pending.sort(function (a, b) { return tops.get(a) - tops.get(b); });
  }

  function sweep(vh) {
    if (!pending.length) return;
    var trigger = vh * 0.94;
    var i = 0, misses = 0;
    /* The list runs down the page, so the first element still below the line
       ends the search — with a couple of elements of slack, since a grid can
       place a later element beside an earlier one. */
    while (i < pending.length && misses < 3) {
      if (pending[i].getBoundingClientRect().top < trigger) { i++; misses = 0; }
      else { misses++; i++; }
    }
    i -= misses;
    if (i <= 0) return;
    var hit = pending.splice(0, i);
    for (var k = 0; k < hit.length; k++) {
      if (hit[k].getBoundingClientRect().top < trigger) hit[k].classList.add("is-in");
      else pending.push(hit[k]);
    }
    if (misses) orderReveals();
  }

  /* The axis strokes are painted on, left to right, once. */
  var axis = null;
  function paintAxis(vh) {
    if (!axis) return;
    if (axis.getBoundingClientRect().top < vh * 0.82) {
      axis.classList.add("is-painted");
      axis = null;
    }
  }

  /* =========================================================================
     2. Header
     The header takes its colour from whichever field is behind it. The field
     bands are measured once per layout change and looked up by scroll
     position, instead of hit-testing the page on every frame.
     ========================================================================= */
  var header = document.querySelector(".site-header");
  var headerStuck = null;
  var headerField = "";
  var bands = [];

  function measureBands() {
    var y = window.scrollY || window.pageYOffset;
    bands = [];
    each(document.querySelectorAll("main [data-field], body > footer[data-field]"), function (el) {
      var r = el.getBoundingClientRect();
      if (r.height) bands.push({ top: r.top + y, bottom: r.bottom + y, field: el.dataset.field });
    });
  }

  function fieldAt(docY) {
    /* Nested fields come after their parents in document order; the last
       band that contains the point is the innermost one. */
    var hit = "paper";
    for (var i = 0; i < bands.length; i++) {
      if (docY >= bands[i].top && docY < bands[i].bottom) hit = bands[i].field;
    }
    return hit;
  }

  var headerMid = 0;
  function headerFrame(y) {
    var stuck = y > 12;
    if (stuck !== headerStuck) {
      headerStuck = stuck;
      header.classList.toggle("is-stuck", stuck);
    }
    if (!stuck) return;
    var field = fieldAt(y + headerMid);
    if (field === headerField) return;
    headerField = field;
    header.style.setProperty("--header-bg",
      field === "ink" ? "var(--nsv-ink)" : field === "yellow" ? "var(--nsv-yellow)" : "var(--nsv-paper)");
    header.style.setProperty("--header-fg",
      field === "ink" ? "var(--nsv-paper)" : "var(--nsv-ink)");
  }

  /* =========================================================================
     3. Counter-motion — fallback only.
     Images drift against their frame by a few percent. Where the browser has
     scroll-driven animations, CSS does this on the compositor and this code
     never runs. Elsewhere it runs on devices with a fine pointer only: a
     main-thread effect on a touch screen always trails the finger by a frame,
     and a photograph that swims against its own window reads as a glitch.
     ========================================================================= */
  var movers = [];
  var scrollTimeline = window.CSS && CSS.supports && CSS.supports("animation-timeline: view()");

  function collectMovers() {
    movers = (scrollTimeline || !fine.matches || reduce.matches) ? [] :
      Array.prototype.map.call(document.querySelectorAll("[data-counter] img"), function (img) {
        return { img: img, box: img.closest("[data-counter]") };
      });
  }

  function moverFrame(vh) {
    if (!movers.length) return;
    var rects = movers.map(function (m) { return m.box.getBoundingClientRect(); });
    for (var i = 0; i < movers.length; i++) {
      var r = rects[i];
      if (r.bottom < -200 || r.top > vh + 200) continue;
      /* 0 as the frame enters at the bottom, 1 as it leaves at the top —
         the same progress the CSS view timeline uses. */
      var p = (vh - r.top) / (vh + r.height);
      if (p < 0) p = 0; else if (p > 1) p = 1;
      movers[i].img.style.translate = "0 " + (-3.5 + p * 7).toFixed(2) + "%";
    }
  }

  /* =========================================================================
     4. The single scroll loop
     ========================================================================= */
  var ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY || window.pageYOffset;
    var vh = window.innerHeight;
    sweep(vh);
    paintAxis(vh);
    if (header) headerFrame(y);
    moverFrame(vh);
  }
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(frame);
  }

  /* Anything that moves layout — the width of the window, the type being set,
     an image or a panel changing height — re-measures the header bands. */
  var relayoutQueued = false;
  function relayout() {
    if (relayoutQueued) return;
    relayoutQueued = true;
    requestAnimationFrame(function () {
      relayoutQueued = false;
      pageWidth();
      orderReveals();
      if (header) headerMid = header.getBoundingClientRect().height / 2;
      measureBands();
      headerField = "";
      onScroll();
    });
  }

  /* =========================================================================
     5. Menu
     ========================================================================= */
  var closeMenu = function () {};

  function menu() {
    var btn = document.querySelector(".menu-btn[aria-controls]");
    var panel = document.getElementById("menu");
    if (!btn || !panel) return;
    var lastFocus = null;
    var focusTimer = 0;
    var outside = [document.querySelector("main"), document.querySelector("body > footer"),
                   document.querySelector(".skip-link")].filter(Boolean);

    panel.inert = true;

    function isOpen() { return panel.classList.contains("is-open"); }

    function focusables() {
      return Array.prototype.filter.call(
        panel.querySelectorAll("a[href], button:not([disabled])"),
        function (el) { return el.offsetParent !== null; });
    }

    function open() {
      if (isOpen()) return;
      lastFocus = document.activeElement;
      panel.inert = false;
      panel.removeAttribute("aria-hidden");
      panel.classList.add("is-open");
      btn.setAttribute("aria-expanded", "true");
      root.classList.add("menu-open");
      outside.forEach(function (el) { el.inert = true; });
      document.addEventListener("keydown", onKey);
      clearTimeout(focusTimer);
      /* After the wipe has begun, and only if the menu is still open by then —
         a quick second tap must not leave focus inside a closed panel. */
      focusTimer = setTimeout(function () {
        if (!isOpen()) return;
        var f = focusables();
        if (f.length) f[0].focus({ preventScroll: true });
      }, 90);
    }

    function close(opts) {
      clearTimeout(focusTimer);
      if (!isOpen()) return;
      panel.classList.remove("is-open");
      if (opts && opts.instant) {
        panel.style.transition = "none";
        void panel.offsetWidth;
        panel.style.transition = "";
      }
      btn.setAttribute("aria-expanded", "false");
      panel.setAttribute("aria-hidden", "true");
      panel.inert = true;
      root.classList.remove("menu-open");
      outside.forEach(function (el) { el.inert = false; });
      document.removeEventListener("keydown", onKey);
      /* Focus never stays behind in a closed panel. It goes back to where it
         came from — or to the menu button, since a tap does not focus a
         button in every browser and "where it came from" is then the page. */
      if (!(opts && opts.navigating)) {
        var back = lastFocus && lastFocus !== document.body && lastFocus.isConnected &&
          !panel.contains(lastFocus) ? lastFocus : btn;
        back.focus({ preventScroll: true });
      } else if (panel.contains(document.activeElement)) {
        document.activeElement.blur();
      }
    }
    closeMenu = close;

    function onKey(e) {
      if (e.key === "Escape") { close(); return; }
      if (e.key !== "Tab") return;
      var f = focusables();
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }

    btn.addEventListener("click", function () { isOpen() ? close() : open(); });
    var closeBtn = panel.querySelector("[data-menu-close]");
    if (closeBtn) closeBtn.addEventListener("click", function () { close(); });
    var leaveTimer = 0;
    panel.addEventListener("click", function (e) {
      var a = e.target.closest("a[href]");
      if (!a) return;
      var sameDoc = a.pathname === location.pathname && a.search === location.search;
      var leaves = !sameDoc && !e.defaultPrevented && e.button === 0 &&
        !(e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) &&
        (a.protocol === "http:" || a.protocol === "https:" || a.protocol === "file:") &&
        (!a.target || a.target === "_self");
      if (!leaves) {
        /* This page stays: an anchor, a mail link, a new tab. */
        close({ navigating: sameDoc && !!a.hash });
        return;
      }
      /* Another page. The panel stays drawn while it loads, so the reader goes
         from the menu straight to the page they chose, never back through the
         one they left. The chosen line keeps its mark as the only feedback.
         If nothing arrives (a cancelled load), the panel lets go. */
      each(panel.querySelectorAll(".is-going"), function (x) { x.classList.remove("is-going"); });
      a.classList.add("is-going");
      clearTimeout(leaveTimer);
      leaveTimer = setTimeout(function () {
        a.classList.remove("is-going");
        close();
      }, 4000);
    });
    window.addEventListener("pagehide", function () { clearTimeout(leaveTimer); });
  }

  /* =========================================================================
     6. Large actions — the yellow field grows from the edge the pointer
        actually came in from.
     ========================================================================= */
  function actions() {
    if (!fine.matches) return;
    each(document.querySelectorAll(".action"), function (el) {
      el.addEventListener("pointerenter", function (e) {
        var r = el.getBoundingClientRect();
        el.style.setProperty("--origin", (e.clientX - r.left) < r.width / 2 ? "left" : "right");
      });
    });
  }

  /* =========================================================================
     7. The echo — VISION, looked at twice.
        Off by default. Surfaces under a fine pointer, tracks it by a few
        pixels, and leaves when the pointer does.
     ========================================================================= */
  function echo() {
    if (reduce.matches || !fine.matches) return;
    each(document.querySelectorAll(".echo"), function (el) {
      var raf = 0, lastX = 0;
      function place() {
        raf = 0;
        var r = el.getBoundingClientRect();
        var nx = (lastX - r.left) / r.width - 0.5;
        el.style.setProperty("--ex", (nx * 10).toFixed(2) + "px");
        el.style.setProperty("--ey", (r.height * 1.02).toFixed(1) + "px");
      }
      el.addEventListener("pointermove", function (e) {
        lastX = e.clientX;
        if (!raf) raf = requestAnimationFrame(place);
      });
      el.addEventListener("pointerleave", function () { el.style.setProperty("--ex", "0px"); });
      el.style.setProperty("--ey", el.getBoundingClientRect().height * 1.02 + "px");
    });
  }

  /* =========================================================================
     8. Cursor — a rule, not a blob. Desktop only, and it never replaces the
        native pointer's meaning: it sits on top of it. The loop runs only
        while the rule is still travelling.
     ========================================================================= */
  function cursor() {
    if (reduce.matches || !fine.matches) return;
    var el = document.querySelector(".cursor");
    if (!el) return;
    var label = el.querySelector(".cursor__label");
    document.body.classList.add("cursor-on");

    var tx = 0, ty = 0, cx = 0, cy = 0, raf = 0, placed = false, current = "";
    function paint() {
      el.style.transform = "translate3d(" + cx.toFixed(1) + "px," + cy.toFixed(1) + "px,0)";
    }
    function loop() {
      cx += (tx - cx) * 0.22;
      cy += (ty - cy) * 0.22;
      if (Math.abs(tx - cx) < 0.15 && Math.abs(ty - cy) < 0.15) {
        cx = tx; cy = ty; paint(); raf = 0; return;
      }
      paint();
      raf = requestAnimationFrame(loop);
    }
    window.addEventListener("pointermove", function (e) {
      if (e.pointerType && e.pointerType !== "mouse") return;
      tx = e.clientX; ty = e.clientY;
      if (!placed) {
        /* Arrive where the pointer is, not with a streak from the corner. */
        placed = true; cx = tx; cy = ty; paint();
        el.style.opacity = "1";
      }
      if (!raf) raf = requestAnimationFrame(loop);
      var hit = e.target.closest && e.target.closest("[data-cursor]");
      var want = hit ? hit.dataset.cursor : "";
      if (want !== current) {
        current = want;
        if (want) label.textContent = want;
        el.classList.toggle("has-label", !!want);
      }
    }, { passive: true });
    document.documentElement.addEventListener("pointerleave", function () {
      el.style.opacity = "0";
      placed = false;
    });
  }

  /* =========================================================================
     9. The closing inversion — the last field turns over under the pointer.
     ========================================================================= */
  var footerCanvas = null;
  function closer() {
    footerCanvas = document.querySelector(".footer-canvas");
    var f = footerCanvas;
    if (!f || !fine.matches) return;
    f.addEventListener("pointerenter", function () { f.classList.add("is-lit"); });
    f.addEventListener("pointerleave", function () { f.classList.remove("is-lit"); });
    f.addEventListener("focusin", function () { f.classList.add("is-lit"); });
    f.addEventListener("focusout", function (e) {
      if (!f.contains(e.relatedTarget)) f.classList.remove("is-lit");
    });
  }

  /* =========================================================================
     10. Legal contents — highlight the section being read.
     ========================================================================= */
  function legalToc() {
    var toc = document.querySelector(".legal-toc");
    if (!toc || !("IntersectionObserver" in window)) return;
    var links = {};
    each(toc.querySelectorAll("a[href^='#']"), function (a) {
      links[a.getAttribute("href").slice(1)] = a;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var a = links[e.target.id];
        if (!a || !e.isIntersecting) return;
        Object.keys(links).forEach(function (k) { links[k].classList.remove("is-current"); });
        a.classList.add("is-current");
      });
    }, { rootMargin: "-10% 0px -70% 0px" });
    Object.keys(links).forEach(function (id) {
      var s = document.getElementById(id);
      if (s) io.observe(s);
    });
  }

  /* =========================================================================
     11. Photographs arrive, they do not pop.
     The head script marks every image as it loads; this catches the ones that
     were already complete before it could listen.
     ========================================================================= */
  function images() {
    each(document.querySelectorAll(".frame img"), function (img) {
      if (img.complete && img.naturalWidth) img.classList.add("is-loaded");
      else img.addEventListener("load", function () { img.classList.add("is-loaded"); }, { once: true });
    });
  }

  /* Photographs are there before the reader is.
     Lazy loading waits until a picture is nearly on screen, and on a phone a
     quick flick outruns it: the reader arrives at a placeholder. So once the
     page has settled, the remaining pictures are fetched quietly in the
     background — nearest first, two at a time — and are already decoded when
     the reader gets to them. Not on a metered or very slow connection. */
  function warmImages() {
    var c = navigator.connection;
    if (c && (c.saveData || /(^|-)2g$/.test(c.effectiveType || ""))) return;
    var queue = Array.prototype.filter.call(document.querySelectorAll('.frame img[loading="lazy"]'),
      function (img) { return !img.complete; })
      .map(function (img) {
        return { img: img, d: Math.abs(img.closest(".frame").getBoundingClientRect().top) };
      })
      .sort(function (a, b) { return a.d - b.d; })
      .map(function (x) { return x.img; });
    var active = 0;
    function next() {
      while (active < 2 && queue.length) {
        var img = queue.shift();
        if (img.complete) continue;
        active++;
        var done = function () { active--; next(); };
        img.addEventListener("load", done, { once: true });
        img.addEventListener("error", done, { once: true });
        img.loading = "eager";
      }
    }
    next();
  }

  /* =========================================================================
     12. The opening sequence.
         Frame 1: the yellow field. Frame 2: the rule draws across one grid
         unit. Frame 3: the lines lift out from behind their own baselines.
         Under 1.4s, only on a real first entrance, and never before the lines
         have been set — an animation of type that is still being composed
         would be half over by the time it could be seen.
     ========================================================================= */
  function intro() {
    var hero = document.querySelector("[data-intro]");
    if (!hero) return;
    var done = function () { hero.classList.add("intro-done"); };
    if (reduce.matches) { done(); return; }
    try {
      if (sessionStorage.getItem("nsv-intro") === "1") { done(); return; }
      sessionStorage.setItem("nsv-intro", "1");
    } catch (err) { /* private mode: just play it */ }

    var started = false;
    function run() {
      if (started) return;
      started = true;
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          hero.classList.add("intro-run");
          /* Once it has played (the last piece lands at 1.32s), hand the hero
             back to its resting styles. Timed from the first frame of the
             sequence, not from the request, so a slow first frame can never
             cut the ending short. */
          setTimeout(function () { hero.classList.remove("intro-run"); done(); }, 1500);
        });
      });
    }
    if (root.hasAttribute("data-composed")) run();
    else {
      document.addEventListener("nsv:composed", run, { once: true });
      setTimeout(run, 2600);
    }
  }

  /* =========================================================================
     Boot
     ========================================================================= */
  function boot() {
    pageWidth();
    axis = document.querySelector(".axis:not(.is-painted)");
    collectReveals();
    menu();
    actions();
    echo();
    cursor();
    closer();
    legalToc();
    images();
    collectMovers();
    intro();

    if (header) headerMid = header.getBoundingClientRect().height / 2;
    measureBands();
    frame();

    window.addEventListener("scroll", onScroll, { passive: true });

    /* Width is the only resize that changes the composition. A phone's address
       bar sliding in and out changes the height on almost every scroll, and
       must cost nothing. */
    var lastW = window.innerWidth;
    window.addEventListener("resize", function () {
      if (window.innerWidth !== lastW) {
        lastW = window.innerWidth;
        pageWidth();
        collectMovers();
        relayout();
      } else {
        onScroll();
      }
    }, { passive: true });

    if ("ResizeObserver" in window) new ResizeObserver(relayout).observe(document.body);
    document.addEventListener("nsv:composed", relayout);
    /* A late sweep catches anything that only became measurable after images
       and fonts settled. */
    window.addEventListener("load", function () {
      relayout();
      var idle = window.requestIdleCallback || function (fn) { return setTimeout(fn, 300); };
      setTimeout(function () { idle(warmImages, { timeout: 1500 }); }, 400);
    });

    /* Returning through the back button restores the page as it was left —
       including a panel caught mid-close or a footer still lit by a pointer
       that is no longer there. Put it back to rest. */
    window.addEventListener("pageshow", function (e) {
      if (!e.persisted) return;
      each(document.querySelectorAll(".menu-list .is-going"), function (x) { x.classList.remove("is-going"); });
      closeMenu({ instant: true, navigating: true });
      if (footerCanvas) footerCanvas.classList.remove("is-lit");
      relayout();
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
