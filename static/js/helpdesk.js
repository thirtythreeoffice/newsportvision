/* ===========================================================================
   NEWSPORTVISION — Help Desk
   ---------------------------------------------------------------------------
   The live site expressed this as 43 duplicated Wix pages: audience -> sport ->
   topic -> a contact form, copy-pasted once per branch, with slugs and titles
   that no longer matched each other. Every one of those choices survives here;
   it is simply one instrument instead of forty-three pages.

   Each state is addressable — /help-desk/?who=person&sport=basketball&topic=
   injuries — so all the old deep links still land where they meant to, and the
   browser's back button walks the tree the way it always should have.
   =========================================================================== */
(function () {
  "use strict";

  var root = document.querySelector(".hd");
  if (!root) return;

  var panels = root.querySelectorAll("[data-panel]");
  var steps = root.querySelectorAll(".hd-step");
  var orgWrap = root.querySelector("[data-org-topics]");
  var sportPanel = root.querySelector('[data-panel="2"]');
  var topicPanel = root.querySelector('[data-panel="3"]');
  var sportOpts = sportPanel ? sportPanel.querySelectorAll(".opts") : [];
  var generalTopics = topicPanel ? topicPanel.querySelector(".opts") : null;
  var summary = root.querySelector("[data-summary]");
  var form = root.querySelector("[data-hd-form]");
  var status = root.querySelector("[data-hd-status]");
  var resetBtn = root.querySelector("[data-hd-reset]");

  /* An individual is asked which sport. An organisation is not — it is asked
     what kind of programme it needs. That is how the original tree branched. */
  var PERSON = "person";

  var state = { who: "", sport: "", topic: "", step: 1 };

  /* Every answer this instrument accepts is one of its own buttons. The
     values arrive from the address bar, where anything can be typed, so they
     are looked up among the buttons rather than written into a selector: a
     quote in a hand-edited link used to throw on load, and since the bad value
     stayed in the state, every tap after it threw again. All 172 legacy links
     into this page name values that are buttons, so none of them is refused. */
  var byGroup = Object.create(null);
  Array.prototype.forEach.call(root.querySelectorAll(".opt[data-group]"), function (b) {
    var g = byGroup[b.dataset.group] || (byGroup[b.dataset.group] = Object.create(null));
    g[b.dataset.value] = b;
  });

  function option(group, value) {
    var g = byGroup[group];
    return (g && value && g[value]) || null;
  }

  function known(group, value) { return option(group, value) ? value : ""; }

  function labelFor(group, value) {
    var btn = option(group, value);
    return btn ? btn.querySelector(".opt__name").textContent.trim() : value;
  }

  function stepsAvailable() {
    return state.who && state.who !== PERSON ? [1, 3, 4] : [1, 2, 3, 4];
  }

  function render() {
    var avail = stepsAvailable();
    if (avail.indexOf(state.step) === -1) state.step = avail[0];

    Array.prototype.forEach.call(panels, function (p) {
      p.hidden = parseInt(p.dataset.panel, 10) !== state.step;
    });

    /* Organisations get the programme list; individuals get the sport topics. */
    if (orgWrap && generalTopics) {
      var org = state.who && state.who !== PERSON;
      orgWrap.hidden = !org;
      generalTopics.hidden = org;
    }

    Array.prototype.forEach.call(steps, function (s) {
      var n = parseInt(s.dataset.step, 10);
      var slot = s.querySelector("[data-slot]");
      var key = slot ? slot.dataset.slot : null;
      var val = key ? state[key] : "";
      if (key && val) {
        if (!slot.dataset.base) slot.dataset.base = slot.textContent;
        slot.textContent = labelFor(key === "who" ? "who" : key, val);
      } else if (slot && slot.dataset.base) {
        slot.textContent = slot.dataset.base;
      }
      s.dataset.state = n === state.step ? "active" : (val ? "done" : "");
      s.hidden = avail.indexOf(n) === -1 && n !== 4;
    });

    Array.prototype.forEach.call(root.querySelectorAll(".opt"), function (b) {
      var g = b.dataset.group;
      b.setAttribute("aria-pressed", state[g] === b.dataset.value ? "true" : "false");
    });

    if (summary) {
      var bits = [];
      if (state.who) bits.push(labelFor("who", state.who));
      if (state.sport) bits.push(labelFor("sport", state.sport));
      if (state.topic) bits.push(labelFor("topic", state.topic));
      summary.textContent = bits.join("  /  ");
      summary.hidden = !bits.length;
    }

  }

  /* A choice the visitor makes is a new history entry, so the back button
     walks back up the tree; restoring a state (on load, or from back/forward)
     only rewrites the current entry. */
  function writeUrl(push) {
    var q = [];
    ["who", "sport", "topic"].forEach(function (k) {
      if (state[k]) q.push(k + "=" + encodeURIComponent(state[k]));
    });
    if (state.step === 4) q.push("step=contact");
    var url = location.pathname + (q.length ? "?" + q.join("&") : "");
    if (url === location.pathname + location.search) return;
    if (push) history.pushState({ hd: 1 }, "", url);
    else history.replaceState(history.state, "", url);
  }

  function readUrl() {
    var p = new URLSearchParams(location.search);
    state.who = known("who", p.get("who"));
    state.sport = known("sport", p.get("sport"));
    state.topic = known("topic", p.get("topic"));

    /* A legacy link that named a sport but no audience was, by definition, a
       person asking about that sport. */
    if (state.sport && !state.who) state.who = PERSON;

    if (p.get("step") === "contact") state.step = 4;
    else if (state.topic) state.step = 4;
    else if (state.who && state.who !== PERSON) state.step = 3;
    else if (state.sport) state.step = 3;
    else if (state.who) state.step = 2;
    else state.step = 1;
  }

  var smooth = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* The new question takes focus, and if the visitor had scrolled down a long
     list to answer the last one, the instrument comes back into view — on a
     phone the next question would otherwise be above the screen. */
  function focusPanel() {
    var p = root.querySelector('[data-panel="' + state.step + '"]');
    if (!p) return;
    var h = p.querySelector(".hd-q");
    if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
    var steps = root.querySelector(".hd-steps") || p;
    var top = steps.getBoundingClientRect().top;
    var pad = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
    if (top < pad || top > window.innerHeight * 0.6) {
      window.scrollTo({ top: window.scrollY + top - pad, behavior: smooth ? "smooth" : "auto" });
    }
  }

  /* The panel under a finger changes the moment an option is chosen. A quick
     second tap would land on whatever option now sits in the same place, and
     answer a question the visitor has not read yet. */
  var settledAt = 0;
  var SETTLE = 350;

  function go() {
    render();
    writeUrl(true);
    settledAt = Date.now();
    /* A line about the last send belongs to the answers it was sent with;
       once the visitor changes an answer it is no longer true. Never while
       a send is still on its way — that line is the only sign of it. */
    if (!sending) say("");
    focusPanel();
  }

  root.addEventListener("click", function (e) {
    var opt = e.target.closest(".opt");
    if (opt) {
      if (Date.now() - settledAt < SETTLE) { e.preventDefault(); return; }
      var g = opt.dataset.group;
      state[g] = opt.dataset.value;
      if (g === "who") {
        /* A different audience invalidates what was chosen under the old one. */
        state.sport = ""; state.topic = "";
        state.step = (state[g] === PERSON) ? 2 : 3;
      } else if (g === "sport") { state.topic = ""; state.step = 3; }
      else if (g === "topic") state.step = 4;
      go();
      return;
    }
    var back = e.target.closest("[data-back]");
    if (back) {
      var to = parseInt(back.dataset.back, 10);
      var avail = stepsAvailable();
      while (to > 1 && avail.indexOf(to) === -1) to--;
      state.step = to;
      if (to <= 3) state.topic = "";
      if (to <= 2) state.sport = "";
      if (to <= 1) state.who = "";
      go();
    }
  });

  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      state = { who: "", sport: "", topic: "", step: 1 };
      if (form) form.reset();
      forget();
      say("");
      go();
    });
  }

  /* ---------------------------------------------------------------------
     Submission.
     The answers and the form go to this site's own Help Desk endpoint, which
     checks them again and hands them to Resend for the office. The page says
     the message has gone only when the endpoint says Resend has taken it.
     Anything else keeps every word the visitor typed and lets them send
     again; nothing is kept anywhere once the page is closed.
     --------------------------------------------------------------------- */
  var ENDPOINT = form ? form.getAttribute("action") : "";
  var openedAt = Date.now();
  var sending = false;
  var lastBody = "", lastKey = "";
  var submit = form ? form.querySelector('button[type="submit"]') : null;

  function say(to) {
    if (!form) return;
    if (to) form.setAttribute("data-state", to); else form.removeAttribute("data-state");
    if (status) status.textContent = to ? (form.getAttribute("data-" + to) || "") : "";
    var busy = to === "sending";
    form.setAttribute("aria-busy", busy ? "true" : "false");
    if (submit) submit.disabled = busy;
  }

  function forget() { lastBody = ""; lastKey = ""; }

  function newKey() {
    var c = window.crypto;
    if (c && c.randomUUID) return c.randomUUID();
    var bytes = new Uint8Array(16);
    c.getRandomValues(bytes);
    return Array.prototype.map.call(bytes, function (b) { return (b + 256).toString(16).slice(1); }).join("");
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (sending) return;                       // a second press while the first is on its way
      if (!form.reportValidity()) return;

      var d = new FormData(form);
      var field = function (k) { return (d.get(k) || "").toString(); };
      var answer = {
        who: state.who, sport: state.sport, topic: state.topic,
        name: field("name"), surname: field("surname"), email: field("email"),
        phone: field("phone"), insurance: field("insurance"), message: field("message"),
        terms: !!(form.elements.terms && form.elements.terms.checked),
        website: field("website"),
        lang: document.documentElement.lang === "it" ? "it" : "en"
      };
      /* Sent again unchanged — after a dropped connection, say — a request
         keeps its key, so if the first attempt did reach Resend the second
         cannot deliver the message twice. A changed request is a new one. */
      var body = JSON.stringify(answer);
      if (body !== lastBody) { lastBody = body; lastKey = newKey(); }
      answer.key = lastKey;
      answer.page = location.href;
      answer.elapsed = Date.now() - openedAt;

      sending = true;
      say("sending");
      var abort = "AbortController" in window ? new AbortController() : null;
      var timer = abort ? setTimeout(function () { abort.abort(); }, 20000) : 0;

      fetch(ENDPOINT, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(answer),
        credentials: "same-origin",
        signal: abort ? abort.signal : undefined
      })
        .then(function (res) {
          return res.json()
            .catch(function () { return {}; })
            .then(function (r) {
              return { ok: res.ok && !!r && r.ok === true, error: r && r.error };
            });
        })
        .catch(function () { return { ok: false, error: "network" }; })
        .then(function (r) {
          clearTimeout(timer);
          sending = false;
          if (r.ok) {
            /* Only now: the office has it. The fields empty so the same words
               cannot be sent twice by accident; the answers above stay, so the
               visitor can see what the message was about. */
            form.reset();
            forget();
            say("sent");
          } else {
            say(r.error === "busy" ? "busy" : "failed");
          }
        });
    });

    /* A line about the last attempt stops being true the moment the visitor
       starts on the next one. */
    form.addEventListener("input", function () {
      if (!sending && form.hasAttribute("data-state")) say("");
    });
  }

  window.addEventListener("popstate", function () {
    readUrl();
    render();
    if (!sending) say("");
    settledAt = Date.now();
    focusPanel();
  });

  readUrl();
  render();
  writeUrl(false);
})();
