# Housing Case Comparison

An interactive dashboard that compares housing paths in Singapore on **total wealth at exit**. You add the cases you're weighing as tiles: rent, BTO, resale HDB, resale condo and new-launch condo, as many of each as you like. It works out month by month what each costs, what's left to invest, and what you have after selling. It is served on GitHub Pages.

Sister project of [hdb-resale-dashboard](https://github.com/garethgoh99/hdb-resale-dashboard) and [private-condo-analysis](https://github.com/garethgoh99/private-condo-analysis), whose data supplies the growth defaults.

**Live dashboard:** https://garethgoh99.github.io/housing-case-analysis/ (once Pages is switched on, see *One-time setup*)

The design rule: allow for flexibility and nuance, but default to what you'd expect, so the tool stays quick to use. Yellow *key* fields first; everything else is prefilled under *More settings*.

## What it does

- **Tiles:** start empty and add Rent, BTO, Resale HDB, Resale condo or New-launch condo. Rename, duplicate, collapse or remove any tile, and add the same type twice to compare two options.
- **A fair comparison:** every case gets the same starting cash, income and living costs. What housing doesn't use is invested at a return you set; running out of cash costs shortfall interest. A path that ties up more money in the home has to beat what that money would have earned invested.
- **Where you live:** each buying case rents (or lives with family) until move-in, on a schedule that can change over time. If it sells before the others, it rents afterwards until the comparison ends.
- **Running costs from move-in:** utilities, condo maintenance, HDB service & conservancy charges and property tax start only when you live there.
- **Exits:** by default everything is sold in the same month, the latest of each case's earliest sensible sale (MOP for HDB and BTO, SSD-free for condos). You can set it by hand, or give any case its own sale date.
- **Case-specific rules:**
  - BTO: booking, agreement for lease and keys payments; Plus/Prime 10-year MOP and clawback; market value above the BTO price; grants.
  - Resale condo: option, exercise and completion.
  - New-launch condo: progressive payment by stage.
  - HDB and bank loans with MAS LTV caps, BSD/ABSD, and SSD.
- **Growth autofill** for each tile from your other two dashboards' data: a 5-year blend weighted to the latest year. HDB resale for HDB and BTO; RCR condo resales (plus sub-sales for new launches) for condos.
- **Results:**
  - The verdict, and a card per case with the wealth breakdown, lowest cash balance, sale breakdown, net gain on the home and return on the cash in it.
  - Charts of net worth, invested cash, home equity, total paid out and monthly cash out.
  - A timeline and a month-by-month table with copy-as-CSV.

Inputs are saved in the viewer's browser (`localStorage`), so nothing leaves the page. **Load example** recreates the original rent vs resale HDB vs new-launch condo comparison.

See [`docs/methods.md`](docs/methods.md) for every rule, default and source.

## How it's deployed

The dashboard is one self-contained page, `site/index.html`. Chart.js loads from jsDelivr and the fonts from Google Fonts; everything else is inline. The only data it loads is `growth.json`, from the same site.

`.github/workflows/deploy.yml` runs on every push to `main`, every Monday at 03:43 SGT, and from **Actions → Deploy dashboard → Run workflow**:

1. **`tools/growth.py`** recomputes the growth defaults from your two sister projects and writes `data/growth.json`. If a source can't be reached, its last value is kept.
2. **`tools/check.mjs`** syntax-checks the page's JavaScript, then runs the engine on the built-in example and on one tile of each type. It checks wealth at exit still matches `docs/methods.md` (within $50).
3. The workflow copies `data/growth.json` into `site/`, commits it if the defaults changed, and deploys `site/` to GitHub Pages.

If the check fails, nothing is deployed and the previous dashboard stays live. If you change the maths or the defaults on purpose, update the expected figures in `tools/check.mjs` and `docs/methods.md` in the same commit.

## One-time setup

1. Go to **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
2. Go to **Actions → Deploy dashboard → Run workflow** (or push any change).

## Run locally

```bash
node tools/check.mjs      # same check the workflow runs
python tools/growth.py    # optional: refresh data/growth.json
open site/index.html      # growth.json won't load from a file:// page; the built-in values are used
```

## Repo layout

| Path | What it is |
|---|---|
| `site/index.html` | The dashboard. |
| `data/growth.json` | Current growth defaults (copied to `site/growth.json` on deploy). |
| `tools/growth.py` | Computes the growth defaults from the sister projects' data. |
| `tools/check.mjs` | JavaScript syntax check plus a regression test of the example results. |
| `docs/methods.md` | Calculation rules, defaults, sources and open ideas. |
| `reference/Rent_vs_HDB_vs_Condo.xlsx` | The earliest monthly spreadsheet version; kept for reference. |
| `.github/workflows/deploy.yml` | Refresh, check and deploy to Pages. |

Rough guide only, not financial advice.
