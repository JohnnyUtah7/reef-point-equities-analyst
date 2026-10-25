export const SEC_USER_AGENT = "Reef Point Capital realchrismiller@gmail.com";

export const TICKER_URL = "https://www.sec.gov/files/company_tickers.json";

const FILING_FORMS = ["10-K", "10-Q", "8-K", "20-F", "40-F", "6-K"];

const CONCEPTS = {
  revenue: [
    "Revenues",
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
  ],
  shares: [
    "CommonStockSharesOutstanding",
    "EntityCommonStockSharesOutstanding",
    "WeightedAverageNumberOfDilutedSharesOutstanding",
  ],
  cash: ["CashAndCashEquivalentsAtCarryingValue", "Cash"],
  debt: [
    "LongTermDebtNoncurrent",
    "LongTermDebt",
    "LongTermDebtAndCapitalLeaseObligations",
  ],
} as const;

export type SecGet = (url: string) => Promise<unknown>;

type FactRow = {
  val?: number;
  end?: string;
  filed?: string;
  form?: string;
  fp?: string;
  fy?: number;
  accn?: string;
};

export function padCik(cik: number | string): string {
  return String(cik).replace(/\D/g, "").padStart(10, "0");
}

export function submissionsUrl(cik: string): string {
  return `https://data.sec.gov/submissions/CIK${padCik(cik)}.json`;
}

export function factsUrl(cik: string): string {
  return `https://data.sec.gov/api/xbrl/companyfacts/CIK${padCik(cik)}.json`;
}

export function filingUrl(cik: string, accession: string, primaryDocument: string): string {
  const flat = accession.replace(/-/g, "");
  return `https://www.sec.gov/Archives/edgar/data/${Number(padCik(cik))}/${flat}/${primaryDocument}`;
}

type TickerRow = { cik_str: number; ticker: string; title: string };

export async function resolveTicker(ticker: string, get: SecGet) {
  const want = ticker.trim().toUpperCase();
  if (!/^[A-Z0-9.\-]{1,10}$/.test(want)) {
    throw new Error(`Ticker ${ticker} is not a usable symbol`);
  }
  const raw = (await get(TICKER_URL)) as Record<string, TickerRow>;
  for (const row of Object.values(raw)) {
    if (String(row.ticker || "").toUpperCase() === want) {
      return {
        cik: padCik(row.cik_str),
        ticker: want,
        name: row.title,
      };
    }
  }
  throw new Error(`No SEC company for ticker ${want}`);
}

export async function companyLookup(ticker: string, get: SecGet) {
  const base = await resolveTicker(ticker, get);
  const sub = (await get(submissionsUrl(base.cik))) as {
    name?: string;
    exchanges?: string[];
    sic?: string;
    sicDescription?: string;
  };
  return {
    ticker: base.ticker,
    cik: base.cik,
    name: sub.name || base.name,
    exchange: (sub.exchanges || []).filter(Boolean),
    sic: sub.sic || null,
    sicDescription: sub.sicDescription || null,
    source: "SEC submissions",
  };
}

export function filingsFromSubmissions(sub: Record<string, unknown>, limit: number) {
  const recent = ((sub.filings as { recent?: Record<string, string[]> }) || {}).recent || {};
  const forms = recent.form || [];
  const cap = Math.max(1, Math.min(limit, 40));
  const matched = [];
  for (let i = 0; i < forms.length; i++) {
    const form = forms[i];
    if (!FILING_FORMS.includes(form)) continue;
    const accession = (recent.accessionNumber || [])[i];
    const doc = (recent.primaryDocument || [])[i];
    if (!accession || !doc) continue;
    matched.push({
      form,
      filingDate: (recent.filingDate || [])[i] || null,
      reportDate: (recent.reportDate || [])[i] || null,
      accession,
      primaryDocument: doc,
      url: filingUrl(String(sub.cik || ""), accession, doc),
    });
  }
  const picked = [];
  const seen = new Set<string>();
  for (const form of ["10-K", "20-F", "40-F", "10-Q", "8-K", "6-K"]) {
    const hit = matched.find((row) => row.form === form);
    if (!hit) continue;
    picked.push(hit);
    seen.add(hit.accession);
  }
  for (const row of matched) {
    if (picked.length >= cap) break;
    if (seen.has(row.accession)) continue;
    picked.push(row);
    seen.add(row.accession);
  }
  return picked.slice(0, cap);
}

export async function recentFilings(ticker: string, limit: number, get: SecGet) {
  const base = await resolveTicker(ticker, get);
  const sub = (await get(submissionsUrl(base.cik))) as Record<string, unknown>;
  return {
    ticker: base.ticker,
    cik: base.cik,
    name: (sub.name as string) || base.name,
    filings: filingsFromSubmissions(sub, limit),
    source: "SEC submissions",
  };
}

function latest(rows: FactRow[], forms: string[], fyOnly: boolean): FactRow | undefined {
  const pool = rows.filter((row) => {
    if (row.form && !forms.includes(row.form)) return false;
    if (fyOnly && row.fp && row.fp !== "FY") return false;
    return row.val !== undefined && row.end;
  });
  return pool.sort((a, b) => {
    const end = String(b.end).localeCompare(String(a.end));
    if (end !== 0) return end;
    return String(b.filed || "").localeCompare(String(a.filed || ""));
  })[0];
}

export function pickConcept(
  facts: { facts?: { "us-gaap"?: Record<string, { units?: Record<string, FactRow[]> }> } },
  concepts: readonly string[],
  kind: "flow" | "stock" | "shares",
) {
  const gaap = facts.facts?.["us-gaap"] || {};
  let chosen: ReturnType<typeof shapeFact> = null;
  for (const concept of concepts) {
    const units = gaap[concept]?.units;
    if (!units) continue;
    const unitKey = kind === "shares" ? (units.shares ? "shares" : Object.keys(units)[0]) : units.USD ? "USD" : Object.keys(units)[0];
    const rows = units[unitKey] || [];
    const forms = kind === "flow" ? ["10-K", "20-F", "40-F"] : ["10-K", "10-Q", "20-F", "40-F"];
    const best = latest(rows, forms, kind === "flow");
    if (!best) continue;
    const shaped = shapeFact(concept, unitKey, best);
    if (!chosen || String(shaped.end) > String(chosen.end)) chosen = shaped;
  }
  return chosen;
}

function shapeFact(concept: string, unitKey: string, best: FactRow) {
  return {
    concept,
    value: best.val,
    unit: unitKey,
    form: best.form || null,
    end: best.end || null,
    filed: best.filed || null,
    accession: best.accn || null,
    fiscalYear: best.fy ?? null,
    fiscalPeriod: best.fp || null,
  };
}

export async function companyFacts(ticker: string, get: SecGet) {
  const base = await resolveTicker(ticker, get);
  const facts = (await get(factsUrl(base.cik))) as Parameters<typeof pickConcept>[0];
  return {
    ticker: base.ticker,
    cik: base.cik,
    name: base.name,
    facts: {
      revenue: pickConcept(facts, CONCEPTS.revenue, "flow"),
      shares: pickConcept(facts, CONCEPTS.shares, "shares"),
      cash: pickConcept(facts, CONCEPTS.cash, "stock"),
      debt: pickConcept(facts, CONCEPTS.debt, "stock"),
    },
    source: "SEC companyfacts",
    note: "Figures are as reported in the cited filing. They are not a valuation.",
  };
}
