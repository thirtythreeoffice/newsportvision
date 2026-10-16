/* ===========================================================================
   NEWSPORTVISION — Support to Values (FSF26 signatures)
   ---------------------------------------------------------------------------
   POST  a signature of the declaration on /fsf2026/. It is checked, given the
         next running number (FSF26-0001, …) and a random token (for checking
         a certificate later), written to the store, and sent to the office
         by the same route as the Help Desk: Resend, through the Help Desk's
         own tested sender, from the same address to the same inbox. If the
         signer left an email, they get a thank-you with their number.
   GET   the wall of supporters: only those who ticked the separate box.

   Environment (Vercel → Project → Settings → Environment Variables):
     RESEND_API_KEY            the Help Desk's key
     HELP_DESK_TO_EMAIL        optional, the office inbox (default office@…)
     HELP_DESK_FROM_EMAIL      optional, the office mail's sender (as Help Desk)
     SUPPORT_FROM_EMAIL        optional, the thank-you's sender
                               (default NewSportVision <fsf26@send.newsportvision.com>)
     UPSTASH_REDIS_REST_URL    the store (set by Vercel's Upstash integration;
     UPSTASH_REDIS_REST_TOKEN  KV_REST_API_URL / KV_REST_API_TOKEN also work)

   Without the store or the key nothing is written or sent and the page says
   signing is not open: no signature is ever shown as accepted that was not.
   Nothing a visitor typed is logged. The address is used only for the rate
   limit, as a salted hash that expires in ten minutes.
   =========================================================================== */

import { clean, escapeHtml, createLimiter, sendWithResend } from "./help-desk.mjs";
import { storeFrom } from "../lib/fsf26-store.mjs";
import { TEXT } from "../lib/fsf26-text.mjs";

const TO_DEFAULT = "office@newsportvision.com";
const FROM_DEFAULT = "NewSportVision Help Desk <helpdesk@send.newsportvision.com>";
const CONFIRM_FROM_DEFAULT = "NewSportVision <fsf26@send.newsportvision.com>";
const MAX_BODY_BYTES = 320 * 1024;
export const MIN_ELAPSED_MS = 3000;                 // faster than this is a bot
const SIGNATURE_MAX_B64 = 272000;                   // ~200 KB of PNG
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const RATE = { window: 600, max: 5 };               // per address, seconds / signatures
const DUP_TTL = 86400;                              // same name + place: 24 h
const TYPES = TEXT.en.signer_types.map((p) => p[0]);

/* Names in every alphabet the page may meet: letters with their marks,
   spaces, hyphens, apostrophes and dots (Đorđe Šćepanović-Žižić, Niccolò
   D'Alessandro, J. R. R.). A place or organisation may also have numbers and
   a few joining signs. */
