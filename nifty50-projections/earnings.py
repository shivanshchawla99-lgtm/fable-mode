"""Rank Nifty 50 stocks by broker-estimated earnings CAGR, with P/E, into earnings_table.md / earnings_pe.csv.

Trailing P/E = 30 Sep 2026 close (data.csv) / FY26 EPS (fy26_eps.csv).
FY28E P/E    = same price / (FY26 EPS x (1 + CAGR)^2), only where the CAGR is an EPS/PAT
               figure for FY26-28E (EBITDA proxies and other periods are skipped).
"""
import csv

from meta import META

price = {r["symbol"]: float(r["price"]) for r in csv.DictReader(open("data.csv"))}
eps = {r["symbol"]: r for r in csv.DictReader(open("fy26_eps.csv"))}

rows = []
for r in csv.DictReader(open("eps_cagr.csv")):
    sym = r["symbol"]
    name, sector, _ = META[sym]
    cagr = float(r["earnings_cagr_pct"]) if r["earnings_cagr_pct"] else None
    e = float(eps[sym]["fy26_eps"]) if eps[sym]["fy26_eps"] else None
    pe = price[sym] / e if e else None
    fwd_ok = cagr is not None and e and r["period"] == "FY26-28E" and "proxy" not in r["metric"]
    fwd_pe = price[sym] / (e * (1 + cagr / 100) ** 2) if fwd_ok else None
    rows.append({**r, "company": name, "sector": sector, "cagr": cagr, "price": price[sym],
                 "fy26_eps": e, "pe": pe, "fwd_pe": fwd_pe,
                 "eps_basis": eps[sym]["basis"], "eps_source": eps[sym]["source"]})

found = sorted((r for r in rows if r["cagr"] is not None), key=lambda r: -r["cagr"])
missing = sorted((r for r in rows if r["cagr"] is None), key=lambda r: r["company"])


def fmt_pe(v, basis):
    if v is None:
        return "loss" if basis == "loss" else "n/m"
    return f"{v:.0f}x" if v < 1000 else f"{v:,.0f}x"


out = [
    "| # | Stock | Sector | Earnings CAGR | Trailing P/E | FY28E P/E | Period | Metric | Source | Note |",
    "|---|---|---|---:|---:|---:|---|---|---|---|",
]
for i, r in enumerate(found + missing, 1):
    rank = str(i) if r in found else "–"
    cagr = f"**{r['cagr']:.0f}%**" if r["cagr"] is not None else "n/a"
    fwd = f"{r['fwd_pe']:.0f}x" if r["fwd_pe"] else "–"
    out.append(
        f"| {rank} | {r['company']} ({r['symbol']}) | {r['sector']} | {cagr} | {fmt_pe(r['pe'], r['eps_basis'])} | {fwd} | "
        f"{r['period']} | {r['metric']} | {r['source']} | {r['note']} |"
    )
open("earnings_table.md", "w").write("\n".join(out) + "\n")

cols = ["symbol", "company", "sector", "price", "fy26_eps", "eps_basis", "eps_source", "pe",
        "earnings_cagr_pct", "period", "metric", "source", "fwd_pe", "note"]
with open("earnings_pe.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in found + missing:
        w.writerow({k: round(r[k], 1) if isinstance(r.get(k), float) else r.get(k) for k in cols})

pes = sorted(r["pe"] for r in rows if r["pe"] and r["symbol"] != "ETERNAL")
eps_only = sorted(r["cagr"] for r in found if "proxy" not in r["metric"] and r["symbol"] != "ETERNAL")
print("found", len(found), "missing", len(missing))
print("median CAGR (ex proxies, ex Eternal)", eps_only[len(eps_only) // 2], "n", len(eps_only))
print("median trailing PE (ex Eternal)", round(pes[len(pes) // 2], 1), "n", len(pes))
for r in sorted(rows, key=lambda r: r["pe"] or 0):
    print(r["symbol"], fmt_pe(r["pe"], r["eps_basis"]), f"{r['fwd_pe']:.0f}x" if r["fwd_pe"] else "-")
