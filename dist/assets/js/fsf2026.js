/* ===========================================================================
   NEWSPORTVISION — FSF2026
   ---------------------------------------------------------------------------
   Three small things, each of which the page works without: the declaration
   is sent, a photograph opens large, a hosted film is fetched only when it is
   asked for. No library.
   =========================================================================== */
(function () {
  "use strict";

  /* --- The tree --------------------------------------------------------
     Its growth is CSS, started by the house's reveal sweep. Here only the
     breeze afterwards: it begins when the last leaves have opened, and rests
     whenever the tree is off screen or the tab is hidden. */
  var plate = document.querySelector(".fsf-plate");
  if (plate) {
    var last = plate.querySelector(".tos-leaves-9");
    var idle = function () { plate.classList.add("is-idle"); };
    if (last) last.addEventListener("animationend", idle, { once: true });
    var onScreen = true;
    var rest = function () { plate.classList.toggle("is-paused", !onScreen || document.hidden); };
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { onScreen = es[0].isIntersecting; rest(); }).observe(plate);
    }
    document.addEventListener("visibilitychange", rest);
  }

  /* --- The staircase -----------------------------------------------------
     One straight line falling under the five words, as in the manifesto. It
     is redrawn
     here in the page's own pixels — a stretched drawing has no honest length,
     and Safari will not dash one — so that it can be drawn along as the
     section arrives. Without this the stair is simply there. */
  var stair = document.querySelector("[data-fsf-stair]");
  if (stair) {
    var svg = stair.querySelector("svg"), path = svg && svg.querySelector("path");
    var lastW = 0, lastH = 0;
    var draw = function () {
      var w = svg.clientWidth, h = svg.clientHeight;
      if (!w || !h || (w === lastW && h === lastH)) return;
      lastW = w; lastH = h;
      var d = "M0 " + (h / 6) + "L" + w + " " + h;
      svg.setAttribute("viewBox", "0 0 " + w + " " + h);
      path.removeAttribute("vector-effect");
      path.setAttribute("d", d);
      path.style.setProperty("--len", Math.ceil(path.getTotalLength()) + 1);
      path.setAttribute("data-len", "");
    };
    if (path) {
      draw();
      if ("ResizeObserver" in window) new ResizeObserver(draw).observe(svg);
      else window.addEventListener("resize", draw);
    }
  }

  /* --- The declaration ---------------------------------------------------
     It goes to this site's own endpoint, which checks it again, keeps it and
     passes it to the office. The page says it is signed only when the
     endpoint answers with its number; otherwise everything written stays.
     The faint example on each line is a placeholder: never a value. */
  var form = document.querySelector("[data-fsf-form]");
  if (form) {
    var status = form.querySelector("[data-fsf-status]");
    var submit = form.querySelector('button[type="submit"]');
    var openedAt = Date.now();
    var sending = false, done = false, lastBody = "", lastKey = "";
    var lang = document.documentElement.lang === "it" ? "it" : "en";
    var NAME_RE, FROM_RE, EMAIL_RE = /^[^\s@<>()[\]\\,;:"]{1,64}@[^\s@<>()[\]\\,;:"]+\.[^\s@<>()[\]\\,;:".]{2,}$/;
    try {
      NAME_RE = new RegExp("^[\\p{L}\\p{M}][\\p{L}\\p{M} .'’‐-]*$", "u");
      FROM_RE = new RegExp("^[\\p{L}\\p{M}\\p{N}][\\p{L}\\p{M}\\p{N} .,'’‐&()/-]*$", "u");
    } catch (e) { NAME_RE = FROM_RE = /./; }   // very old engines: the server still checks
    var chars = function (s) { return Array.from ? Array.from(s).length : s.length; };
    var tidy = function (s) { return (s || "").normalize ? s.normalize("NFC").replace(/\s+/g, " ").trim() : (s || "").trim(); };

    var say = function (to, text) {
      if (to) form.setAttribute("data-state", to); else form.removeAttribute("data-state");
      if (status) status.textContent = text != null ? text : (to ? (form.getAttribute("data-" + to) || "") : "");
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
    var field = function (name) { return name === "consent" ? form.elements.consent : form.elements[name]; };
    var showErrors = function (list) {
      Array.prototype.forEach.call(form.querySelectorAll(".fsf-err[data-for]"), function (li) {
        var f = li.getAttribute("data-for"), on = list.indexOf(f) !== -1;
        li.hidden = !on;
        var el = f === "signature" ? null : field(f);
        if (!el) return;
        /* the reason is part of the field's description only while it shows */
        var ids = (el.getAttribute("aria-describedby") || "").split(" ").filter(function (x) { return x && x !== li.id; });
        if (on) { el.setAttribute("aria-invalid", "true"); ids.push(li.id); } else el.removeAttribute("aria-invalid");
        if (ids.length) el.setAttribute("aria-describedby", ids.join(" ")); else el.removeAttribute("aria-describedby");
      });
    };

    /* the blank grows with what is written, where the browser cannot do it */
    var grow = (function () {
      var ctx = document.createElement("canvas").getContext("2d");
      return function (input) {
        var cs = getComputedStyle(input);
        ctx.font = cs.fontStyle + " " + cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
        var fs = parseFloat(cs.fontSize), w = ctx.measureText(input.value || input.placeholder || "").width;
        input.style.width = Math.ceil(Math.max(w + fs * .7, fs * (input.name === "from" ? 4.8 : 6.2))) + "px";
      };
    })();
    ["name", "from"].forEach(function (n) {
      var el = form.elements[n]; grow(el);
      el.addEventListener("input", function () { grow(el); });
    });
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { grow(form.elements.name); grow(form.elements.from); });

    /* --- the signature pad: a mouse, a finger or a pen, on the horizon --- */
    var pad = form.querySelector("[data-fsf-pad]");
    var canvas = pad && pad.querySelector("canvas");
    var clearBtn = pad && pad.querySelector("[data-fsf-clear]");
    var ink = false, strokes = [], current = null;
    var ctx2 = canvas && canvas.getContext("2d");
    var fit = function () {
      if (!canvas) return;
      var r = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 3);
      canvas.width = Math.max(1, Math.round(r.width * dpr)); canvas.height = Math.max(1, Math.round(r.height * dpr));
      ctx2.setTransform(dpr, 0, 0, dpr, 0, 0);
      redraw();
    };
    var drawStroke = function (s) {
      if (!s.length) return;
      ctx2.beginPath(); ctx2.moveTo(s[0].x, s[0].y);
      if (s.length === 1) { ctx2.lineTo(s[0].x + .1, s[0].y + .1); }
      for (var i = 1; i < s.length - 1; i++) {
        var mx = (s[i].x + s[i + 1].x) / 2, my = (s[i].y + s[i + 1].y) / 2;
        ctx2.quadraticCurveTo(s[i].x, s[i].y, mx, my);
      }
      if (s.length > 1) ctx2.lineTo(s[s.length - 1].x, s[s.length - 1].y);
      ctx2.stroke();
    };
    var redraw = function () {
      if (!ctx2) return;
      var r = canvas.getBoundingClientRect();
      ctx2.clearRect(0, 0, r.width, r.height);
      ctx2.lineCap = "round"; ctx2.lineJoin = "round"; ctx2.strokeStyle = "#1D1D1B"; ctx2.lineWidth = 2.4;
      // strokes are kept in fractions of the box, so a resize keeps the drawing
      strokes.forEach(function (s) { drawStroke(s.map(function (p) { return { x: p.x * r.width, y: p.y * r.height }; })); });
    };
    if (canvas && canvas.getContext && window.PointerEvent) {
      var at = function (e) { var r = canvas.getBoundingClientRect(); return { x: (e.clientX - r.left) / r.width, y: (e.clientY - r.top) / r.height }; };
      canvas.addEventListener("pointerdown", function (e) {
        if (done) return;
        e.preventDefault();
        try { canvas.setPointerCapture(e.pointerId); } catch (err) { /* fine */ }
        current = [at(e)]; strokes.push(current); redraw();
      });
      canvas.addEventListener("pointermove", function (e) {
        if (!current) return;
        e.preventDefault();
        var evs = e.getCoalescedEvents ? e.getCoalescedEvents() : [e];
        evs.forEach(function (ev) { current.push(at(ev)); });
        redraw();
      });
      var end = function () {
        if (!current) return;
        current = null; ink = true; pad.classList.add("has-ink"); clearBtn.disabled = false;
        showErrors(currentErrors.filter(function (f) { return f !== "signature"; }));
      };
      canvas.addEventListener("pointerup", end);
      canvas.addEventListener("pointercancel", end);
      clearBtn.addEventListener("click", function () {
        strokes = []; ink = false; pad.classList.remove("has-ink"); clearBtn.disabled = true; redraw();
      });
      if ("ResizeObserver" in window) new ResizeObserver(fit).observe(canvas); else window.addEventListener("resize", fit);
      fit();
    } else if (pad) { pad.hidden = true; }

    /* the drawing, cropped to the ink and kept small: a PNG of at most 600 px */
    var signatureData = function () {
      if (!ink || !strokes.length) return "";
      var r = canvas.getBoundingClientRect(), minx = 1, miny = 1, maxx = 0, maxy = 0;
      strokes.forEach(function (s) { s.forEach(function (p) { minx = Math.min(minx, p.x); miny = Math.min(miny, p.y); maxx = Math.max(maxx, p.x); maxy = Math.max(maxy, p.y); }); });
      var pad8 = 8, w = (maxx - minx) * r.width + pad8 * 2, h = (maxy - miny) * r.height + pad8 * 2;
      var scale = Math.min(1, 600 / w, 200 / h);
      var out = document.createElement("canvas");
      out.width = Math.max(1, Math.round(w * scale)); out.height = Math.max(1, Math.round(h * scale));
      var c = out.getContext("2d");
      c.setTransform(scale, 0, 0, scale, 0, 0);
      c.lineCap = "round"; c.lineJoin = "round"; c.strokeStyle = "#1D1D1B"; c.lineWidth = 2.4;
      var keep = ctx2; ctx2 = c;
      strokes.forEach(function (s) { drawStroke(s.map(function (p) { return { x: (p.x - minx) * r.width + pad8, y: (p.y - miny) * r.height + pad8 }; })); });
      ctx2 = keep;
      return out.toDataURL("image/png");
    };

    var currentErrors = [];
    var check = function (a) {
      var bad = [];
      if (chars(a.name) < 2 || chars(a.name) > 80 || !NAME_RE.test(a.name)) bad.push("name");
      if (chars(a.from) < 2 || chars(a.from) > 120 || !FROM_RE.test(a.from)) bad.push("from");
      if (a.email && (a.email.length > 254 || !EMAIL_RE.test(a.email))) bad.push("email");
      if (a.signature && a.signature.length > 272000 + 22) bad.push("signature");
      if (!a.consent) bad.push("consent");
      return bad;
    };

    /* signed: the sentence is set, the drawing stays, the seal comes down */
    var lock = function (r, a) {
      ["name", "from"].forEach(function (n) {
        var el = form.elements[n], span = document.createElement("span");
        span.className = "fsf-line__set"; span.textContent = a[n];
        el.parentNode.replaceChild(span, el);
      });
      var stamp = form.querySelector("[data-fsf-stamp]"), who = form.querySelector("[data-fsf-supporter]");
      if (r.no) {
        stamp.textContent = (form.getAttribute("data-seal") || "").replace("%s", r.no).replace("%s", r.day || "");
        who.textContent = (form.getAttribute("data-supporter") || "").replace("%s", String(r.n));
      } else { stamp.textContent = form.getAttribute("data-sent") || ""; who.textContent = ""; }
      form.querySelector("[data-fsf-signed]").hidden = false;
      done = true;
      say("sent", "");
      if (status) status.textContent = (stamp.textContent + " " + who.textContent).trim();
      if (form.getBoundingClientRect().top < 0) form.scrollIntoView({ block: "start", behavior: "smooth" });
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (sending || done) return;
      var typeEl = form.querySelector('input[name="type"]:checked');
      var answer = {
        name: tidy(form.elements.name.value), from: tidy(form.elements.from.value),
        email: tidy(form.elements.email.value), type: typeEl ? typeEl.value : "",
        signature: signatureData(), wall: form.elements.wall.checked,
        consent: form.elements.consent.checked, website: form.elements.website.value, lang: lang
      };
      currentErrors = check(answer);
      showErrors(currentErrors);
      if (currentErrors.length) {
        say("missing");
        var first = currentErrors[0];
        (first === "signature" ? clearBtn : field(first)).focus();
        return;
      }
      if (navigator.onLine === false) { say("offline"); return; }
      var body = JSON.stringify(answer);
      if (body !== lastBody) { lastBody = body; lastKey = newKey(); }
      answer.key = lastKey; answer.page = location.href; answer.elapsed = Date.now() - openedAt;

      sending = true;
      say("sending");
      var abort = "AbortController" in window ? new AbortController() : null;
      var timer = abort ? setTimeout(function () { abort.abort(); }, 20000) : 0;
      fetch(form.getAttribute("action"), {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify(answer), credentials: "same-origin", signal: abort ? abort.signal : undefined
      })
        .then(function (res) {
          return res.json().catch(function () { return {}; }).then(function (r) {
            r = r || {}; r.status = res.status; r.ok = res.ok && r.ok === true; return r;
          });
        })
        .catch(function () { return { ok: false, error: navigator.onLine === false ? "offline" : "network" }; })
        .then(function (r) {
          clearTimeout(timer);
          sending = false;
          if (r.ok) return lock(r, answer);
          if (r.error === "invalid" && r.fields) { currentErrors = r.fields; showErrors(r.fields); say("missing"); return; }
          say({ busy: "busy", duplicate: "dup", offline: "offline", unavailable: "unavailable" }[r.error] || "failed");
        });
    });
    form.addEventListener("input", function (e) {
      if (sending || done) return;
      if (form.hasAttribute("data-state")) say("");
      var n = e.target && e.target.name;
      if (n && currentErrors.indexOf(n) !== -1) { currentErrors = currentErrors.filter(function (f) { return f !== n; }); showErrors(currentErrors); }
    });
    window.addEventListener("online", function () { if (form.getAttribute("data-state") === "offline") say(""); });
  }

  /* --- The wall of supporters: names given for it, nothing else --------- */
  var wallBox = document.querySelector("[data-fsf-wall]");
  if (wallBox && window.fetch) {
    fetch("/api/support/", { headers: { accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : { wall: [] }; })
      .then(function (j) {
        var list = (j && j.wall) || [];
        if (!list.length) return;
        var ol = wallBox.querySelector("[data-fsf-wall-list]");
        list.forEach(function (w) {
          var li = document.createElement("li"), b = document.createElement("b"), small = document.createElement("small");
          b.textContent = w.name; small.textContent = w.from + (document.documentElement.lang === "it" ? " · N. " : " · No. ") + w.no;
          li.appendChild(b); li.appendChild(small); ol.appendChild(li);
        });
        wallBox.hidden = false;
      })
      .catch(function () { /* the wall is a courtesy; nothing to say */ });
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
