"""Build 3-year growth projections for Nifty 50 stocks from analyst consensus data.

Inputs: data.csv (price + 12-month analyst targets pulled from INDmoney, 30 Sep 2026 close).
Method:
  Year 1  = analyst 12-month target (mean / low / high for base / bear / bull).
  Years 2-3 = compounded at an assumed annual EPS growth rate for the sector,
              i.e. constant valuation multiple after year 1.
              Bear case uses half that growth rate.
"""
import csv

from meta import META

rows = []
with open("data.csv") as f:
    for r in csv.DictReader(f):
        sym = r["symbol"]
        name, sector, g = META[sym]
        p, t, lo, hi = (float(r[k]) for k in ("price", "target", "low", "high"))
        base = t * (1 + g) ** 2
        bear = lo * (1 + g / 2) ** 2
        bull = hi * (1 + g) ** 2
        cagr = lambda v: ((v / p) ** (1 / 3) - 1) * 100
        rows.append(dict(
            symbol=sym, company=name, sector=sector, price=p,
            target_12m=t, upside_12m=(t / p - 1) * 100,
            analysts=int(r["analysts"]), buy_pct=float(r["buy_pct"]),
            eps_growth_yr2_3=g * 100,
            bear_3y=bear, base_3y=base, bull_3y=bull,
            bear_cagr=cagr(bear), base_cagr=cagr(base), bull_cagr=cagr(bull),
        ))

rows.sort(key=lambda x: -x["base_cagr"])
assert len(rows) == 50, len(rows)

with open("nifty50_3yr_projections.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    for r in rows:
        w.writerow({k: round(v, 2) if isinstance(v, float) else v for k, v in r.items()})

def fmt(v):
    return f"{v:,.0f}" if v >= 100 else f"{v:,.1f}"

lines = [
    "| # | Stock | Sector | Price (₹) | 12m target (₹) | 12m upside | Analysts (% Buy) | Bear 3y (₹) | **Base 3y (₹)** | Bull 3y (₹) | **Base CAGR** | Range CAGR |",
    "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
]
for i, r in enumerate(rows, 1):
    lines.append(
        f"| {i} | {r['company']} ({r['symbol']}) | {r['sector']} | {fmt(r['price'])} | {fmt(r['target_12m'])} | "
        f"{r['upside_12m']:+.0f}% | {r['analysts']} ({r['buy_pct']:.0f}%) | {fmt(r['bear_3y'])} | **{fmt(r['base_3y'])}** | "
        f"{fmt(r['bull_3y'])} | **{r['base_cagr']:+.1f}%** | {r['bear_cagr']:+.0f}% to {r['bull_cagr']:+.0f}% |"
    )
open("table.md", "w").write("\n".join(lines) + "\n")

import statistics as s
print("median base CAGR", round(s.median(r["base_cagr"] for r in rows), 1))
print("median bear CAGR", round(s.median(r["bear_cagr"] for r in rows), 1))
print("median bull CAGR", round(s.median(r["bull_cagr"] for r in rows), 1))
print("top5", [(r["symbol"], round(r["base_cagr"], 1)) for r in rows[:5]])
print("bottom5", [(r["symbol"], round(r["base_cagr"], 1)) for r in rows[-5:]])
print("neg bear", [r["symbol"] for r in rows if r["bear_cagr"] < 0])
