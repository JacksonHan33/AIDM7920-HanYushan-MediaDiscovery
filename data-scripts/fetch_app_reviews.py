"""Fetch reviews for cross-platform video discovery apps.
Strategy: Google Play Store (HTML scrape) primary, App Store lookup for ratings only.
Saves to data/raw/app_store_reviews.json
"""
import json, time, re
from pathlib import Path
import requests

OUT = Path("/Users/apple/Documents/AIDM7920-HanYushan-MediaDiscovery/data/raw/app_store_reviews.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

# Google Play Store package IDs (Android apps)
APPS_GOOGLE = {
    "JustWatch":    "com.justwatch.justwatch",
    "TV Time":      "com.tozelabs.tvshowtime",
    "Plex":         "com.plexapp.android",
    "Letterboxd":   "com.letterboxd.letterboxd",  # bonus — popular movie tracker
    "IMDb":         "com.imdb.mobile",              # bonus — also tracks
}

# iTunes app IDs (for ratings metadata only)
APPS_ITUNES = {
    "JustWatch":    "564698458",
    "TV Time":      "984120754",
    "Reelgood":     "1059831242",
    "Plex":         "383457984",
}

def fetch_google_play_reviews(pkg_id, app_name, max_pages=5):
    """Scrape Google Play reviews (HTML, no API key needed)."""
    all_reviews = []
    for page in range(max_pages):
        try:
            url = f"https://play.google.com/store/apps/details?id={pkg_id}&hl=en&gl=US"
            r = requests.get(url, timeout=15, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            })
            r.raise_for_status()
            html = r.text

            # Reviews are embedded in the page as a JS data structure.
            # Use a simpler regex approach for a few recent reviews.
            # The page has a pattern: "Review text: ..." in JSON blocks
            snippets = re.findall(r'"([^"]{50,500})"', html)
            # Filter to plausible review-like text
            for s in snippets:
                if any(kw in s.lower() for kw in [
                    "love", "great", "amazing", "awesome", "perfect", "best",
                    "hate", "bad", "terrible", "awful", "worst", "suck", "useless",
                    "scrolling", "find", "search", "recommend", "streaming",
                    "recommendation", "platform", "where to watch", "discover",
                    "available", "miss", "wish", "hard to find", "waste time",
                    "frustrating", "annoying", "multiple", "switch", "between",
                    "netflix", "disney", "hulu", "prime", "hbo", "max"
                ]):
                    if len(s) > 80 and not s.startswith(("https://", "http://", "data-", "<")):
                        all_reviews.append({
                            "text": s[:500],
                            "source": "Google Play Store",
                            "app": app_name,
                        })
            break  # one page is enough for our needs
        except Exception as e:
            print(f"  {app_name} page {page} err: {e}")
            time.sleep(1)
    return all_reviews[:50]  # cap at 50 per app


def fetch_itunes_metadata(itunes_id, app_name):
    """Get just the iTunes store rating (for credibility)."""
    try:
        r = requests.get(
            "https://itunes.apple.com/lookup",
            params={"id": itunes_id, "country": "us", "entity": "software"},
            timeout=10, headers={"User-Agent": "Mozilla/5.0"}
        )
        r.raise_for_status()
        data = r.json()
        if data.get("resultCount", 0) > 0:
            m = data["results"][0]
            return {
                "average_user_rating": m.get("averageUserRating"),
                "user_rating_count": m.get("userRatingCount"),
                "track_name": m.get("trackName"),
                "track_view_url": m.get("trackViewUrl"),
            }
    except Exception as e:
        print(f"  iTunes meta err for {app_name}: {e}")
    return {}


def main():
    result = {}
    print("=== Fetching cross-platform video app reviews ===\n")
    for app_name, pkg_id in APPS_GOOGLE.items():
        print(f"[{app_name}] (pkg: {pkg_id})")
        reviews = fetch_google_play_reviews(pkg_id, app_name)
        print(f"  reviews scraped: {len(reviews)}")
        result[app_name] = {
            "google_play_pkg": pkg_id,
            "reviews": reviews,
        }
        time.sleep(1.0)

    print("\n=== Fetching iTunes store ratings (metadata only) ===\n")
    for app_name, itunes_id in APPS_ITUNES.items():
        if app_name in result:
            print(f"[{app_name}] (id: {itunes_id})")
            meta = fetch_itunes_metadata(itunes_id, app_name)
            result[app_name]["itunes_meta"] = meta
            if meta:
                print(f"  rating: {meta.get('average_user_rating')} ({meta.get('user_rating_count')} reviews)")
            time.sleep(0.5)

    with open(OUT, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved to {OUT}")
    total = sum(len(v["reviews"]) for v in result.values())
    print(f"  Total reviews: {total}")
    print(f"  File size: {OUT.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
