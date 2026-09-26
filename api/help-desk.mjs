/* ===========================================================================
   NEWSPORTVISION — Help Desk endpoint
   ---------------------------------------------------------------------------
   One Vercel Function, and the only server code the site has. The Help Desk
   page posts its answers here; this checks every one of them again, then
   hands a plain message to Resend addressed to the office. Nothing is stored
   and nothing a visitor typed is ever logged.

   The visitor controls only the fields the form asks for. Who the message
   goes to, who it comes from and what it is called are decided here, so this
   cannot be used to send mail anywhere else.

   Configuration, server-side only:
     RESEND_API_KEY        required. Without it nothing is sent, and the page
                           is told so — it is never told that it worked.
     HELP_DESK_TO_EMAIL    optional, defaults to office@newsportvision.com
     HELP_DESK_FROM_EMAIL  optional, defaults to
                           NewSportVision Help Desk <helpdesk@send.newsportvision.com>
   =========================================================================== */

import { PERSON, WHO, SPORT, TOPIC_PERSON, TOPIC_ORG, INSURANCE }
  from "../lib/help-desk-options.mjs";

const TO_DEFAULT = "office@newsportvision.com";
const FROM_DEFAULT = "NewSportVision Help Desk <helpdesk@send.newsportvision.com>";
const RESEND_URL = "https://api.resend.com/emails";
const PROVIDER_TIMEOUT_MS = 8000;

/* The largest honest request is a few kilobytes: 5,000 characters of message
   and a handful of short fields. */
export const MAX_BODY_BYTES = 24 * 1024;
export const LIMIT = { name: 80, surname: 80, email: 254, phone: 40, message: 5000, page: 400 };

/* Reaching the form means answering up to three questions first. Nobody does
   that and fills in five fields in under two seconds. */
export const MIN_ELAPSED_MS = 2000;

/* Rate limiting is best effort, and said so. An instance of this function
   remembers for ten minutes who has just sent, so one address cannot pour
   requests through the same warm instance. Instances are not shared and do
   not outlive their idle period, so this bounds a burst rather than a
   determined sender; Resend's own limits and its plan's daily cap are the
   hard ceiling. A shared limit would need a store this site does not have. */
const WINDOW_MS = 10 * 60 * 1000;
const PER_ADDRESS = 5;
const PER_INSTANCE = 60;

const EMAIL = /^[^\s@<>()[\]\\,;:"]+@[^\s@<>()[\]\\,;:"]+\.[^\s@<>()[\]\\,;:".]{2,}$/;
const PHONE = /^[+0-9 ()./-]+$/;
const KEY = /^[0-9a-f-]{16,64}$/i;

const has = (map, key) =>
  typeof key === "string" && Object.prototype.hasOwnProperty.call(map, key);

function reply(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}
const refuse = (status, error, extra) => reply(status, { ok: false, error, ...extra });

/* Text arrives from a browser, so anything can be in it. Single lines lose
   control characters and repeated spaces; the message keeps its line breaks
   and nothing else invisible. Too long is refused rather than cut, so the
   visitor is never shown "sent" for words that were not. */
export function clean(value, max, multiline = false) {
  if (value == null) return "";
  if (typeof value !== "string") return null;
  let s = value.normalize("NFC");
  s = multiline
    ? s.replace(/\r\n?/g, "\n")
       .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "")
       .replace(/[ \t]+\n/g, "\n")
       .replace(/\n{3,}/g, "\n\n")
    : s.replace(/[\u0000-\u001F\u007F]+/g, " ").replace(/\s+/g, " ");
  s = s.trim();
  return s.length > max ? null : s;
}

/* Only the site's own page may be named as where the message came from. */
function pageOf(value, host) {
  if (typeof value !== "string" || value.length > LIMIT.page) return "";
  try {
    const u = new URL(value);
    return (u.protocol === "https:" || u.protocol === "http:") && u.host === host ? u.href : "";
  } catch {
    return "";
  }
}