const NAME_RE = /^[\p{L}\p{M}][\p{L}\p{M} .'’‐-]*$/u;
const FROM_RE = /^[\p{L}\p{M}\p{N}][\p{L}\p{M}\p{N} .,'’‐&()/-]*$/u;
const EMAIL_RE = /^[^\s@<>()[\]\\,;:"]{1,64}@[^\s@<>()[\]\\,;:"]+\.[^\s@<>()[\]\\,;:".]{2,}$/;

const reply = (status, body, cache) => new Response(JSON.stringify(body), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": cache || "no-store" },
});
const refuse = (status, error, extra) => reply(status, { ok: false, error, ...extra });
const configured = (value, fallback) => {
  const v = typeof value === "string" ? value.trim() : "";
  return v && v.length <= 320 && !/[\r\n]/.test(v) && v.includes("@") ? v : fallback;
};
const chars = (s) => Array.from(s).length;
/* nothing that could end a mail header, ever */
const oneLine = (s) => String(s).replace(/[\r\n\u2028\u2029]+/g, " ");

/* --- checking ------------------------------------------------------------- */
export function validate(input) {
  const bad = [];
  const name = clean(input.name, 80);
  const from = clean(input.from, 120);
  const email = clean(input.email, 254);
  if (!name || chars(name) < 2 || !NAME_RE.test(name)) bad.push("name");
  if (!from || chars(from) < 2 || !FROM_RE.test(from)) bad.push("from");
  if (email === null || (email && !EMAIL_RE.test(email))) bad.push("email");
  const type = typeof input.type === "string" ? input.type : "";
  if (type && !TYPES.includes(type)) bad.push("type");
  let signature = "";
  if (input.signature != null && input.signature !== "") {
    const m = typeof input.signature === "string" && /^data:image\/png;base64,([A-Za-z0-9+/]+={0,2})$/.exec(input.signature);
    let ok = false;
    if (m && m[1].length <= SIGNATURE_MAX_B64) {
      const head = Buffer.from(m[1].slice(0, 12), "base64");
      ok = PNG_MAGIC.every((b, i) => head[i] === b);
    }
    if (ok) signature = m[1]; else bad.push("signature");
  }
  if (input.consent !== true) bad.push("consent");
  return {
    ok: bad.length === 0, fields: bad,
    data: { name, from, email: email || "", type, signature, wall: input.wall === true,
            lang: input.lang === "it" ? "it" : "en" },
  };
}

/* --- time, in Belgrade ---------------------------------------------------- */
export function belgrade(date) {
  const parts = {};
  new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Belgrade", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23", timeZoneName: "longOffset",
  }).formatToParts(date).forEach((p) => { parts[p.type] = p.value; });
  const offset = (parts.timeZoneName || "GMT").replace("GMT", "") || "+00:00";
  return {
    iso: `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}${offset}`,
    day: `${parts.day}.${parts.month}.${parts.year}`,
    human: `${parts.day}.${parts.month}.${parts.year} ${parts.hour}:${parts.minute} (Belgrade)`,
  };
}

