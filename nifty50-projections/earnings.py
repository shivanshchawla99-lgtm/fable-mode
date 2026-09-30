"""Rank Nifty 50 stocks by broker-estimated earnings CAGR (eps_cagr.csv) into earnings_table.md."""
import csv

from meta import META

rows = []
for r in csv.DictReader(open("eps_cagr.csv")):
    name, sector, _ = META[r["symbol"]]
    cagr = float(r["earnings_cagr_pct"]) if r["earnings_cagr_pct"] else None
    rows.append({**r, "company": name, "sector": sector, "cagr": cagr})

found = sorted((r for r in rows if r["cagr"] is not None), key=lambda r: -r["cagr"])
missing = sorted((r for r in rows if r["cagr"] is None), key=lambda r: r["company"])

out = [
    "| # | Stock | Sector | Earnings CAGR | Period | Metric | Source | Note |",
    "|---|---|---|---:|---|---|---|---|",
]
for i, r in enumerate(found, 1):
    out.append(
        f"| {i} | {r['company']} ({r['symbol']}) | {r['sector']} | **{r['cagr']:.0f}%** | {r['period']} | "
        f"{r['metric']} | {r['source']} | {r['note']} |"
    )
for r in missing:
    out.append(f"| – | {r['company']} ({r['symbol']}) | {r['sector']} | n/a | | | | {r['note']} |")
open("earnings_table.md", "w").write("\n".join(out) + "\n")

eps_only = [r["cagr"] for r in found if "proxy" not in r["metric"] and r["symbol"] != "ETERNAL"]
eps_only.sort()
print("found", len(found), "missing", len(missing))
print("median (ex proxies, ex Eternal)", eps_only[len(eps_only) // 2], "n", len(eps_only))
