// Sanity check for site/index.html, run by the deploy workflow and locally with `node tools/check.mjs`.
// 1. Syntax-checks the page's inline JavaScript.
// 2. Runs the calculation engine on the default scenario and compares net gain and
//    wealth at exit with the figures recorded in docs/methods.md (within $50).
import { readFileSync } from "node:fs";
import vm from "node:vm";

const html = readFileSync(new URL("../site/index.html", import.meta.url), "utf8");
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (!scripts.length) throw new Error("No inline <script> found in site/index.html");
const js = scripts.join("\n");
new vm.Script(js); // throws on a syntax error

const engine = js.slice(js.indexOf("/* ================= ENGINE"), js.indexOf("/* ================= END ENGINE"));
const defaults = js.match(/const DEFAULTS=(\{[\s\S]*?\n\});/)[1];
const ctx = {};
vm.runInNewContext(`${engine}\nconst DEFAULTS=${defaults};\nresult=simulate(structuredClone(DEFAULTS));`, Object.assign(ctx, { structuredClone }));
const sim = ctx.result;

const expect = {
  rent:  { paid: 202000, cashBack: 0,      net: -202000 },
  hdb:   { paid: 454772, cashBack: 432886, net: -21886 },
  condo: { paid: 856981, cashBack: 935415, net: 78435 },
};
// Wealth at exit with the default cash & income (start $600,000, $8,000/mo, invested at 4%).
const expectWealth = { rent: 1173526, hdb: 1285699, condo: 1297074 };
let ok = true;
for (const [k, e] of Object.entries(expect)) {
  const r = sim[k].result;
  const got = { paid: r.paidNominal, cashBack: r.cashBack, net: r.gainNominal };
  for (const f of Object.keys(e)) {
    const diff = Math.abs(got[f] - e[f]);
    const line = `${k.padEnd(5)} ${f.padEnd(8)} expected ${e[f].toLocaleString()}  got ${Math.round(got[f]).toLocaleString()}`;
    if (diff > 50) { ok = false; console.error("FAIL " + line); } else console.log("ok   " + line);
  }
}
for (const [k, e] of Object.entries(expectWealth)) {
  const got = sim[k].result.wealth, line = `${k.padEnd(5)} wealth   expected ${e.toLocaleString()}  got ${Math.round(got).toLocaleString()}`;
  if (Math.abs(got - e) > 50) { ok = false; console.error("FAIL " + line); } else console.log("ok   " + line);
}
if (!ok) { console.error("\nThe default results changed. If that's intended, update tools/check.mjs and docs/methods.md."); process.exit(1); }
console.log("\nAll checks passed.");
