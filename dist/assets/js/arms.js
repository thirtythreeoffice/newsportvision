/* ===========================================================================
   A.R.M.S. — the one thing the microsite needs a script for.

   Everything else on this page is CSS: the mark assembles on animations, the
   sections arrive on the host's reveal engine, the index blocks move on
   transitions. What cannot be written in CSS is the answer to "where am I" —
   so the index marks the section the reader is actually in, and nothing else
   happens here.

   One observer, no scroll handler, no loop. With JavaScript off the page is
   whole: every section is present, every link is an anchor that works.
   =========================================================================== */
(function () {
  "use strict";

  var list = document.querySelector(".a-index__list");
  if (!list || !("IntersectionObserver" in window)) return;

  var links = {};
  Array.prototype.forEach.call(list.querySelectorAll("a[href^='#']"), function (a) {
    links[a.getAttribute("href").slice(1)] = a;
  });

  var sections = Array.prototype.filter.call(
    document.querySelectorAll("[data-a-sec]"), function (s) { return links[s.id]; });
  if (!sections.length) return;

  var here = null;
  function mark(id) {
    if (id === here) return;
    if (here && links[here]) {
      links[here].classList.remove("is-here");
      links[here].removeAttribute("aria-current");
    }
    here = id;
    if (id && links[id]) {
      links[id].classList.add("is-here");
      links[id].setAttribute("aria-current", "true");
    }
  }

  /* A section counts as the one being read when it crosses the upper third of
     the screen. The observer reports both directions, so scrolling back up
     hands the mark back rather than leaving it stuck at the bottom. */
  var seen = {};
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { seen[e.target.id] = e.isIntersecting; });
    var current = null;
    for (var i = 0; i < sections.length; i++) {
      if (seen[sections[i].id]) { current = sections[i].id; break; }
    }
    mark(current);
  }, { rootMargin: "-33% 0px -55% 0px", threshold: 0 });

  sections.forEach(function (s) { io.observe(s); });

  window.addEventListener("pagehide", function () { io.disconnect(); }, { once: true });
})();
