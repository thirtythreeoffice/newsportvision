/* ===========================================================================
   NEWSPORTVISION — where FSF26 signatures are kept
   ---------------------------------------------------------------------------
   Upstash Redis, spoken to over its REST API with plain fetch: no client
   library. Vercel's Upstash integration puts the address and token into the
   project's environment (either naming scheme is accepted). Nothing here is
   specific to the request; the endpoint decides what is written.

     fsf26:seq           the running number — INCR, so two signers can never
                         get the same one
     fsf26:sig:<n>       one signature, as JSON
     fsf26:img:<n>       its drawing, if there is one (PNG, base64)
     fsf26:all           every number, in order
     fsf26:wall          the numbers of those who asked to be on the wall
     fsf26:dup:<hash>    name + city seen in the last 24 hours
     fsf26:rl:<hash>     submissions from one address in the last 10 minutes
                         (the address itself is never written: a salted hash,
                         and it expires)
   =========================================================================== */

const TIMEOUT_MS = 4000;

export function storeFrom(env, fetchImpl = fetch) {
  const url = String(env.UPSTASH_REDIS_REST_URL || env.KV_REST_API_URL || "").trim().replace(/\/+$/, "");
  const token = String(env.UPSTASH_REDIS_REST_TOKEN || env.KV_REST_API_TOKEN || "").trim();
  if (!/^https:\/\//.test(url) || !token) return null;

  /* Several commands in one round trip; each answer is { result } or { error }. */
  async function pipe(commands) {
    let res;
    try {
      res = await fetchImpl(url + "/pipeline", {
        method: "POST",
        headers: { authorization: "Bearer " + token, "content-type": "application/json" },
        body: JSON.stringify(commands.map((c) => c.map(String))),
        signal: AbortSignal.timeout(TIMEOUT_MS),
      });
    } catch (err) {
      throw new Error("store: " + (err && err.name === "TimeoutError" ? "timeout" : "network"));
    }
    if (!res.ok) throw new Error("store: http " + res.status);
    const body = await res.json();
    if (!Array.isArray(body) || body.length !== commands.length) throw new Error("store: unexpected answer");
    return body.map((r) => {
      if (r && r.error) throw new Error("store: " + String(r.error).slice(0, 80));
      return r ? r.result : null;
    });
  }
  const one = async (...command) => (await pipe([command]))[0];
  return { pipe, one };
}
