# Rent vs Resale HDB vs Private Condo

An interactive dashboard that compares three housing paths in Singapore from today to a sale date: **renting**, buying a **resale HDB flat**, and buying a **new-launch private condo** on progressive payment. It works out, month by month, what each path costs and what you get back when you sell, and is served on GitHub Pages.

Sister project of [hdb-resale-dashboard](https://github.com/garethgoh99/hdb-resale-dashboard) and [private-condo-analysis](https://github.com/garethgoh99/private-condo-analysis).

**Live dashboard:** https://garethgoh99.github.io/housing-case-analysis/ (once Pages is switched on, see *One-time setup*)

## What it shows

- **Fair comparison by wealth:** all three paths start with the same cash and get the same monthly income. Whatever isn't spent on housing is invested at a return you set, and running out of cash costs shortfall interest. The verdict ranks the paths by **wealth at exit** (invested cash + sale proceeds), so a path that ties up more money in the home has to beat what that money would have earned invested.
- **Cards:** wealth at exit with its breakdown, the lowest cash balance (flagged if it goes negative), and net gain at exit for each path (cash back from the sale minus everything paid in), with the breakdown behind it: loan, instalment, sale price, loan payoff, selling costs and SSD, price growth and the return on your cash (IRR).
- **Time value of money:** optional. Discounts every monthly flow and the sale proceeds to the start month, so the comparison becomes an NPV.
- **Charts:** net worth (invested cash + home equity), invested cash, net cost if you sold in any month, equity built, total paid out, and monthly cash out.
- **Timeline:** renting, loan and milestone dates (completion, keys, MOP, OTP, TOP, CSC) for each path.
- **Month-by-month table:** every month's payments, equity change and cash balance, with a milestone-only filter and copy-as-CSV.
- **Inputs:** yellow *key* fields first, everything else under *More settings*. Covers SORA (with a stress-test picker) and bank spread, HDB vs bank loan, LTV and tenure with MAS caps, ABSD, renovation, renting while you wait for keys, the condo's progressive payment milestones (auto-estimated or edited by hand), growth presets, and agent and legal fees on sale. An optional household income turns on MSR and TDSR checks.

Inputs are saved in the viewer's browser (`localStorage`), so nothing leaves the page. **Reset to defaults** restores the scenario below.

See [`docs/methods.md`](docs/methods.md) for every rule the calculation uses and the default scenario.

## Default scenario (Oct 2026)

Start Oct 2026, exit Aug 2032 (HDB keys + 5-year MOP), HDB growth 2.0% and condo 2.5% a year. Each path starts with $600,000 and gets $8,000 a month, invested at 4%. The cash and income figures are placeholders; set your own.

| Case | Wealth at exit | Net gain on housing |
|---|---|---|
| Rent | $1,173,526 | −$202,000 |
| Resale HDB | $1,285,699 | −$21,886 |
| Condo | **$1,297,074** | +$78,435 |

On net gain alone the condo is $100K ahead of the HDB. Once the HDB buyer's spare cash is invested, the gap shrinks to about $11K, and at a 6% return the HDB comes out ahead. Rough guide only, not financial advice.

## How it's deployed

The dashboard is a single self-contained page, `site/index.html`. Chart.js loads from jsDelivr and the fonts from Google Fonts; everything else is inline. There's no build step and no data pull.

`.github/workflows/deploy.yml` runs on every push to `main` that touches `site/`, `tools/` or the workflow, and from **Actions → Deploy dashboard → Run workflow**:

1. **`tools/check.mjs`** syntax-checks the page's JavaScript, then runs the calculation engine on the default scenario and checks the net gain and wealth figures still match the table above (within $50).
2. The workflow deploys `site/` to GitHub Pages.

If the check fails, nothing is deployed and the previous dashboard stays live. If you change the defaults or the maths on purpose, update the expected figures in `tools/check.mjs` and `docs/methods.md` in the same commit.

## One-time setup

1. Go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
2. Go to **Actions → Deploy dashboard → Run workflow** (or push any change to `site/`).

## Run locally

```bash
node tools/check.mjs      # optional: same check the workflow runs
open site/index.html      # or just double-click it
```

## Repo layout

| Path | What it is |
|---|---|
| `site/index.html` | The dashboard. |
| `tools/check.mjs` | JavaScript syntax check plus a regression test of the default results. |
| `docs/methods.md` | Calculation rules, default scenario, sources and open ideas. |
| `reference/Rent_vs_HDB_vs_Condo.xlsx` | The earlier monthly spreadsheet (Oct 2026 – Jan 2035). It has no growth or exit modelling and predates the rent-while-waiting changes; kept for reference. |
| `.github/workflows/deploy.yml` | Check and deploy to Pages. |
