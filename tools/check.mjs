// Sanity check for site/index.html, run by the deploy workflow and locally with `node tools/check.mjs`.
// 1. Syntax-checks the page's inline JavaScript.
// 2. Runs the calculation engine on the built-in example (rent vs resale HDB vs new-launch condo)
//    and on one tile of every type, and compares wealth at exit with docs/methods.md (within $50).
//    Growth uses the built-in fallback, so the result doesn't depend on the live growth.json.
import { readFileSync } from "node:fs";
import vm from "node:vm";

const html = readFileSync(new URL("../site/index.html", import.meta.url), "utf8");
const js = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).join("\n");
if (!js) throw new Error("No inline <script> found in site/index.html");
new vm.Script(js); // throws on a syntax error

const cut = (a, b) => { const i = js.indexOf(a), j = js.indexOf(b); if (i < 0 || j < 0) throw new Error(`Marker missing: ${a}`); return js.slice(i, j); };
const code = cut("/* ================= ENGINE", "/* ================= END ENGINE")
  + cut("/* ================= SCENARIOS", "/* ================= END SCENARIOS");
const ctx = { structuredClone };
vm.createContext(ctx);
vm.runInContext(code + "\nthis.simulate=simulate; this.exampleState=exampleState; this.newTile=newTile; this.DEFAULTS=DEFAULTS;", ctx);

const example = ctx.simulate(ctx.exampleState());
const all = structuredClone(ctx.DEFAULTS);
["rent", "bto", "hdb", "rcondo", "ncondo"].forEach((t, i) => all.tiles.push(ctx.newTile(t, all, i + 1)));
const every = ctx.simulate(all);

const expect = [
  ["example", example, { "Rent": 1125720, "Resale HDB": 1230817, "New-launch condo": 1226247 }],
  ["one of each", every, { "Rent": 2095890, "BTO": 2996328, "Resale HDB": 2986181, "Resale condo": 3362375, "New-launch condo": 3176592 }],
];
let ok = true;
for (const [label, sim, want] of expect) {
  for (const [name, e] of Object.entries(want)) {
    const o = sim.tiles.find(x => x.t.name === name);
    const got = o ? o.wealth.final : NaN;
    const line = `${label.padEnd(12)} ${name.padEnd(17)} expected ${e.toLocaleString()}  got ${Math.round(got).toLocaleString()}`;
    if (!(Math.abs(got - e) <= 50)) { ok = false; console.error("FAIL " + line); } else console.log("ok   " + line);
  }
}
if (!ok) { console.error("\nThe default results changed. If that's intended, update tools/check.mjs and docs/methods.md."); process.exit(1); }
console.log("\nAll checks passed.");
