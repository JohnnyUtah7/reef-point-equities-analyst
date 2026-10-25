import assert from "node:assert/strict";
import { filingsFromSubmissions, pickConcept } from "../src/sec.ts";
import { handleRpc } from "../src/protocol.ts";

const submissions = {
  cik: "320193",
  name: "Apple Inc.",
  filings: {
    recent: {
      form: ["8-K", "4", "10-Q", "10-K"],
      filingDate: ["2026-01-02", "2026-01-01", "2025-08-01", "2025-11-01"],
      reportDate: ["2026-01-02", "", "2025-06-28", "2025-09-27"],
      accessionNumber: ["0001-26-000001", "0001-26-000002", "0001-25-000010", "0001-25-000099"],
      primaryDocument: ["a8k.htm", "form4.xml", "a10q.htm", "a10k.htm"],
    },
  },
};

const filings = filingsFromSubmissions(submissions, 2);
assert.equal(filings.some((row) => row.form === "10-K"), true);
assert.equal(filings.find((row) => row.form === "10-K")?.accession, "0001-25-000099");
assert.match(filings.find((row) => row.form === "10-K")!.url, /320193\/000125000099\/a10k\.htm$/);

const facts = {
  facts: {
    "us-gaap": {
      Revenues: {
        units: {
          USD: [
            { val: 100, end: "2024-09-28", filed: "2024-11-01", form: "10-K", fp: "FY", fy: 2024, accn: "0001-24-1" },
            { val: 200, end: "2025-09-27", filed: "2025-10-31", form: "10-K", fp: "FY", fy: 2025, accn: "0001-25-1" },
            { val: 50, end: "2025-06-28", filed: "2025-08-01", form: "10-Q", fp: "Q3", fy: 2025, accn: "0001-25-2" },
          ],
        },
      },
      CommonStockSharesOutstanding: {
        units: {
          shares: [
            { val: 15000000000, end: "2025-09-27", filed: "2025-10-31", form: "10-K", accn: "0001-25-1" },
          ],
        },
      },
    },
  },
};

const revenue = pickConcept(facts, ["Revenues", "SalesRevenueNet"], "flow");
assert.equal(revenue?.value, 200);
facts.facts["us-gaap"].SalesRevenueNet = {
  units: {
    USD: [{ val: 9, end: "2018-09-29", filed: "2018-11-01", form: "10-K", fp: "FY", fy: 2018, accn: "old" }],
  },
};
assert.equal(pickConcept(facts, ["SalesRevenueNet", "Revenues"], "flow")?.value, 200);
assert.equal(revenue?.accession, "0001-25-1");
const shares = pickConcept(facts, ["CommonStockSharesOutstanding"], "shares");
assert.equal(shares?.unit, "shares");

const fakeGet = async (url: string) => {
  if (url.includes("company_tickers")) {
    return { "0": { cik_str: 320193, ticker: "AAPL", title: "Apple Inc." } };
  }
  if (url.includes("submissions")) return submissions;
  if (url.includes("companyfacts")) return facts;
  throw new Error(url);
};

const listed = await handleRpc({ jsonrpc: "2.0", id: 1, method: "tools/list" }, fakeGet);
const tools = (listed as { result: { tools: { annotations: Record<string, boolean> }[] } }).result.tools;
assert.equal(tools.length, 3);
for (const tool of tools) {
  assert.equal(tool.annotations.readOnlyHint, true);
  assert.equal(tool.annotations.destructiveHint, false);
  assert.equal(tool.annotations.openWorldHint, true);
}

const called = await handleRpc(
  { jsonrpc: "2.0", id: 2, method: "tools/call", params: { name: "company_lookup", arguments: { ticker: "aapl" } } },
  fakeGet,
);
const text = (called as { result: { content: { text: string }[] } }).result.content[0].text;
const looked = JSON.parse(text);
assert.equal(looked.cik, "0000320193");
assert.equal(looked.ticker, "AAPL");

const missing = await handleRpc(
  { jsonrpc: "2.0", id: 3, method: "tools/call", params: { name: "company_lookup", arguments: { ticker: "NOTREAL" } } },
  fakeGet,
);
assert.equal((missing as { result: { isError: boolean } }).result.isError, true);

const note = await handleRpc({ jsonrpc: "2.0", method: "notifications/initialized" }, fakeGet);
assert.equal(note, null);

console.log("protocol tests ok");
