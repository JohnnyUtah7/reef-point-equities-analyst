import { SEC_USER_AGENT } from "./sec.ts";
import { handleRpc } from "./protocol.ts";

export class SecRateLimit {
  private nextAt = 0;

  constructor(private readonly state: DurableObjectState) {
    void this.state;
  }

  async fetch(): Promise<Response> {
    const now = Date.now();
    const start = Math.max(now, this.nextAt);
    if (start - now > 2000) {
      return new Response("busy", { status: 429, headers: { "retry-after": "1" } });
    }
    this.nextAt = start + 125;
    const wait = start - now;
    if (wait > 0) await new Promise((resolve) => setTimeout(resolve, wait));
    return new Response("ok");
  }
}

type Env = { RATE_LIMIT: DurableObjectNamespace };

const OPENAI_APPS_CHALLENGE = "WTIp5k0H-bCK3Hd2cUBR3Ny_F4GUtnnEkdozJfl6JTE";

const CORS = {
  "access-control-allow-origin": "*",
  "access-control-allow-methods": "GET, POST, OPTIONS",
  "access-control-allow-headers": "content-type, accept, mcp-protocol-version",
};

async function allow(env: Env): Promise<void> {
  const stub = env.RATE_LIMIT.get(env.RATE_LIMIT.idFromName("sec"));
  let res = await stub.fetch("https://rate-limit/acquire");
  if (res.status === 429) {
    await new Promise((resolve) => setTimeout(resolve, 250));
    res = await stub.fetch("https://rate-limit/acquire");
  }
  if (!res.ok) throw new Error("SEC rate limit is busy. Retry in a second.");
}

async function secGet(url: string, env: Env, ctx: ExecutionContext): Promise<unknown> {
  const cache = caches.default;
  const key = new Request(url, { method: "GET" });
  const hit = await cache.match(key);
  if (hit) return hit.json();
  await allow(env);
  const res = await fetch(url, {
    headers: { "user-agent": SEC_USER_AGENT, accept: "application/json" },
  });
  if (!res.ok) throw new Error(`SEC returned ${res.status} for ${url}`);
  const text = await res.text();
  const cached = new Response(text, {
    headers: { "content-type": "application/json", "cache-control": "public, max-age=3600" },
  });
  ctx.waitUntil(cache.put(key, cached.clone()));
  return JSON.parse(text);
}

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...CORS },
  });
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: CORS });
    if (request.method === "GET" && url.pathname === "/.well-known/openai-apps-challenge") {
      return new Response(OPENAI_APPS_CHALLENGE, {
        headers: { "content-type": "text/plain; charset=utf-8", ...CORS },
      });
    }
    if (request.method === "GET" && (url.pathname === "/" || url.pathname === "/health")) {
      return json({ ok: true, name: "reef-point-edgar", version: "1.3.15" });
    }
    if (url.pathname !== "/mcp") return json({ error: "Not found" }, 404);
    if (request.method !== "POST") return json({ error: "POST JSON-RPC to /mcp" }, 405);
    let body: unknown;
    try {
      body = await request.json();
    } catch {
      return json({ jsonrpc: "2.0", id: null, error: { code: -32700, message: "Parse error" } }, 400);
    }
    const get = (target: string) => secGet(target, env, ctx);
    if (Array.isArray(body)) {
      const out = [];
      for (const item of body) {
        const one = await handleRpc(item, get);
        if (one) out.push(one);
      }
      if (!out.length) return new Response(null, { status: 202, headers: CORS });
      return json(out);
    }
    const one = await handleRpc(body as Parameters<typeof handleRpc>[0], get);
    if (!one) return new Response(null, { status: 202, headers: CORS });
    return json(one);
  },
};
