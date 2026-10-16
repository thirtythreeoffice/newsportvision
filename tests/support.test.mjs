/* node --test tests/  — the FSF26 signature endpoint against a fake store
   (an in-memory Redis for the commands it uses) and a fake Resend. */
import test from "node:test";
import assert from "node:assert/strict";
import { handle, wall, validate, MIN_ELAPSED_MS } from "../api/support.mjs";

function fakeStore() {
  const kv = new Map(), lists = new Map(), ttl = new Map();
  const run = ([c, ...a]) => {
    switch (c) {
      case "SET": {
        const [k, v, ...opt] = a;
        if (opt.includes("NX") && kv.has(k)) return null;
        kv.set(k, String(v)); if (opt.includes("EX")) ttl.set(k, Number(opt[opt.indexOf("EX") + 1])); return "OK";
      }
      case "INCR": { const v = Number(kv.get(a[0]) || 0) + 1; kv.set(a[0], String(v)); return v; }
      case "DEL": return kv.delete(a[0]) ? 1 : 0;
      case "RPUSH": { const l = lists.get(a[0]) || []; l.push(String(a[1])); lists.set(a[0], l); return l.length; }
      case "LRANGE": { const l = lists.get(a[0]) || []; return l.slice(Math.max(0, l.length + Number(a[1])), l.length); }
      case "MGET": return a.map((k) => kv.has(k) ? kv.get(k) : null);
      default: throw new Error("unknown " + c);
    }
  };
  return { kv, lists, ttl, pipe: async (cmds) => cmds.map((c) => run(c.map(String))), one: async (...c) => run(c.map(String)) };
}
const PNG = "data:image/png;base64," + Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 13]).toString("base64");
function req(body, { origin = "https://www.newsportvision.com", ip = "203.0.113.7", type = "application/json" } = {}) {
  const raw = typeof body === "string" ? body : JSON.stringify(body);
  const h = { host: "www.newsportvision.com", origin, "content-type": type, "content-length": String(raw.length), "x-real-ip": ip };
  return { url: "https://www.newsportvision.com/api/support/", headers: { get: (k) => h[k.toLowerCase()] ?? null }, text: async () => raw };
}
function deps(over = {}) {
  const sent = [];
  return { sent, env: { RESEND_API_KEY: "re_test" }, store: fakeStore(), log: { warn() {} },
    limiter: { allow: () => true }, now: () => Date.UTC(2026, 9, 16, 12, 3, 0),
    send: async ({ message, idempotencyKey }) => { sent.push({ message, idempotencyKey }); return { kind: "sent" }; }, ...over };
}
const base = { name: "Ana Petrović", from: "Novi Sad", consent: true, website: "", lang: "en", elapsed: 9000 };

test("a signature without email or drawing: numbered, stored, office mailed", async () => {
  const d = deps();
  const r = await handle(req(base), d); const j = await r.json();
  assert.equal(r.status, 200); assert.equal(j.id, "FSF26-0001"); assert.equal(j.no, "0001"); assert.equal(j.day, "16.10.2026");
  const rec = JSON.parse(d.store.kv.get("fsf26:sig:1"));
  assert.equal(rec.full_name, "Ana Petrović"); assert.equal(rec.timestamp, "2026-10-16T14:03:00+02:00");
  assert.match(rec.token, /^[0-9a-f]{32}$/); assert.equal(rec.channel, "web"); assert.equal(rec.consent_version, "fsf26-2026-10-16");
  assert.equal(d.sent.length, 1);
  assert.equal(d.sent[0].message.subject, "[FSF26 · Support to Values] No. 0001 — Ana Petrović, Novi Sad");
  assert.equal(d.sent[0].message.to[0], "office@newsportvision.com");
  assert.equal(d.sent[0].message.from, "NewSportVision Help Desk <helpdesk@send.newsportvision.com>");
  assert.equal(d.sent[0].message.reply_to, undefined);
  assert.ok(d.sent[0].message.html.includes("Ana Petrović</strong> from <strong>Novi Sad"));
});

test("with email and drawing, Italian: reply-to, inline signature, thank-you in Italian; numbers rise", async () => {
  const d = deps();
  await handle(req(base), d);
  const r = await handle(req({ ...base, name: "Niccolò D'Alessandro", from: "Città di Castello", email: "n@example.it",
    type: "club", signature: PNG, wall: true, lang: "it" }, { ip: "198.51.100.2" }), d);
  const j = await r.json(); assert.equal(j.id, "FSF26-0002");
  const office = d.sent[1].message, thanks = d.sent[2].message;
  assert.equal(office.subject, "[FSF26 · Support to Values] No. 0002 — Niccolò D'Alessandro, Città di Castello");
  assert.equal(office.reply_to, "n@example.it");
  assert.equal(office.attachments[0].content_id, "fsf26-signature-0002");
  assert.ok(office.html.includes("cid:fsf26-signature-0002"));
  assert.ok(office.html.includes("Niccolò D&#39;Alessandro") || office.html.includes("Niccolò D&#x27;Alessandro") || office.html.includes("Niccolò D'Alessandro"));
  assert.deepEqual(thanks.to, ["n@example.it"]); assert.match(thanks.subject, /N\. 0002/); assert.match(thanks.text, /Sei il sostenitore n\. 2\./);
  assert.ok(d.store.kv.get("fsf26:img:2").length > 0);
});

