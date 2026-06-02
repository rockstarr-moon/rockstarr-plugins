#!/usr/bin/env python3
"""Phase 2 — indexability fundamentals.

Usage:
    python3 check_indexability.py https://example.com/

Runs the cheap checks that determine whether Google can crawl + index the site
at all. Prints pass/fail per check. Anything red here jumps to Critical in the
audit.
"""

import argparse
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UAS = {
    "browser-mac": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "browser-windows": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl": "curl/8.0",
    "googlebot": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
}


def head(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua}, method="HEAD")
    try:
        # urlopen doesn't follow redirects on HEAD by default; we want to see them
        opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
        with opener.open(req, timeout=15) as r:
            return r.status, dict(r.headers), r.url
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), url
    except Exception as e:
        return 0, {"_error": str(e)}, url


def get(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode("utf-8", errors="ignore")
            return r.status, dict(r.headers), body, r.url
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), "", url
    except Exception as e:
        return 0, {"_error": str(e)}, "", url


def extract_meta(html, name):
    m = re.search(
        r'<meta\s+(?:name|property)=["\']' + re.escape(name) + r'["\']\s+content=["\'](.*?)["\']',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    return m.group(1) if m else None


def extract_canonical(html):
    m = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.IGNORECASE
    )
    return m.group(1) if m else None


def extract_title(html):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("base", help="Site root URL (e.g. https://example.com/)")
    args = p.parse_args()

    base = args.base.rstrip("/") + "/"
    parsed = urllib.parse.urlparse(base)
    apex = parsed.netloc.lstrip("www.")
    www_form = f"{parsed.scheme}://www.{apex}/"
    apex_form = f"{parsed.scheme}://{apex}/"
    http_form = f"http://{apex}/"
    http_www_form = f"http://www.{apex}/"

    print(f"=== Indexability check: {base} ===\n")

    # 1. robots.txt
    print("[1] robots.txt")
    status, _, body, _ = get(base + "robots.txt", UAS["googlebot"])
    print(f"  HTTP {status}, {len(body)} bytes")
    if status == 200:
        for line in body.splitlines():
            ls = line.strip().lower()
            if ls.startswith("disallow:"):
                rule = line.split(":", 1)[1].strip()
                if rule == "/":
                    print(f"  RED FLAG: site-wide Disallow rule: {line.strip()}")
                elif rule and "*" not in rule and rule != "":
                    print(f"  Disallow: {rule}")
            if ls.startswith("sitemap:"):
                print(f"  {line.strip()}")
    else:
        print("  RED FLAG: robots.txt not 200")

    # 2. sitemap.xml
    print("\n[2] sitemap.xml")
    status, _, body, _ = get(base + "sitemap.xml", UAS["googlebot"])
    print(f"  HTTP {status}, {len(body)} bytes")
    if status == 200:
        urls = re.findall(r"<loc>(.*?)</loc>", body)
        lastmods = re.findall(r"<lastmod>(.*?)</lastmod>", body)
        print(f"  URLs in sitemap: {len(urls)}")
        if lastmods:
            print(f"  Most recent lastmod: {max(lastmods)}")
            print(f"  Oldest lastmod: {min(lastmods)}")

    # 3. Homepage canonical + meta robots
    print("\n[3] Homepage canonical + meta robots")
    status, _, body, _ = get(base, UAS["googlebot"])
    print(f"  HTTP {status}, {len(body)} bytes")
    canonical = extract_canonical(body)
    robots_meta = extract_meta(body, "robots")
    title = extract_title(body)
    print(f"  Title: {title}")
    print(f"  Canonical: {canonical}")
    print(f"  Meta robots: {robots_meta}")
    if canonical and apex not in canonical:
        print(f"  RED FLAG: canonical points off-domain")
    if robots_meta and ("noindex" in robots_meta.lower()):
        print(f"  RED FLAG: homepage carries noindex")

    # 4. www / apex / http redirects
    print("\n[4] HTTPS + www canonicalization")
    for label, url in [
        ("http apex", http_form),
        ("http www", http_www_form),
        ("https www", www_form),
    ]:
        status, headers, final_url = head(url, UAS["googlebot"])
        loc = headers.get("Location") or headers.get("location") or ""
        print(f"  {label} {url} => {status} {('-> ' + loc) if loc else ''}")

    # 5. Cache integrity: do different UAs see the same content?
    print("\n[5] Cache integrity (different UAs)")
    titles = {}
    canons = {}
    for ua_name, ua in UAS.items():
        status, _, body, _ = get(base + f"?cb_check={ua_name}", ua)
        titles[ua_name] = extract_title(body) or "(no title)"
        canons[ua_name] = extract_canonical(body) or "(no canonical)"
    seen_titles = set(titles.values())
    seen_canons = set(canons.values())
    for ua_name in UAS:
        print(f"  {ua_name}: title={titles[ua_name][:60]} canonical={canons[ua_name]}")
    if len(seen_titles) > 1:
        print(f"  RED FLAG: title differs across UAs — possible CDN edge cache leak")
    if len(seen_canons) > 1:
        print(f"  RED FLAG: canonical differs across UAs — possible CDN edge cache leak")

    print("\nDone. Anything marked RED FLAG goes in Critical (after re-verification).")


if __name__ == "__main__":
    sys.exit(main() or 0)