/* Every answer is checked against the same lists the buttons are drawn from.
   A choice may be missing — some old links open the form directly — but one
   that is present has to be real, and has to belong to the branch it is in:
   a sport is asked only of an individual, and organisations have their own
   topics. */
export function validate(input, host) {
  const bad = [];
  const name = clean(input.name, LIMIT.name);
  const surname = clean(input.surname, LIMIT.surname);
  const email = clean(input.email, LIMIT.email);
  const phone = clean(input.phone, LIMIT.phone);
  const message = clean(input.message, LIMIT.message, true);
  const insurance = input.insurance == null ? "" : input.insurance;

  if (!name) bad.push("name");
  if (!surname) bad.push("surname");
  if (!email || !EMAIL.test(email)) bad.push("email");
  if (phone === null || (phone && (!PHONE.test(phone) || (phone.match(/\d/g) || []).length < 5))) {
    bad.push("phone");
  }
  if (insurance !== "" && !has(INSURANCE, insurance)) bad.push("insurance");
  if (!message) bad.push("message");
  if (input.terms !== true) bad.push("terms");

  let who = input.who == null ? "" : input.who;
  let sport = input.sport == null ? "" : input.sport;
  const topic = input.topic == null ? "" : input.topic;
  if (typeof who !== "string" || typeof sport !== "string" || typeof topic !== "string") {
    bad.push("selection");
  } else {
    if (!who && sport) who = PERSON;          // the page's own rule for old links
    if (who && !has(WHO, who)) {
      /* The branch is unknown, so the other two cannot be judged against it;
         one bad answer is reported once, not three times. */
      bad.push("who");
    } else {
      const person = who === PERSON;
      if (sport && (!person || !has(SPORT, sport))) bad.push("sport");
      const topics = !who ? { ...TOPIC_PERSON, ...TOPIC_ORG } : person ? TOPIC_PERSON : TOPIC_ORG;
      if (topic && !has(topics, topic)) bad.push("topic");
    }
  }

  return {
    ok: bad.length === 0,
    fields: bad,
    data: {
      name, surname, email, phone, message,
      insurance: typeof insurance === "string" ? insurance : "",
      who, sport, topic,
      lang: input.lang === "it" ? "it" : "en",
      page: pageOf(input.page, host),
    },
  };
}

export function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

function when(date) {
  try {
    return new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/Rome", dateStyle: "long", timeStyle: "short",
    }).format(date) + " (Rome)";
  } catch {
    return date.toISOString();
  }
}

/* The message the office reads: plain, in the order the questions were
   asked, and easy to scan on a phone. Every value is escaped for the HTML
   part, and the text part carries the same words for any client that
   prefers it. */
