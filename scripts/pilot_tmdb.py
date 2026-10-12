"""
pilot_tmdb.py — Phase 1 pilot data
Fetch top 20 popular movies from TMDB and their streaming availability
across 5 regions. Save to data/pilot/tmdb_top20.json.

Phase 1 pilot: validates feasibility of our cross-platform analysis.
"""
import os
import json
import time
from pathlib import Path
import requests

API_KEY = os.environ.get("TMDB_API_KEY")
if not API_KEY:
    raise SystemExit(
        "TMDB_API_KEY not set.\n"
        "Run:   export TMDB_API_KEY=your_key_here\n"
        "Then re-run this script."
    )

BASE = "https://api.themoviedb.org/3"
LANG = "en-US"

# Region codes per TMDB convention
REGIONS = [
    ("US", "United States"),
    ("GB", "United Kingdom"),
    ("HK", "Hong Kong"),
    ("CN", "China"),
    ("JP", "Japan"),
]

OUT_DIR = Path("data/pilot")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def tmdb_get(path, params=None):
    """GET a TMDB endpoint with API key + language + timeout."""
    params = dict(params or {})
    params["api_key"] = API_KEY
    params["language"] = LANG
    r = requests.get(BASE + path, params=params, timeout=15)
    if r.status_code != 200:
        raise SystemExit(
            f"TMDB API error {r.status_code} for {path}: {r.text[:200]}"
        )
    return r.json()


def fetch_popular(n=20):
    """Fetch top N currently popular movies."""
    movies, page = [], 1
    while len(movies) < n:
        data = tmdb_get("/movie/popular", {"page": page})
        movies.extend(data.get("results", []))
        total_pages = min(data.get("total_pages", 1), 5)  # cap
        if page >= total_pages:
            break
        page += 1
    return movies[:n]


def fetch_providers(movie_id):
    """Fetch watch providers for a movie across our regions."""
    data = tmdb_get(f"/movie/{movie_id}/watch/providers")
    out = {}
    for code, _name in REGIONS:
        r = data.get("results", {}).get(code, {})
        entries = []
        # subscription / rental / purchase / free / ad-supported
        for category in ("flatrate", "rent", "buy", "free", "ads"):
            for p in r.get(category, []):
                entries.append({
                    "name": p["provider_name"],
                    "category": category,
                    "logo": p.get("logo_path"),
                })
        out[code] = {
            "link": r.get("link"),  # deep link to JustWatch for that region
            "providers": entries,
        }
    return out


def main():
    print("=" * 70)
    print("TMDB pilot data — COMM7660 Phase 1")
    print("=" * 70)
    print(f"API key: {API_KEY[:6]}...{API_KEY[-4:]}  (len {len(API_KEY)})")
    print(f"Regions: {[c for c, _ in REGIONS]}")
    print()

    print("Fetching top 20 popular movies from TMDB...")
    movies = fetch_popular(20)
    print(f"Got {len(movies)} movies.\n")

    enriched = []
    for m in movies:
        title = m["title"]
        year = (m.get("release_date") or "?")[:4]
        print(f"  [{len(enriched)+1:2d}/20] {title} ({year}) ... ", end="", flush=True)
        try:
            providers = fetch_providers(m["id"])
            print("ok")
        except Exception as e:
            print(f"FAILED: {e}")
            providers = {}
        enriched.append({
            "id": m["id"],
            "title": title,
            "original_title": m.get("original_title"),
            "release_date": m.get("release_date"),
            "vote_average": m.get("vote_average"),
            "vote_count": m.get("vote_count"),
            "popularity": m.get("popularity"),
            "overview": (m.get("overview") or "")[:300],
            "providers": providers,
        })
        time.sleep(0.25)  # polite rate limit

    out_path = OUT_DIR / "tmdb_top20.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {len(enriched)} records to {out_path}")

    # ----- Summary table -----
    print("\n" + "=" * 70)
    print("Cross-platform availability (subscription only)")
    print("=" * 70)
    header = f"{'#':<3} {'Title':<32} " + " ".join(f"{c:<16}" for c, _ in REGIONS)
    print(header)
    print("-" * len(header))
    for i, m in enumerate(enriched, 1):
        title = m["title"][:30]
        cells = []
        for code, _ in REGIONS:
            ps = m["providers"].get(code, {}).get("providers", [])
            flatrate = sorted({p["name"] for p in ps if p["category"] == "flatrate"})
            cells.append(",".join(flatrate)[:14] or "—")
        print(f"{i:<3} {title:<32} " + " ".join(f"{c:<16}" for c in cells))

    print("\nDone. Open data/pilot/tmdb_top20.json for the full record.")
    print("Next step: review this pilot before scaling up the dataset.")


if __name__ == "__main__":
    main()
