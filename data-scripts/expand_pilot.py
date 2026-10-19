"""Expand TMDB pilot from 20 to 200 popular movies.
Saves to data/pilot/tmdb_market_200.json with full metadata
and watch_providers for US, GB, HK, CN, JP.
"""
import os, json, time
from pathlib import Path

API = os.environ.get("TMDB_API_KEY")
if not API:
    raise SystemExit("TMDB_API_KEY not set. Run: source ~/.zshrc")
REGIONS = ["US", "GB", "HK", "CN", "JP"]
PAGES = 12  # 12 pages x 20 = 240 candidates
OUT = Path("/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery/data/pilot/tmdb_market_200.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

def tmdb_get(path, **params):
    params["api_key"] = API
    params.setdefault("language", "en-US")
    r = __import__("requests").get(f"https://api.themoviedb.org/3{path}", params=params, timeout=15)
    r.raise_for_status()
    return r.json()

# Step 1: collect candidate movies
candidates = []
for page in range(1, PAGES+1):
    d = tmdb_get("/movie/popular", page=page)
    candidates.extend(d.get("results", []))
    print(f"  page {page}: {len(candidates)} total candidates")
    time.sleep(0.30)

# Step 2: dedupe by id
seen = set()
unique = []
for m in candidates:
    if m["id"] not in seen:
        seen.add(m["id"])
        unique.append(m)

# Step 3: for each unique movie, fetch watch_providers for 5 regions; keep if available in >=2 regions
print(f"\nFetching watch_providers for {len(unique)} candidates...")
clean = []
for i, m in enumerate(unique):
    if len(clean) >= 200:
        break
    try:
        wp = tmdb_get(f"/movie/{m['id']}/watch/providers")
        results = wp.get("results", {})
        region_data = {r: results[r] for r in REGIONS if r in results}
        if len(region_data) >= 2:  # keep if available in >=2 regions
            m["region_providers"] = region_data
            m["_n_platforms_total"] = sum(
                len(set(p["provider_name"]
                        for cat in ["flatrate", "rent", "buy", "free"]
                        for p in region_data[r].get(cat, [])))
                for r in region_data
            )
            clean.append(m)
    except Exception as e:
        print(f"  err {m['id']}: {e}")
    if (i+1) % 25 == 0:
        print(f"  ... {i+1}/{len(unique)} processed, {len(clean)} kept so far")
    time.sleep(0.15)

print(f"\nFinal: {len(clean)} movies across {len(REGIONS)} regions")
print(f"Writing to {OUT}")
with open(OUT, "w") as f:
    json.dump(clean, f, indent=2)
print(f"File size: {OUT.stat().st_size / 1024:.1f} KB")
