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
      if (status) status.textContent = "";
      go();
    });
  }

  /* ---------------------------------------------------------------------
     Submission.
     There is no back end behind this build, and inventing one that silently
     drops enquiries would be worse than none. The form therefore composes the
     message and hands it to the visitor's mail client, addressed to the same
     address the site already publishes. Swap this one function for a POST when
     an endpoint exists; nothing else has to change.
     --------------------------------------------------------------------- */
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;

      var d = new FormData(form);
      var lines = [];
      ["who", "sport", "topic"].forEach(function (k) {
        if (state[k]) lines.push(k.toUpperCase() + ": " + labelFor(k, state[k]));
      });
      lines.push("");
      [["name", "Name"], ["surname", "Surname"], ["email", "Email"],
       ["phone", "Phone"], ["insurance", "Polizza"]].forEach(function (pair) {
        var v = (d.get(pair[0]) || "").toString().trim();
        if (v) lines.push(pair[1] + ": " + v);
      });
      var msg = (d.get("message") || "").toString().trim();
      if (msg) { lines.push(""); lines.push(msg); }

      var subject = "NSV Help Desk — " +
        ["who", "sport", "topic"].filter(function (k) { return state[k]; })
          .map(function (k) { return labelFor(k, state[k]); }).join(" / ");

      var href = "mailto:office@newsportvision.com?subject=" +
        encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));

      if (status) status.textContent = form.dataset.sent || "";
      window.location.href = href;
    });
  }

  window.addEventListener("popstate", function () {
    readUrl();
    render();
    settledAt = Date.now();
    focusPanel();
  });

  readUrl();
  render();
  writeUrl(false);
})();