export function composeEmail(d, sentAt) {
  const topic = d.topic ? (TOPIC_PERSON[d.topic] || TOPIC_ORG[d.topic]) : "";
  const rows = [
    ["Name", d.name],
    ["Surname", d.surname],
    ["Email", d.email],
    ["Phone", d.phone],
    ["User/category", d.who ? WHO[d.who] : ""],
    ["Sport", d.sport ? SPORT[d.sport] : ""],
    ["Requested help/topic", topic],
    ["Insurance/policy", d.insurance ? INSURANCE[d.insurance] : ""],
  ];
  const meta = [
    ["Page URL", d.page],
    ["Submission time", when(sentAt)],
    ["Language", d.lang === "it" ? "Italian" : "English"],
  ];
  const dash = (v) => (v ? v : "—");

  const subject = ("NewSportVision Help Desk — " + d.name + " " + d.surname).slice(0, 180);

  const text = [
    "NEW SPORT VISION",
    "HELP DESK REQUEST",
    "",
    ...rows.map(([k, v]) => k + ": " + dash(v)),
    "",
    "Message:",
    d.message,
    "",
    ...meta.map(([k, v]) => k + ": " + dash(v)),
    "",
    "Reply to this email to answer " + d.name + " directly.",
  ].join("\n");

  const cell = "padding:7px 0;border-bottom:1px solid #DEDAD0;vertical-align:top;";
  const tr = ([k, v]) =>
    '<tr><td style="' + cell + 'width:190px;color:#6B6A64;font-size:13px;">' + escapeHtml(k) +
    '</td><td style="' + cell + 'font-size:15px;">' + escapeHtml(dash(v)) + "</td></tr>";
  const html =
    '<!doctype html><html><body style="margin:0;padding:28px 20px;background:#F2EFE7;' +
    'color:#1D1D1B;font-family:Helvetica,Arial,sans-serif;">' +
    '<div style="max-width:640px;margin:0 auto;">' +
    '<p style="margin:0;font-size:12px;font-weight:700;letter-spacing:.18em;">NEW SPORT VISION</p>' +
    '<h1 style="margin:6px 0 22px;font-size:24px;letter-spacing:.02em;">HELP DESK REQUEST</h1>' +
    '<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;">' +
    rows.map(tr).join("") + "</table>" +
    '<p style="margin:26px 0 8px;color:#6B6A64;font-size:13px;">Message</p>' +
    '<div style="font-size:16px;line-height:1.55;">' +
    escapeHtml(d.message).replace(/\n/g, "<br>") + "</div>" +
    '<table role="presentation" cellpadding="0" cellspacing="0" ' +
    'style="width:100%;border-collapse:collapse;margin-top:28px;">' +
    meta.map(tr).join("") + "</table>" +
    '<p style="margin:22px 0 0;color:#6B6A64;font-size:13px;">Reply to this email to answer ' +
    escapeHtml(d.name) + " directly.</p>" +
    "</div></body></html>";

  return { subject, text, html };
}

export function createLimiter() {
  const byAddress = new Map();
  let everyone = [];
  return {
    allow(address, now) {
      const since = now - WINDOW_MS;
      everyone = everyone.filter((t) => t > since);
      if (everyone.length >= PER_INSTANCE) return false;
      if (address) {
        const mine = (byAddress.get(address) || []).filter((t) => t > since);
        if (mine.length >= PER_ADDRESS) {
          byAddress.set(address, mine);
          return false;
        }
        mine.push(now);
        byAddress.set(address, mine);
        if (byAddress.size > 5000) {
          for (const [k, v] of byAddress) if (!v.some((t) => t > since)) byAddress.delete(k);
        }
      }
      everyone.push(now);
      return true;
    },
  };
}

/* Vercel sets both of these itself and overwrites whatever a client sends,
   so neither can be forged from outside. The address is held in memory for
   the rate limit and nowhere else. */
function addressOf(request) {
  const real = request.headers.get("x-real-ip");
  if (real) return real.trim();
  const forwarded = request.headers.get("x-forwarded-for") || "";
  return forwarded.split(",")[0].trim();
}

/* Only a configured address is used, and only one that could be an address:
   a stray line break in an environment variable must not become a header. */
function configured(value, fallback) {
  const v = typeof value === "string" ? value.trim() : "";
  return v && v.length <= 320 && !/[\r\n]/.test(v) && v.includes("@") ? v : fallback;
}

export async function sendWithResend({ apiKey, idempotencyKey, message }) {
  const headers = {
    authorization: "Bearer " + apiKey,
    "content-type": "application/json",
  };
  if (idempotencyKey) headers["idempotency-key"] = idempotencyKey;
  let res;
  try {
    res = await fetch(RESEND_URL, {
      method: "POST",
      headers,
      body: JSON.stringify(message),
      signal: AbortSignal.timeout(PROVIDER_TIMEOUT_MS),
    });
  } catch (err) {
    const name = err && err.name;
    return { kind: name === "TimeoutError" || name === "AbortError" ? "timeout" : "network" };
  }
  let body = null;
  try { body = await res.json(); } catch { /* not JSON: handled below */ }
  if (res.ok && body && typeof body.id === "string" && body.id) return { kind: "sent" };
  return {
    kind: res.ok ? "unexpected" : "refused",
    status: res.status,
    code: body && typeof body.name === "string" ? body.name.slice(0, 60) : "",
  };
}

