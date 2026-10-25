import { companyFacts, companyLookup, recentFilings } from "../src/sec.ts";
import { SEC_USER_AGENT } from "../src/sec.ts";

const get = async (url: string) => {
  const res = await fetch(url, { headers: { "user-agent": SEC_USER_AGENT, accept: "application/json" } });
  if (!res.ok) throw new Error(`${res.status} ${url}`);
  return res.json();
};

const company = await companyLookup("AAPL", get);
if (company.cik !== "0000320193") throw new Error(`unexpected cik ${company.cik}`);
const filings = await recentFilings("AAPL", 8, get);
if (!filings.filings.some((row) => row.form === "10-K" && row.accession && row.url)) {
  throw new Error("no 10-K in recent filings");
}
const facts = await companyFacts("AAPL", get);
if (!facts.facts.revenue || facts.facts.revenue.value <= 0 || !facts.facts.revenue.accession) {
  throw new Error("revenue fact missing");
}
console.log(JSON.stringify({
  name: company.name,
  cik: company.cik,
  filing: filings.filings[0],
  revenue: facts.facts.revenue,
  shares: facts.facts.shares,
}, null, 2));
