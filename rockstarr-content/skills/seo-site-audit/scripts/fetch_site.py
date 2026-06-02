#!/usr/bin/env python3
"""Fetch homepage + top pages + sitemap + robots.txt for an SEO audit.

Usage:
    python3 fetch_site.py https://example.com/ --out /tmp/audit-example
    python3 fetch_site.py https://example.com/ --out /tmp/audit-example --extra services about contact

Pulls with a Googlebot user agent because that's what matters for SEO.
Saves HTML files to <out>/<slug>.html and prints a one-line summary per URL.
"""

import argparse
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# Default paths to try on top of homepage. Real audits should add more from
# the client's sitemap or nav.
DEFAULT_PATHS = [
    "",
    "services/",
    "about/",
    "about-us/",
    "who-we-are/",
    "contact/",
    "contact-us/",
    "blog/",
]


def fetch(url, timeout=30):
    """GET a URL with Googlebot UA. Returns (status, headers, body_bytes)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), e.read() if e.fp else b""
    except Exception as e:
        return 0, {}, str(e).encode()


def slug(path):
    s = path.strip("/").replace("/", "_") or "home"
    return s + ".html"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("base", help="Base URL of the site (e.g. https://example.com/)")
    p.add_argument("--out", required=True, help="Output directory")
    p.add_argument("--extra", nargs="*", default=[], help="Extra paths to fetch")
    args = p.parse_args()

    base = args.base.rstrip("/") + "/"
    out = args.out
    os.makedirs(out, exist_ok=True)

    # Pull robots.txt + sitemap separately
    for name, suffix in [("robots.txt", "robots.txt"), ("sitemap.xml", "sitemap.xml")]:
        url = urllib.parse.urljoin(base, suffix)
        status, _, body = fetch(url)
        target = os.path.join(out, name)
        with open(target, "wb") as f:
            f.write(body)
        print(f"  {url} => {status} ({len(body)}b) -> {target}")

    # Pull pages
    paths = list(dict.fromkeys(DEFAULT_PATHS + args.extra))
    for path in paths:
        url = urllib.parse.urljoin(base, path)
        status, _, body = fetch(url)
        target = os.path.join(out, slug(path))
        with open(target, "wb") as f:
            f.write(body)
        print(f"  {url} => {status} ({len(body)}b) -> {target}")

    print(f"\nDone. Output in: {out}")
    print("Next: parse with extract_on_page.py and extract_schema.py.")


if __name__ == "__main__":
    sys.exit(main() or 0)