const defaultLimiter = createLimiter();

export async function handle(request, deps = {}) {
  const env = deps.env || {};
  const send = deps.send || sendWithResend;
  const now = deps.now || Date.now;
  const limiter = deps.limiter || defaultLimiter;
  const log = deps.log || console;

  /* Only this site's own pages post here. A browser always names the page's
     origin on a POST, so a request from anywhere else — or from no page at
     all — is turned away before anything is read. */
  const host = request.headers.get("host") || new URL(request.url).host;
  let from = "";
  try { from = new URL(request.headers.get("origin") || "").host; } catch { from = ""; }
  if (!from || from !== host) return refuse(403, "forbidden");

  const type = (request.headers.get("content-type") || "").toLowerCase();
  if (!type.startsWith("application/json")) return refuse(415, "unsupported");
  if (Number(request.headers.get("content-length") || 0) > MAX_BODY_BYTES) {
    return refuse(413, "too_large");
  }
  let raw;
  try { raw = await request.text(); } catch { return refuse(400, "malformed"); }
  if (new TextEncoder().encode(raw).length > MAX_BODY_BYTES) return refuse(413, "too_large");
  let input;
  try { input = JSON.parse(raw); } catch { return refuse(400, "malformed"); }
  if (!input || typeof input !== "object" || Array.isArray(input)) return refuse(400, "malformed");

  /* The trap field is invisible to people, and a request that arrives faster
     than anyone could answer the questions is not a person either. Neither
     is told it worked: a person caught by accident would otherwise lose the
     message without knowing. */
  if (typeof input.website === "string" && input.website.trim() !== "") {
    return refuse(400, "rejected");
  }
  if (typeof input.elapsed !== "number" || !(input.elapsed >= MIN_ELAPSED_MS)) {
    return refuse(400, "rejected");
  }

  const checked = validate(input, host);
  if (!checked.ok) return refuse(422, "invalid", { fields: checked.fields });

  if (!limiter.allow(addressOf(request), now())) return refuse(429, "busy");

  const apiKey = typeof env.RESEND_API_KEY === "string" ? env.RESEND_API_KEY.trim() : "";
  if (!apiKey) {
    log.warn("help-desk: RESEND_API_KEY is not set, nothing was sent");
    return refuse(503, "unavailable");
  }

  const mail = composeEmail(checked.data, new Date(now()));
  const result = await send({
    apiKey,
    idempotencyKey: typeof input.key === "string" && KEY.test(input.key) ? "help-desk/" + input.key : "",
    message: {
      from: configured(env.HELP_DESK_FROM_EMAIL, FROM_DEFAULT),
      to: [configured(env.HELP_DESK_TO_EMAIL, TO_DEFAULT)],
      reply_to: checked.data.email,
      subject: mail.subject,
      html: mail.html,
      text: mail.text,
      tags: [{ name: "source", value: "help-desk" }],
    },
  });

  if (result.kind === "sent") return reply(200, { ok: true });
  if (result.kind === "timeout") {
    log.warn("help-desk: Resend did not answer in time");
    return refuse(504, "timeout");
  }
  if (result.kind === "refused" && result.status === 429) return refuse(503, "busy");
  if (result.kind === "refused" && result.status === 409) return refuse(409, "duplicate");
  /* Only the status and Resend's own error name are logged — never an
     address, a name or a word of the message. */
  log.warn("help-desk: Resend did not accept the message", result.kind, result.status || "", result.code || "");
  return refuse(502, "unavailable");
}

export function POST(request) {
  return handle(request, { env: process.env });
}
