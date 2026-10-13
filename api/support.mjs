/* ===========================================================================
   NEWSPORTVISION — Support for the Values
   ---------------------------------------------------------------------------
   The declaration on the FSF2026 page arrives here: a name and where the
   signer is from, nothing else. It is checked and sent to the office through
   Resend — the same route, key and guards as the Help Desk, whose tested
   pieces this file borrows rather than repeats. Nothing is stored here and
   nothing a visitor typed is logged. There is no public list of signers.
   =========================================================================== */

import { clean, escapeHtml, createLimiter, sendWithResend } from "./help-desk.mjs";

const TO_DEFAULT = "office@newsportvision.com";
const FROM_DEFAULT = "NewSportVision Help Desk <helpdesk@send.newsportvision.com>";
const MAX_BODY_BYTES = 8 * 1024;
const LIMIT = 80;
/* Two short lines and a tick take a person a few seconds at least. */
const MIN_ELAPSED_MS = 2000;
const KEY = /^[0-9a-f-]{16,64}$/i;

const reply = (status, body) => new Response(JSON.stringify(body), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" },
});
const refuse = (status, error, extra) => reply(status, { ok: false, error, ...extra });

const configured = (value, fallback) => {
  const v = typeof value === "string" ? value.trim() : "";
  return v && v.length <= 320 && !/[\r\n]/.test(v) && v.includes("@") ? v : fallback;
};

export function validate(input) {
  const bad = [];
  const name = clean(input.name, LIMIT);
  const from = clean(input.from, LIMIT);
  if (!name) bad.push("name");
  if (!from) bad.push("from");
  if (input.consent !== true) bad.push("consent");
  return { ok: bad.length === 0, fields: bad, data: { name, from, lang: input.lang === "it" ? "it" : "en" } };
}

export function composeEmail(d, sentAt, page) {
  let when;
  try {
    when = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Rome", dateStyle: "long", timeStyle: "short" })
      .format(sentAt) + " (Rome)";
  } catch { when = sentAt.toISOString(); }
  const rows = [
    ["Name", d.name], ["From", d.from],
    ["Consent to keep this record", "Yes"],
    ["Language", d.lang === "it" ? "Italian" : "English"],
    ["Page URL", page || "—"], ["Submission time", when],
  ];
  const subject = ("NewSportVision Support for the Values — " + d.name).slice(0, 180);
  const text = ["NEW SPORT VISION", "SUPPORT FOR THE VALUES", "",
    d.name + ", from " + d.from + ", has signed the declaration of support.", "",
    ...rows.map(([k, v]) => k + ": " + v)].join("\n");
  const cell = "padding:7px 0;border-bottom:1px solid #DEDAD0;vertical-align:top;";
  const html =
    '<!doctype html><html><body style="margin:0;padding:28px 20px;background:#F2EFE7;' +
    'color:#1D1D1B;font-family:Helvetica,Arial,sans-serif;"><div style="max-width:640px;margin:0 auto;">' +
    '<p style="margin:0;font-size:12px;font-weight:700;letter-spacing:.18em;">NEW SPORT VISION</p>' +
    '<h1 style="margin:6px 0 18px;font-size:24px;letter-spacing:.02em;">SUPPORT FOR THE VALUES</h1>' +
    '<p style="margin:0 0 22px;font-size:17px;line-height:1.5;"><strong>' + escapeHtml(d.name) +
    "</strong>, from <strong>" + escapeHtml(d.from) + "</strong>, has signed the declaration of support.</p>" +
    '<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;">' +
    rows.map(([k, v]) => '<tr><td style="' + cell + 'width:210px;color:#6B6A64;font-size:13px;">' +
      escapeHtml(k) + '</td><td style="' + cell + 'font-size:15px;">' + escapeHtml(v) + "</td></tr>").join("") +
    "</table></div></body></html>";
  return { subject, text, html };
}

const defaultLimiter = createLimiter();

export async function handle(request, deps = {}) {
  const env = deps.env || {};
  const send = deps.send || sendWithResend;
  const now = deps.now || Date.now;
  const limiter = deps.limiter || defaultLimiter;
  const log = deps.log || console;

  const host = request.headers.get("host") || new URL(request.url).host;
  let origin = "";
  try { origin = new URL(request.headers.get("origin") || "").host; } catch { origin = ""; }
  if (!origin || origin !== host) return refuse(403, "forbidden");

  if (!(request.headers.get("content-type") || "").toLowerCase().startsWith("application/json")) {
    return refuse(415, "unsupported");
  }
  if (Number(request.headers.get("content-length") || 0) > MAX_BODY_BYTES) return refuse(413, "too_large");
  let raw;
  try { raw = await request.text(); } catch { return refuse(400, "malformed"); }
  if (new TextEncoder().encode(raw).length > MAX_BODY_BYTES) return refuse(413, "too_large");
  let input;
  try { input = JSON.parse(raw); } catch { return refuse(400, "malformed"); }
  if (!input || typeof input !== "object" || Array.isArray(input)) return refuse(400, "malformed");

  if (typeof input.website === "string" && input.website.trim() !== "") return refuse(400, "rejected");
  if (typeof input.elapsed !== "number" || !(input.elapsed >= MIN_ELAPSED_MS)) return refuse(400, "rejected");

  const checked = validate(input);
  if (!checked.ok) return refuse(422, "invalid", { fields: checked.fields });

  const address = (request.headers.get("x-real-ip") ||
    (request.headers.get("x-forwarded-for") || "").split(",")[0]).trim();
  if (!limiter.allow(address, now())) return refuse(429, "busy");

  const apiKey = typeof env.RESEND_API_KEY === "string" ? env.RESEND_API_KEY.trim() : "";
  if (!apiKey) {
    log.warn("support: RESEND_API_KEY is not set, nothing was sent");
    return refuse(503, "unavailable");
  }

  let page = "";
  try {
    const u = new URL(typeof input.page === "string" ? input.page.slice(0, 400) : "");
    if (u.host === host) page = u.origin + u.pathname;
  } catch { page = ""; }

  const mail = composeEmail(checked.data, new Date(now()), page);
  const result = await send({
    apiKey,
    idempotencyKey: typeof input.key === "string" && KEY.test(input.key) ? "support/" + input.key : "",
    message: {
      from: configured(env.HELP_DESK_FROM_EMAIL, FROM_DEFAULT),
      to: [configured(env.HELP_DESK_TO_EMAIL, TO_DEFAULT)],
      subject: mail.subject, html: mail.html, text: mail.text,
      tags: [{ name: "source", value: "support-values" }],
    },
  });

  if (result.kind === "sent") return reply(200, { ok: true });
  if (result.kind === "timeout") { log.warn("support: Resend did not answer in time"); return refuse(504, "timeout"); }
  if (result.kind === "refused" && result.status === 429) return refuse(503, "busy");
  if (result.kind === "refused" && result.status === 409) return refuse(409, "duplicate");
  log.warn("support: Resend did not accept the message", result.kind, result.status || "", result.code || "");
  return refuse(502, "unavailable");
}

export function POST(request) {
  return handle(request, { env: process.env });
}
