// Click-tracking filter for a static site on edge functions (sanitized excerpt of the Ashram Atlas pattern).
//
// Problem: affiliate and outbound-click counts are only useful if the owner's own clicks and automated
// traffic (crawlers, headless test runs) are not in them. Rule used on the site: a request that carries
// the owner cookie OR an automated user agent is still redirected exactly the same way, but no row is
// written to the click log. Only a boolean is derived; the user agent is never stored.
// Run the self-test:  node owner_bot_filter.mjs
import assert from "node:assert";

export const OWNER_COOKIE = "owner_me";
export const BOT_UA = /bot|crawl|spider|slurp|facebookexternalhit|embedly|preview|headless|lighthouse|pagespeed|curl\/|wget|python-requests|httpclient|go-http|playwright|puppeteer|phantomjs/i;
export const hasOwnerCookie = (req) => new RegExp(`(?:^|;\\s*)${OWNER_COOKIE}=1(?:;|$)`).test(req.headers.get("cookie") || "");
export const isAutomated = (req) => BOT_UA.test(req.headers.get("user-agent") || "");
export const isOwner = (req) => hasOwnerCookie(req) || isAutomated(req);

// Redirect handler shape: look up the destination, log the click only for real visitors, then 302.
export async function handleGo(request, { destinations, logClick }) {
  const id = new URL(request.url).pathname.split("/").pop();
  const dest = destinations[id];
  if (!dest) return new Response("Not found", { status: 404 });
  const redirect = new Response(null, { status: 302, headers: { location: dest, "cache-control": "no-store", "x-robots-tag": "noindex" } });
  if (isOwner(request)) return redirect;           // same behaviour, no log row
  await logClick({ id, at: new Date().toISOString() });
  return redirect;
}

// --- self-test ---
const req = (headers) => new Request("https://example.org/go/shop-1", { headers });
const logged = [];
const deps = { destinations: { "shop-1": "https://partner.example/x" }, logClick: async (r) => logged.push(r) };
await handleGo(req({ "user-agent": "Mozilla/5.0 (iPhone)" }), deps);
await handleGo(req({ "user-agent": "Mozilla/5.0 (compatible; Googlebot/2.1)" }), deps);
await handleGo(req({ "user-agent": "Mozilla/5.0", cookie: "owner_me=1" }), deps);
const res = await handleGo(req({ "user-agent": "curl/8.0" }), deps);
assert.equal(logged.length, 1, "only the real visitor is logged");
assert.equal(res.status, 302);
assert.equal((await handleGo(req({}), { ...deps, destinations: {} })).status, 404);
console.log("owner_bot_filter: 4 checks passed");
