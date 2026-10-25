import { companyFacts, companyLookup, recentFilings, type SecGet } from "./sec.ts";

export const SERVER_INFO = { name: "reef-point-edgar", version: "1.3.15" };

const READ_ONLY = {
  readOnlyHint: true,
  destructiveHint: false,
  openWorldHint: true,
};

const TOOLS = [
  {
    name: "company_lookup",
    description: "Look up a US-listed company on EDGAR by ticker. Returns CIK, legal name, exchange, and SIC.",
    inputSchema: {
      type: "object",
      properties: { ticker: { type: "string", description: "Stock ticker, such as AAPL" } },
      required: ["ticker"],
      additionalProperties: false,
    },
    annotations: READ_ONLY,
  },
  {
    name: "recent_filings",
    description: "Latest 10-K, 10-Q, 8-K, 20-F, 40-F, and 6-K filings for a ticker, with form, dates, accession, and the SEC URL.",
    inputSchema: {
      type: "object",
      properties: {
        ticker: { type: "string" },
        limit: { type: "integer", minimum: 1, maximum: 40 },
      },
      required: ["ticker"],
      additionalProperties: false,
    },
    annotations: READ_ONLY,
  },
  {
    name: "company_facts",
    description: "As-reported revenue, shares, cash, and debt from SEC company facts. Each figure cites form, period end, filed date, and accession. Not a valuation.",
    inputSchema: {
      type: "object",
      properties: { ticker: { type: "string" } },
      required: ["ticker"],
      additionalProperties: false,
    },
    annotations: READ_ONLY,
  },
];

type Rpc = { jsonrpc?: string; id?: number | string | null; method?: string; params?: { name?: string; arguments?: Record<string, unknown> } };

function result(id: Rpc["id"], value: unknown) {
  return { jsonrpc: "2.0", id: id ?? null, result: value };
}

function failure(id: Rpc["id"], message: string) {
  return { jsonrpc: "2.0", id: id ?? null, error: { code: -32603, message } };
}

export async function handleRpc(message: Rpc, get: SecGet): Promise<unknown | null> {
  if (!message || message.jsonrpc !== "2.0" || !message.method) {
    return failure(message?.id, "Invalid JSON-RPC");
  }
  if (message.id === undefined) return null;
  if (message.method === "initialize") {
    return result(message.id, {
      protocolVersion: "2025-03-26",
      capabilities: { tools: { listChanged: false } },
      serverInfo: SERVER_INFO,
    });
  }
  if (message.method === "ping") return result(message.id, {});
  if (message.method === "tools/list") return result(message.id, { tools: TOOLS });
  if (message.method === "tools/call") {
    const name = message.params?.name || "";
    const args = message.params?.arguments || {};
    const ticker = String(args.ticker || "");
    try {
      let data: unknown;
      if (name === "company_lookup") data = await companyLookup(ticker, get);
      else if (name === "recent_filings") data = await recentFilings(ticker, Number(args.limit || 12), get);
      else if (name === "company_facts") data = await companyFacts(ticker, get);
      else return result(message.id, { content: [{ type: "text", text: `Unknown tool ${name}` }], isError: true });
      return result(message.id, { content: [{ type: "text", text: JSON.stringify(data) }] });
    } catch (err) {
      const text = err instanceof Error ? err.message : "EDGAR request failed";
      return result(message.id, { content: [{ type: "text", text }], isError: true });
    }
  }
  return failure(message.id, `Method not found: ${message.method}`);
}
