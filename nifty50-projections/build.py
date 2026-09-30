"""Build 3-year growth projections for Nifty 50 stocks from analyst consensus data.

Inputs: data.csv (price + 12-month analyst targets pulled from INDmoney, 30 Sep 2026 close).
Method:
  Year 1  = analyst 12-month target (mean / low / high for base / bear / bull).
  Years 2-3 = compounded at an assumed annual EPS growth rate for the sector,
              i.e. constant valuation multiple after year 1.
              Bear case uses half that growth rate.
"""
import csv

# symbol: (company, sector, assumed EPS growth for years 2-3)
META = {
    "ADANIENT": ("Adani Enterprises", "Diversified / Infra", 0.15),
    "ADANIPORTS": ("Adani Ports & SEZ", "Ports & Logistics", 0.15),
    "APOLLOHOSP": ("Apollo Hospitals", "Healthcare", 0.18),
    "ASIANPAINT": ("Asian Paints", "Consumer Durables", 0.10),
    "AXISBANK": ("Axis Bank", "Private Bank", 0.14),
    "BAJAJ-AUTO": ("Bajaj Auto", "Auto", 0.11),
    "BAJFINANCE": ("Bajaj Finance", "NBFC", 0.18),
    "BAJAJFINSV": ("Bajaj Finserv", "Financial Holding", 0.15),
    "BEL": ("Bharat Electronics", "Defence", 0.16),
    "BHARTIARTL": ("Bharti Airtel", "Telecom", 0.16),
    "BSE": ("BSE Ltd (new entrant)", "Capital Markets", 0.18),
    "CIPLA": ("Cipla", "Pharma", 0.10),
    "COALINDIA": ("Coal India", "Mining", 0.04),
    "DRREDDY": ("Dr Reddy's Labs", "Pharma", 0.08),
    "EICHERMOT": ("Eicher Motors", "Auto", 0.13),
    "ETERNAL": ("Eternal (Zomato)", "Consumer Internet", 0.25),
    "GRASIM": ("Grasim Industries", "Cement / Diversified", 0.12),
    "HCLTECH": ("HCL Technologies", "IT Services", 0.08),
    "HDFCBANK": ("HDFC Bank", "Private Bank", 0.14),
    "HDFCLIFE": ("HDFC Life", "Insurance", 0.14),
    "HINDALCO": ("Hindalco", "Metals", 0.08),
    "HINDUNILVR": ("Hindustan Unilever", "FMCG", 0.09),
    "ICICIBANK": ("ICICI Bank", "Private Bank", 0.15),
    "INDIGO": ("InterGlobe Aviation", "Aviation", 0.12),
    "INFY": ("Infosys", "IT Services", 0.08),
    "ITC": ("ITC", "FMCG", 0.08),
    "JIOFIN": ("Jio Financial Services", "NBFC", 0.20),
    "JSWSTEEL": ("JSW Steel", "Metals", 0.10),
    "KOTAKBANK": ("Kotak Mahindra Bank", "Private Bank", 0.13),
    "LT": ("Larsen & Toubro", "Capital Goods", 0.15),
    "M&M": ("Mahindra & Mahindra", "Auto", 0.14),
    "MARUTI": ("Maruti Suzuki", "Auto", 0.11),
    "MAXHEALTH": ("Max Healthcare", "Healthcare", 0.20),
    "NESTLEIND": ("Nestle India", "FMCG", 0.09),
    "NTPC": ("NTPC", "Power", 0.09),
    "ONGC": ("ONGC", "Oil & Gas", 0.05),
    "POWERGRID": ("Power Grid", "Power", 0.08),
    "RELIANCE": ("Reliance Industries", "Conglomerate", 0.12),
    "SBILIFE": ("SBI Life", "Insurance", 0.14),
    "SBIN": ("State Bank of India", "PSU Bank", 0.11),
    "SHRIRAMFIN": ("Shriram Finance", "NBFC", 0.16),
    "SUNPHARMA": ("Sun Pharma", "Pharma", 0.11),
    "TATACONSUM": ("Tata Consumer Products", "FMCG", 0.12),
    "TATASTEEL": ("Tata Steel", "Metals", 0.10),
    "TCS": ("Tata Consultancy Services", "IT Services", 0.08),
    "TECHM": ("Tech Mahindra", "IT Services", 0.10),
    "TITAN": ("Titan Company", "Consumer Discretionary", 0.16),
    "TMPV": ("Tata Motors Passenger Vehicles", "Auto", 0.08),
    "TRENT": ("Trent", "Retail", 0.20),
    "ULTRACEMCO": ("UltraTech Cement", "Cement", 0.14),
}

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