async function sha256(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");
}
/* The same person written a little differently is still the same person. */
const sameKey = (name, from) => (name + "|" + from).normalize("NFKC").toLocaleLowerCase("und")
  .replace(/[\s.,'’‐\-]+/g, " ").trim();

/* --- the emails ------------------------------------------------------------- */
export function declaration(d) {
  const t = TEXT[d.lang];
  return `${t.decl[0]} ${d.name} ${t.decl[1]} ${d.from}${t.decl[2]}`;
}
const typeLabel = (d) => {
  const hit = TEXT.en.signer_types.find((p) => p[0] === d.type);
  return hit ? hit[1].replace(/^an? /, "") : "—";
};

export function officeMail(r, d) {
  const no = r.no;
  const subject = oneLine(`[FSF26 · Support to Values] No. ${no} — ${d.name}, ${d.from}`).slice(0, 200);
  const rows = [
    ["Number", r.id], ["Name", d.name], ["City or organisation", d.from], ["Signing as", typeLabel(d)],
    ["Email", d.email || "—"], ["On the wall of supporters", d.wall ? "Yes" : "No"],
    ["Language", d.lang === "it" ? "Italian" : "English"], ["Signed", r.signed_at_human],
    ["Consent version", r.consent_version], ["Channel", r.channel],
  ];
  const decl = declaration(d);
  const text = ["NEW SPORT VISION · FSF 26", "SUPPORT TO VALUES — No. " + no, "",
    decl, "", ...rows.map(([k, v]) => k + ": " + v),
    d.signature ? "\nThe drawn signature is attached." : ""].join("\n");
  const cell = "padding:8px 0;border-bottom:1px solid #DEDAD0;vertical-align:top;";
  const html =
    '<!doctype html><html><body style="margin:0;padding:28px 18px;background:#F2EFE7;color:#1D1D1B;' +
    "font-family:Archivo,'Helvetica Neue',Helvetica,Arial,sans-serif;\">" +
    '<div style="max-width:640px;margin:0 auto;">' +
    '<div style="height:6px;width:72px;background:#FAC51C;margin:0 0 18px;"></div>' +
    '<p style="margin:0;font-size:12px;font-weight:700;letter-spacing:.18em;">NEW SPORT VISION · FSF 26</p>' +
    '<h1 style="margin:6px 0 4px;font-size:28px;line-height:1.05;letter-spacing:-.01em;font-weight:800;">SUPPORT TO VALUES</h1>' +
    '<p style="margin:0 0 22px;font-size:13px;font-weight:700;letter-spacing:.16em;">No. ' + escapeHtml(no) + "</p>" +
    '<p style="margin:0 0 24px;font-family:Georgia,\'Times New Roman\',serif;font-size:18px;line-height:1.5;">' +
    escapeHtml(TEXT[d.lang].decl[0]) + " <strong>" + escapeHtml(d.name) + "</strong> " + escapeHtml(TEXT[d.lang].decl[1]) +
    " <strong>" + escapeHtml(d.from) + "</strong>" + escapeHtml(TEXT[d.lang].decl[2]) + "</p>" +
    (d.signature ? '<p style="margin:0 0 24px;border-bottom:2px solid #1D1D1B;padding-bottom:6px;">' +
      '<img src="cid:fsf26-signature-' + escapeHtml(no) + '" alt="Signature of ' + escapeHtml(d.name) +
      '" style="display:block;max-width:100%;height:auto;max-height:140px;"></p>' : "") +
    '<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;">' +
    rows.map(([k, v]) => '<tr><td style="' + cell + 'width:200px;color:#6B6A64;font-size:13px;">' + escapeHtml(k) +
      '</td><td style="' + cell + 'font-size:15px;">' + escapeHtml(v) + "</td></tr>").join("") +
    "</table></div></body></html>";
  return { subject, text, html };
}

export function confirmationMail(r, d) {
  const t = TEXT[d.lang];
  const subject = oneLine(t.mail_confirm_subject.replace("%s", r.no)).slice(0, 200);
  const hello = t.mail_confirm_hello.replace("%s", d.name);
  const body = t.mail_confirm_body.replace("%s", String(r.n));
  const seal = t.seal.replace("%s", r.no).replace("%s", r.signed_day);
  const decl = declaration(d);
  const text = [hello, "", body, t.mail_confirm_pdf, "", t.mail_confirm_copy, "", decl, "", seal, "", t.mail_confirm_sign].join("\n");
  const html =
    '<!doctype html><html><body style="margin:0;padding:28px 18px;background:#F2EFE7;color:#1D1D1B;' +
    "font-family:Archivo,'Helvetica Neue',Helvetica,Arial,sans-serif;\"><div style=\"max-width:600px;margin:0 auto;\">" +
    '<div style="height:6px;width:72px;background:#FAC51C;margin:0 0 18px;"></div>' +
    '<p style="margin:0 0 18px;font-size:12px;font-weight:700;letter-spacing:.18em;">NEW SPORT VISION · FSF 26</p>' +
    '<p style="margin:0 0 12px;font-size:17px;line-height:1.5;">' + escapeHtml(hello) + "</p>" +
    '<p style="margin:0 0 12px;font-size:17px;line-height:1.5;">' + escapeHtml(body) + "</p>" +
    '<p style="margin:0 0 26px;font-size:15px;line-height:1.5;color:#4A4944;">' + escapeHtml(t.mail_confirm_pdf) + "</p>" +
    '<p style="margin:0 0 8px;font-size:12px;font-weight:700;letter-spacing:.16em;color:#6B6A64;">' + escapeHtml(t.mail_confirm_copy.toUpperCase()) + "</p>" +
    '<p style="margin:0 0 20px;padding:18px 20px;background:#FFFFFF;font-family:Georgia,\'Times New Roman\',serif;font-size:16px;line-height:1.55;">' +
    escapeHtml(decl) + "</p>" +
    '<p style="display:inline-block;margin:0 0 26px;padding:6px 10px;background:#FAC51C;font-size:12px;font-weight:800;letter-spacing:.14em;">' +
    escapeHtml(seal) + "</p>" +
    '<p style="margin:0;font-size:13px;color:#6B6A64;">' + escapeHtml(t.mail_confirm_sign) + "</p></div></body></html>";
  return { subject, text, html };
}

/* PHASE 2 HOOK — the signed declaration as a PDF certificate.
   Return Resend attachments here ({ filename, content (base64),
   content_type: "application/pdf" }) and a link built from r.id and r.token
   (e.g. /fsf2026/certificate/?no=<id>&t=<token>) to add to the thank-you.
   Until then the thank-you says the PDF will follow separately. */
export async function phase2Attachments(/* record, data */) { return []; }

/* --- the endpoint ----------------------------------------------------------- */
const defaultLimiter = createLimiter();

async function sendOnce(send, apiKey, idempotencyKey, message, log, what) {
  for (let attempt = 0; attempt < 2; attempt++) {
    const result = await send({ apiKey, idempotencyKey, message });
    if (result.kind === "sent") return true;
    const again = result.kind === "timeout" || result.kind === "network" ||
      (result.kind === "refused" && result.status >= 500);
    log.warn("support: " + what + " not accepted", result.kind, result.status || "", result.code || "");
    if (!again) break;
  }
  return false;
}

export async function handle(request, deps = {}) {
  const env = deps.env || {};
  const send = deps.send || sendWithResend;
  const now = deps.now || Date.now;
  const limiter = deps.limiter || defaultLimiter;
  const log = deps.log || console;
  const store = deps.store !== undefined ? deps.store : storeFrom(env);

  const host = request.headers.get("host") || new URL(request.url).host;
  let origin = "";
  try { origin = new URL(request.headers.get("origin") || "").host; } catch { origin = ""; }
  if (!origin || origin !== host) return refuse(403, "forbidden");
  if (!(request.headers.get("content-type") || "").toLowerCase().startsWith("application/json")) return refuse(415, "unsupported");
  if (Number(request.headers.get("content-length") || 0) > MAX_BODY_BYTES) return refuse(413, "too_large");
  let raw;
  try { raw = await request.text(); } catch { return refuse(400, "malformed"); }
  if (new TextEncoder().encode(raw).length > MAX_BODY_BYTES) return refuse(413, "too_large");
  let input;
  try { input = JSON.parse(raw); } catch { return refuse(400, "malformed"); }
  if (!input || typeof input !== "object" || Array.isArray(input)) return refuse(400, "malformed");

  /* A bot is told it worked and nothing happens: no number, no record, no mail. */
  if ((typeof input.website === "string" && input.website.trim() !== "") ||
      typeof input.elapsed !== "number" || !(input.elapsed >= MIN_ELAPSED_MS)) {
    return reply(200, { ok: true });
  }

  const checked = validate(input);
  if (!checked.ok) return refuse(422, "invalid", { fields: checked.fields });
  const d = checked.data;

  const address = (request.headers.get("x-real-ip") || (request.headers.get("x-forwarded-for") || "").split(",")[0]).trim();
  if (!limiter.allow(address, now())) return refuse(429, "busy");

  const apiKey = typeof env.RESEND_API_KEY === "string" ? env.RESEND_API_KEY.trim() : "";
  if (!store || !apiKey) {
    log.warn("support: " + (!store ? "the store is not configured" : "RESEND_API_KEY is not set") + ", nothing was taken");
    return refuse(503, "unavailable");
  }

  const at = new Date(now());
  const time = belgrade(at);
  let n, dupKey;
  try {
    /* the address only as a salted hash, rotated daily, gone in ten minutes */
    const salt = (env.FSF26_SALT || "fsf26") + time.day;
    const ops = [];
    if (address) {
      const rl = "fsf26:rl:" + (await sha256(salt + "|" + address)).slice(0, 32);
      ops.push(["SET", rl, 0, "NX", "EX", RATE.window], ["INCR", rl]);   // INCR keeps the expiry
    }
    dupKey = "fsf26:dup:" + (await sha256(sameKey(d.name, d.from))).slice(0, 40);
    ops.push(["SET", dupKey, "pending", "NX", "EX", DUP_TTL]);
    const out = await store.pipe(ops);
    if (address && Number(out[1]) > RATE.max) {
      if (out[out.length - 1] === "OK") await store.one("DEL", dupKey);
      return refuse(429, "busy");
    }
    if (out[out.length - 1] !== "OK") return refuse(409, "duplicate");
    n = Number(await store.one("INCR", "fsf26:seq"));
  } catch (err) {
    log.warn("support: store unavailable", String(err && err.message || err).slice(0, 80));
    return refuse(503, "unavailable");
  }

  const no = String(n).padStart(4, "0");
  const tokenBytes = crypto.getRandomValues(new Uint8Array(16));
  const record = {
    id: "FSF26-" + no, no, n,
    token: Array.from(tokenBytes, (b) => b.toString(16).padStart(2, "0")).join(""),
    full_name: d.name, city_or_org: d.from, email: d.email || null, signer_type: d.type || null,
    has_signature: !!d.signature, wall: d.wall, lang: d.lang,
    timestamp: time.iso, consent_version: TEXT[d.lang].consent_version, channel: "web",
    signed_at_human: time.human, signed_day: time.day,
  };

  try {
    const ops = [["SET", "fsf26:sig:" + n, JSON.stringify(record)], ["RPUSH", "fsf26:all", n],
                 ["SET", dupKey, n, "EX", DUP_TTL]];
    if (d.signature) ops.push(["SET", "fsf26:img:" + n, d.signature]);
    if (d.wall) ops.push(["RPUSH", "fsf26:wall", n]);
    await store.pipe(ops);
  } catch (err) {
    log.warn("support: store write failed", String(err && err.message || err).slice(0, 80));
    try { await store.one("DEL", dupKey); } catch { /* best effort */ }
    return refuse(503, "unavailable");
  }

  /* The signature is kept. Now the office hears of it, by the Help Desk's
     route; one retry if the provider stumbles. */
  const office = officeMail(record, d);
  const officeMessage = {
    from: configured(env.HELP_DESK_FROM_EMAIL, FROM_DEFAULT),
    to: [configured(env.HELP_DESK_TO_EMAIL, TO_DEFAULT)],
    subject: office.subject, html: office.html, text: office.text,
    tags: [{ name: "source", value: "fsf26-support" }],
  };
  if (d.email) officeMessage.reply_to = d.email;
  if (d.signature) officeMessage.attachments = [{ content: d.signature, filename: "signature-" + no + ".png",
    content_type: "image/png", content_id: "fsf26-signature-" + no }];
  const officeSent = await sendOnce(send, apiKey, "fsf26/office/" + record.id, officeMessage, log, "office mail");

  let confirmSent = null;
  if (d.email) {
    const c = confirmationMail(record, d);
    const extra = await phase2Attachments(record, d);
    const message = {
      from: configured(env.SUPPORT_FROM_EMAIL, CONFIRM_FROM_DEFAULT),
      to: [d.email], reply_to: configured(env.HELP_DESK_TO_EMAIL, TO_DEFAULT),
      subject: c.subject, html: c.html, text: c.text, tags: [{ name: "source", value: "fsf26-thanks" }],
    };
    if (extra.length) message.attachments = extra;
    confirmSent = await sendOnce(send, apiKey, "fsf26/thanks/" + record.id, message, log, "thank-you");
  }

  if (!officeSent || confirmSent === false) {
    try {
      await store.one("SET", "fsf26:sig:" + n, JSON.stringify({ ...record,
        office_mail: officeSent ? "sent" : "failed", thanks_mail: confirmSent === null ? "none" : confirmSent ? "sent" : "failed" }));
      if (!officeSent) await store.one("RPUSH", "fsf26:unsent", n);
    } catch { /* the signature itself is safe */ }
  }

  return reply(200, { ok: true, id: record.id, no, n, day: time.day });
}

/* The wall: only names given for it, newest first, never an email. */
export async function wall(deps = {}) {
  const store = deps.store !== undefined ? deps.store : storeFrom(deps.env || {});
  if (!store) return reply(200, { wall: [] }, "public, max-age=0, s-maxage=60");
  try {
    const nums = (await store.one("LRANGE", "fsf26:wall", -300, -1)) || [];
    if (!nums.length) return reply(200, { wall: [] }, "public, max-age=0, s-maxage=60");
    const recs = await store.one("MGET", ...nums.map((x) => "fsf26:sig:" + x));
    const list = recs.map((j) => { try { return JSON.parse(j); } catch { return null; } })
      .filter((r) => r && r.wall).reverse()
      .map((r) => ({ no: r.no, name: r.full_name, from: r.city_or_org }));
    return reply(200, { wall: list }, "public, max-age=0, s-maxage=60");
  } catch {
    return reply(200, { wall: [] }, "no-store");
  }
}

export function POST(request) { return handle(request, { env: process.env }); }
export function GET() { return wall({ env: process.env }); }
