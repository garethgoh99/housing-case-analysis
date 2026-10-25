"""Default growth rates for the dashboard's tiles, from the two sister projects' data.

Writes data/growth.json, which the deploy workflow copies to site/growth.json. The page
loads it on start and uses it to prefill each tile's growth field (the user can override).

Sources
- HDB (Resale HDB and BTO tiles): quarterly all-Singapore median $psf published by
  hdb-resale-dashboard at q/sg.json.
- Condo (Resale condo and New-launch condo tiles): every URA private transaction in
  private-condo-analysis's permanent archive (raw-data branch). RCR, non-landed
  (Condominium + Apartment), as a deliberately middle-of-the-market proxy.
    * Resale condo:      resales only.
    * New-launch condo:  resales + sub-sales. New-sale prices track launch pricing, not how
                         a unit you own appreciates, so they are not used.

Method
- For each source, a 12-month (or 4-quarter) median $psf is compared with the same window a
  year earlier, giving up to 5 year-on-year growth rates, most recent first.
- These are blended with weights 40% / 25% / 15% / 10% / 10% (renormalised if fewer years
  exist), so the latest year counts most but the 5-year trend still shows through.

If a source can't be fetched, its previous value in data/growth.json is kept.

Usage:  python tools/growth.py [--condo-csv PATH] [--hdb-json PATH]
"""
import argparse, datetime as dt, gzip, io, json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "growth.json")
HDB_URL = "https://garethgoh99.github.io/hdb-resale-dashboard/q/sg.json"
CONDO_URL = "https://raw.githubusercontent.com/garethgoh99/private-condo-analysis/raw-data/archive/transactions.csv.gz"
WEIGHTS = [0.40, 0.25, 0.15, 0.10, 0.10]
PSF_MEDIAN = 15  # index of median $psf in hdb-resale-dashboard's 18-field quarterly records


def blend(yoy):
    w = WEIGHTS[:len(yoy)]
    return sum(a * b for a, b in zip(yoy, w)) / sum(w)


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def hdb_growth(raw):
    recs = json.loads(raw)["comb"]  # [qkey, n, ..., psf_median at 15, ...], qkey = year + (q-1)/4
    today = dt.date.today()
    cur_q = today.year + ((today.month - 1) // 3) / 4
    recs = [r for r in recs if r[0] < cur_q - 1e-9]  # drop the current, incomplete quarter
    by_q = {round(r[0], 2): r for r in recs}
    last = max(by_q)

    def window(end):  # n-weighted mean of 4 quarterly medians ending at `end`
        qs = [round(end - i / 4, 2) for i in range(4)]
        if not all(q in by_q for q in qs):
            return None
        n = sum(by_q[q][1] for q in qs)
        return sum(by_q[q][PSF_MEDIAN] * by_q[q][1] for q in qs) / n

    yoy = []
    for k in range(5):
        a, b = window(last - k), window(last - k - 1)
        if a is None or b is None:
            break
        yoy.append(a / b - 1)
    y, q = int(last), int(round((last % 1) * 4)) + 1
    return {"rate": blend(yoy), "yoy": yoy, "to": f"{y}Q{q}",
            "basis": "All-Singapore HDB resale, median $psf, 4 quarters vs the 4 before (hdb-resale-dashboard)"}


def condo_growth(raw):
    import csv
    rows = csv.DictReader(io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(raw)), encoding="utf-8"))
    rows = [r for r in rows if r["marketSegment"] == "RCR" and r["propertyType"] in ("Condominium", "Apartment")]
    today = dt.date.today()
    first_of_month = dt.date(today.year, today.month, 1)
    last_full = (first_of_month - dt.timedelta(days=1)).strftime("%Y-%m")
    months = sorted({r["month"] for r in rows if r["month"] <= last_full})
    last = months[-1]

    def shift(ym, years, months_=0):
        y, m = map(int, ym.split("-"))
        t = y * 12 + (m - 1) - years * 12 + months_
        return f"{t // 12}-{t % 12 + 1:02d}"

    def med(xs):
        xs = sorted(xs)
        n = len(xs)
        return None if not n else (xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2)

    out = {}
    for key, sales in (("condoResale", {"3"}), ("condoNew", {"2", "3"})):
        psf = {}
        for r in rows:
            if r["typeOfSale"] in sales and r["month"] <= last:
                try:
                    v = float(r["price"]) / (float(r["area"]) * 10.7639) / max(1.0, float(r["noOfUnits"] or 1))
                except ValueError:
                    continue
                psf.setdefault(r["month"], []).append(v)
        def window(k):
            end = shift(last, k); start = shift(end, 0, -11)
            if start < months[0]:
                return None
            return med([v for m, vs in psf.items() if start <= m <= end for v in vs])
        yoy = []
        for k in range(5):
            a, b = window(k), window(k + 1)
            if a is None or b is None:
                break
            yoy.append(a / b - 1)
        out[key] = {"rate": blend(yoy), "yoy": yoy, "to": last,
                    "basis": ("RCR condo resales" if key == "condoResale" else "RCR condo resales + sub-sales")
                             + ", median $psf, 12 months vs the 12 before (private-condo-analysis)"}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condo-csv"); ap.add_argument("--hdb-json")
    a = ap.parse_args()
    cur = json.load(open(OUT)) if os.path.exists(OUT) else {}
    ok = []
    try:
        raw = open(a.hdb_json, "rb").read() if a.hdb_json else fetch(HDB_URL)
        cur["hdb"] = hdb_growth(raw); ok.append("hdb")
    except Exception as e:  # keep the previous value
        print(f"HDB growth not updated: {e}", file=sys.stderr)
    try:
        raw = open(a.condo_csv, "rb").read() if a.condo_csv else fetch(CONDO_URL)
        cur.update(condo_growth(raw)); ok += ["condoResale", "condoNew"]
    except Exception as e:
        print(f"Condo growth not updated: {e}", file=sys.stderr)
    if ok:
        cur["updated"] = dt.date.today().isoformat()
    cur["weights"] = WEIGHTS
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(cur, open(OUT, "w"), indent=1)
    for k in ("hdb", "condoResale", "condoNew"):
        if k in cur:
            print(f"{k:12s} {cur[k]['rate']*100:5.2f}%  yoy {[round(x*100, 2) for x in cur[k]['yoy']]}  to {cur[k]['to']}")


if __name__ == "__main__":
    main()
