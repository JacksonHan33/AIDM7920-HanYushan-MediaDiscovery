"""Use pytrends (Google Trends unofficial API) to fetch search interest
for video-discovery related queries over the last 5 years.
Saves CSV + a matplotlib chart.
"""
import sys
try:
    from pytrends.request import TrendReq
except ImportError:
    print("pytrends not installed. Run: pip3 install --user pytrends")
    sys.exit(1)

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import time

OUT_DIR = Path("/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery/data/raw")
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = ["what to watch", "JustWatch", "Reelgood", "best streaming service"]

pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2, backoff_factor=0.5)

# 1. Interest over time (last 5 years, monthly)
print("Fetching interest_over_time (5y, monthly)...")
pytrends.build_payload(QUERIES, timeframe='today 5-y', geo='')
iot = pytrends.interest_over_time()
if not iot.empty:
    iot = iot.drop(columns=[c for c in iot.columns if c == 'isPartial'], errors='ignore')
    iot.to_csv(OUT_DIR / "google_trends_5y.csv")
    print(f"  Saved {OUT_DIR/'google_trends_5y.csv'} ({len(iot)} rows)")

    # 2. Plot
    fig, ax = plt.subplots(figsize=(12, 5))
    for q in QUERIES:
        if q in iot.columns:
            ax.plot(iot.index, iot[q], label=q, linewidth=2)
    ax.set_title("Google Trends: Video-Discovery Search Interest (last 5 years)")
    ax.set_ylabel("Relative search interest (0-100)")
    ax.set_xlabel("Year")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "google_trends_5y.png", dpi=140, bbox_inches="tight")
    print(f"  Saved {OUT_DIR/'google_trends_5y.png'}")
else:
    print("  No data returned (rate limit or empty)")

# 3. Interest by region (last 12 months, top 15)
print("\nFetching interest_by_region...")
pytrends.build_payload(["what to watch"], timeframe='today 12-m', geo='')
ibr = pytrends.interest_by_region()
if not ibr.empty:
    top = ibr.sort_values("what to watch", ascending=False).head(15)
    top.to_csv(OUT_DIR / "google_trends_by_region.csv")
    print(f"  Saved top 15 regions to google_trends_by_region.csv")

# 4. Related queries
print("\nFetching related_queries...")
rq = pytrends.related_queries()
for q in QUERIES[:2]:
    if q in rq and rq[q].get("rising") is not None:
        rising = rq[q]["rising"].head(10)
        rising.to_csv(OUT_DIR / f"related_queries_{q.replace(' ', '_')}.csv", index=False)
        print(f"  Saved related queries for '{q}'")
