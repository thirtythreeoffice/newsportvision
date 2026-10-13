/* ===========================================================================
   NEWSPORTVISION — FSF2026
   ---------------------------------------------------------------------------
   Three small things, each of which the page works without: the declaration
   is sent, a photograph opens large, a hosted film is fetched only when it is
   asked for. No library.
   =========================================================================== */
(function () {
  "use strict";

  /* --- The declaration ---------------------------------------------------
     It goes to this site's own endpoint, which checks it again and passes it
     to the office. The page says it has gone only when that is confirmed;
     otherwise everything written stays where it is. The faint example on each
     line is a placeholder, so it is never a value and is never sent. */
  var form = document.querySelector("[data-fsf-form]");
  if (form) {
    var status = form.querySelector("[data-fsf-status]");
    var submit = form.querySelector('button[type="submit"]');
    var openedAt = Date.now();
    var sending = false, lastBody = "", lastKey = "";

    var say = function (to) {
      if (to) form.setAttribute("data-state", to); else form.removeAttribute("data-state");
      if (status) status.textContent = to ? (form.getAttribute("data-" + to) || "") : "";
      var busy = to === "sending";
      form.setAttribute("aria-busy", busy ? "true" : "false");
      if (submit) submit.disabled = busy;
    };
    var newKey = function () {
      var c = window.crypto;
      if (c && c.randomUUID) return c.randomUUID();
      var b = new Uint8Array(16); c.getRandomValues(b);
      return Array.prototype.map.call(b, function (x) { return (x + 256).toString(16).slice(1); }).join("");
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (sending) return;
      var name = form.elements.name.value.trim();
      var from = form.elements.from.value.trim();
      if (!name || !from || !form.elements.consent.checked) {
        say("missing");
        (!name ? form.elements.name : !from ? form.elements.from : form.elements.consent).focus();
        return;
      }
      var answer = {
        name: name, from: from, consent: true,
        website: form.elements.website.value,
        lang: document.documentElement.lang === "it" ? "it" : "en"
      };
      var body = JSON.stringify(answer);
      if (body !== lastBody) { lastBody = body; lastKey = newKey(); }
      answer.key = lastKey;
      answer.page = location.href;
      answer.elapsed = Date.now() - openedAt;

      sending = true;
      say("sending");
      var abort = "AbortController" in window ? new AbortController() : null;
      var timer = abort ? setTimeout(function () { abort.abort(); }, 20000) : 0;
      fetch(form.getAttribute("action"), {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify(answer), credentials: "same-origin",
        signal: abort ? abort.signal : undefined
      })
        .then(function (res) {
          return res.json().catch(function () { return {}; }).then(function (r) {
            return { ok: res.ok && !!r && r.ok === true, error: r && r.error };
          });
        })
        .catch(function () { return { ok: false, error: "network" }; })
        .then(function (r) {
          clearTimeout(timer);
          sending = false;
          if (r.ok) { form.reset(); lastBody = ""; lastKey = ""; say("sent"); }
          else say(r.error === "busy" ? "busy" : r.error === "invalid" ? "missing" : "failed");
        });
    });
    form.addEventListener("input", function () {
      if (!sending && form.hasAttribute("data-state")) say("");
    });
  }

  /* --- A hosted film ------------------------------------------------------
     Nothing is requested from YouTube or Vimeo, and no cookie of theirs is
     set, until the visitor presses play. */
  Array.prototype.forEach.call(document.querySelectorAll(".fsf-play"), function (btn) {
    btn.addEventListener("click", function () {
      var yt = btn.getAttribute("data-youtube"), vm = btn.getAttribute("data-vimeo");
      var frame = document.createElement("iframe");
      frame.src = yt
        ? "https://www.youtube-nocookie.com/embed/" + encodeURIComponent(yt) + "?autoplay=1&rel=0"
        : "https://player.vimeo.com/video/" + encodeURIComponent(vm) + "?autoplay=1&dnt=1";
      frame.title = btn.getAttribute("aria-label") || "";
      frame.allow = "autoplay; fullscreen; picture-in-picture";
      frame.allowFullscreen = true;
      frame.style.aspectRatio = btn.style.aspectRatio || "16 / 9";
      btn.parentNode.replaceChild(frame, btn);
      frame.focus();
    });
  });

  /* --- A photograph, large ------------------------------------------------
     A <dialog>, so the browser itself holds focus inside it and Escape closes
     it. Without this script each picture is still a link to its own file. */
  var lb = document.querySelector("[data-fsf-lb]");
  var shots = Array.prototype.slice.call(document.querySelectorAll("[data-fsf-shot]"));
  if (!lb || !shots.length || !lb.showModal) return;

  var img = lb.querySelector("[data-lb-img]");
  var cap = lb.querySelector("[data-lb-cap]");
  var prev = lb.querySelector("[data-lb-prev]");
  var next = lb.querySelector("[data-lb-next]");
  var at = 0, opener = null;

  function show(i) {
    at = (i + shots.length) % shots.length;
    var a = shots[at], thumb = a.querySelector("img");
    img.removeAttribute("srcset");
    img.src = a.getAttribute("href");
    img.setAttribute("srcset", a.getAttribute("data-srcset") || "");
    img.sizes = "100vw";
    img.width = +a.getAttribute("data-w"); img.height = +a.getAttribute("data-h");
    img.alt = thumb ? thumb.alt : "";
    cap.textContent = a.getAttribute("data-caption") || "";
    var many = shots.length > 1;
    prev.hidden = next.hidden = !many;
    /* have the neighbour ready, so the next one does not arrive blank */
    if (many) { var n = new Image(); n.src = shots[(at + 1) % shots.length].getAttribute("href"); }
  }

  shots.forEach(function (a, i) {
    a.addEventListener("click", function (e) {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
      e.preventDefault();
      opener = a;
      show(i);
      lb.showModal();
    });
  });
  prev.addEventListener("click", function () { show(at - 1); });
  next.addEventListener("click", function () { show(at + 1); });
  lb.querySelector("[data-lb-close]").addEventListener("click", function () { lb.close(); });
  lb.addEventListener("click", function (e) { if (e.target === lb) lb.close(); });
  lb.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { e.preventDefault(); show(at - 1); }
    else if (e.key === "ArrowRight") { e.preventDefault(); show(at + 1); }
  });
  lb.addEventListener("close", function () {
    img.removeAttribute("srcset"); img.removeAttribute("src");
    if (opener && opener.focus) opener.focus({ preventScroll: true });
  });

  /* A sideways drag of a finger turns the page; a mostly vertical one is left
     to the browser. */
  var x0 = null, y0 = 0;
  var fig = lb.querySelector(".fsf-lb__fig");
  fig.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") { x0 = e.clientX; y0 = e.clientY; } });
  fig.addEventListener("pointerup", function (e) {
    if (x0 === null) return;
    var dx = e.clientX - x0, dy = e.clientY - y0; x0 = null;
    if (Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(dy) * 1.5) show(at + (dx < 0 ? 1 : -1));
  });
  fig.addEventListener("pointercancel", function () { x0 = null; });
})();