test("Đorđe Šćepanović-Žižić is accepted and arrives intact", async () => {
  const d = deps();
  const r = await handle(req({ ...base, name: "Đorđe Šćepanović-Žižić", from: "Čačak" }), d);
  assert.equal(r.status, 200);
  assert.ok(d.sent[0].message.subject.endsWith("Đorđe Šćepanović-Žižić, Čačak"));
  assert.ok(d.sent[0].message.text.includes("Đorđe Šćepanović-Žižić"));
});

test("bots are told yes and nothing happens", async () => {
  for (const b of [{ ...base, website: "http://spam" }, { ...base, elapsed: MIN_ELAPSED_MS - 1 }, { ...base, elapsed: undefined }]) {
    const d = deps(); const r = await handle(req(b), d); const j = await r.json();
    assert.equal(r.status, 200); assert.equal(j.ok, true); assert.equal(j.id, undefined);
    assert.equal(d.sent.length, 0); assert.equal(d.store.kv.size, 0);
  }
});

test("the same name and place within a day: duplicate, no second number", async () => {
  const d = deps();
  await handle(req(base), d);
  const r = await handle(req({ ...base, name: "ana  petrović", from: "Novi Sad." }, { ip: "192.0.2.9" }), d);
  assert.equal(r.status, 409); assert.equal(d.store.kv.get("fsf26:seq"), "1"); assert.equal(d.sent.length, 1);
});

test("rate limit per address (5 in 10 minutes), the address never stored", async () => {
  const d = deps();
  for (let i = 0; i < 5; i++) assert.equal((await handle(req({ ...base, name: "Signer " + "abcde"[i] + "x" }), d)).status, 200);
  assert.equal((await handle(req({ ...base, name: "Signer Six" }), d)).status, 429);
  for (const [k, v] of d.store.kv) assert.ok(!k.includes("203.0.113.7") && !String(v).includes("203.0.113.7"));
  const rl = [...d.store.ttl.keys()].find((k) => k.startsWith("fsf26:rl:")); assert.equal(d.store.ttl.get(rl), 600);
});

test("validation: lengths, characters, email, type, drawing, consent", () => {
  assert.deepEqual(validate({ ...base, name: "A" }).fields, ["name"]);
  assert.deepEqual(validate({ ...base, name: "x".repeat(81) }).fields, ["name"]);
  assert.deepEqual(validate({ ...base, from: "y".repeat(121) }).fields, ["from"]);
  assert.ok(validate({ ...base, from: "z".repeat(120) }).ok);
  assert.deepEqual(validate({ ...base, name: "<script>" }).fields, ["name"]);
  assert.deepEqual(validate({ ...base, email: "no-at-sign" }).fields, ["email"]);
  assert.deepEqual(validate({ ...base, type: "army" }).fields, ["type"]);
  assert.deepEqual(validate({ ...base, signature: "data:image/png;base64,AAAA" }).fields, ["signature"]);
  assert.deepEqual(validate({ ...base, signature: "data:image/png;base64," + "A".repeat(300000) }).fields, ["signature"]);
  assert.deepEqual(validate({ ...base, consent: "yes" }).fields, ["consent"]);
});

test("no header injection: line breaks never reach a header", async () => {
  const d = deps();
  const r = await handle(req({ ...base, name: "Ana\r\nBcc: x@evil.test", email: "a@b.co\r\nBcc: y@evil.test" }), d);
  assert.equal(r.status, 422);
  const r2 = await handle(req({ ...base, name: "Ana Bcc" }), d);
  assert.equal(r2.status, 200); assert.ok(!/[\r\n]/.test(d.sent[0].message.subject));
});

test("not configured: refused, nothing kept", async () => {
  const d1 = deps({ env: {} }); assert.equal((await handle(req(base), d1)).status, 503); assert.equal(d1.store.kv.size, 0);
  const d2 = deps({ store: null }); assert.equal((await handle(req(base), d2)).status, 503); assert.equal(d2.sent.length, 0);
});

test("office mail fails twice: the signature stays, flagged for resending", async () => {
  let calls = 0;
  const d = deps({ send: async () => { calls++; return { kind: "timeout" }; } });
  const r = await handle(req(base), d);
  assert.equal(r.status, 200); assert.equal(calls, 2);
  assert.equal(JSON.parse(d.store.kv.get("fsf26:sig:1")).office_mail, "failed");
  assert.deepEqual(d.store.lists.get("fsf26:unsent"), ["1"]);
});

test("origin and type are checked", async () => {
  assert.equal((await handle(req(base, { origin: "https://evil.example" }), deps())).status, 403);
  assert.equal((await handle(req(base, { type: "text/plain" }), deps())).status, 415);
});

test("the wall shows only those who asked, newest first, never an email", async () => {
  const d = deps();
  await handle(req({ ...base, name: "Uno Primo", wall: true, email: "u@x.it" }, { ip: "1.1.1.1" }), d);
  await handle(req({ ...base, name: "Due Secondo" }, { ip: "1.1.1.2" }), d);
  await handle(req({ ...base, name: "Tre Terzo", wall: true }, { ip: "1.1.1.3" }), d);
  const j = await (await wall({ store: d.store })).json();
  assert.deepEqual(j.wall.map((w) => w.name), ["Tre Terzo", "Uno Primo"]);
  assert.ok(!JSON.stringify(j).includes("u@x.it"));
});
